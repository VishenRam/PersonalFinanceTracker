"""
Personal Finance Tracker - Python Data Analysis Module
This script provides advanced analytics and reporting for the finance tracker
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import requests
import json
from datetime import datetime, timedelta
import warnings
from typing import List, Dict, Tuple
import argparse
import os
from dataclasses import dataclass

warnings.filterwarnings('ignore')

@dataclass
class DatabaseConfig:
    """Database configuration class"""
    host: str = "localhost"
    port: int = 5432
    database: str = "finance_tracker"
    username: str = "finance_user"
    password: str = "your_password_here"

class FinanceAnalyzer:
    """Advanced finance analytics class"""

    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.connection = None
        self.df_transactions = None
        self.df_budgets = None

    def connect_database(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                database=self.db_config.database,
                user=self.db_config.username,
                password=self.db_config.password
            )
            print("✅ Database connection established")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

    def load_data(self, user_id: int = None) -> bool:
        """Load transaction and budget data"""
        if not self.connection:
            if not self.connect_database():
                return False

        try:
            # Load transactions
            transaction_query = """
                SELECT t.*, u.name as user_name, u.email
                FROM transactions t
                JOIN users u ON t.user_id = u.id
            """
            if user_id:
                transaction_query += f" WHERE t.user_id = {user_id}"

            self.df_transactions = pd.read_sql(transaction_query, self.connection)
            self.df_transactions['transaction_date'] = pd.to_datetime(self.df_transactions['transaction_date'])

            # Load budgets
            budget_query = """
                SELECT b.*, u.name as user_name, u.email
                FROM budgets b
                JOIN users u ON b.user_id = u.id
            """
            if user_id:
                budget_query += f" WHERE b.user_id = {user_id}"

            self.df_budgets = pd.read_sql(budget_query, self.connection)

            print(f"✅ Loaded {len(self.df_transactions)} transactions and {len(self.df_budgets)} budgets")
            return True

        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False

    def generate_monthly_report(self, year: int, month: int, user_id: int = None) -> Dict:
        """Generate comprehensive monthly financial report"""
        if self.df_transactions is None:
            print("❌ No data loaded. Please run load_data() first.")
            return {}

        # Filter data for the specified month
        df = self.df_transactions.copy()
        if user_id:
            df = df[df['user_id'] == user_id]

        df = df[
            (df['transaction_date'].dt.year == year) &
            (df['transaction_date'].dt.month == month)
        ]

        if df.empty:
            print(f"❌ No transactions found for {month}/{year}")
            return {}

        # Calculate basic metrics
        total_income = df[df['type'] == 'INCOME']['amount'].sum()
        total_expenses = df[df['type'] == 'EXPENSE']['amount'].sum()
        net_savings = total_income - total_expenses

        # Category breakdown
        expense_by_category = df[df['type'] == 'EXPENSE'].groupby('category')['amount'].sum().to_dict()
        income_by_category = df[df['type'] == 'INCOME'].groupby('category')['amount'].sum().to_dict()

        # Daily spending pattern
        daily_expenses = df[df['type'] == 'EXPENSE'].groupby(df['transaction_date'].dt.day)['amount'].sum()

        # Budget analysis
        budget_analysis = {}
        if not self.df_budgets.empty:
            month_budgets = self.df_budgets[
                (self.df_budgets['month'] == month) &
                (self.df_budgets['year'] == year)
            ]
            if user_id:
                month_budgets = month_budgets[month_budgets['user_id'] == user_id]

            for _, budget in month_budgets.iterrows():
                category = budget['category']
                budget_amount = budget['amount']
                spent = expense_by_category.get(category, 0)
                remaining = budget_amount - spent
                utilization = (spent / budget_amount) * 100 if budget_amount > 0 else 0

                budget_analysis[category] = {
                    'budgeted': budget_amount,
                    'spent': spent,
                    'remaining': remaining,
                    'utilization_percent': utilization,
                    'status': 'over_budget' if spent > budget_amount else 'on_track'
                }

        report = {
            'period': f"{month}/{year}",
            'summary': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_savings': net_savings,
                'savings_rate': (net_savings / total_income * 100) if total_income > 0 else 0,
                'transaction_count': len(df)
            },
            'expense_breakdown': expense_by_category,
            'income_breakdown': income_by_category,
            'daily_spending': daily_expenses.to_dict(),
            'budget_analysis': budget_analysis,
            'top_expenses': df[df['type'] == 'EXPENSE'].nlargest(10, 'amount')[['description', 'amount', 'category']].to_dict('records')
        }

        return report

    def calculate_trends(self, months: int = 6, user_id: int = None) -> Dict:
        """Calculate financial trends over specified months"""
        if self.df_transactions is None:
            print("❌ No data loaded. Please run load_data() first.")
            return {}

        df = self.df_transactions.copy()
        if user_id:
            df = df[df['user_id'] == user_id]

        # Get data for last N months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        df = df[df['transaction_date'] >= start_date]

        # Monthly aggregations
        df['year_month'] = df['transaction_date'].dt.to_period('M')
        monthly_stats = df.groupby(['year_month', 'type'])['amount'].sum().unstack(fill_value=0)

        # Calculate trends
        if 'INCOME' in monthly_stats.columns:
            income_trend = monthly_stats['INCOME'].pct_change().mean() * 100
        else:
            income_trend = 0

        if 'EXPENSE' in monthly_stats.columns:
            expense_trend = monthly_stats['EXPENSE'].pct_change().mean() * 100
        else:
            expense_trend = 0

        # Category trends
        category_trends = {}
        for category in df['category'].unique():
            cat_data = df[df['category'] == category].groupby('year_month')['amount'].sum()
            if len(cat_data) > 1:
                trend = cat_data.pct_change().mean() * 100
                category_trends[category] = trend

        return {
            'period_months': months,
            'income_trend_percent': income_trend,
            'expense_trend_percent': expense_trend,
            'category_trends': category_trends,
            'monthly_data': monthly_stats.to_dict()
        }

    def detect_anomalies(self, user_id: int = None) -> List[Dict]:
        """Detect unusual spending patterns"""
        if self.df_transactions is None:
            print("❌ No data loaded. Please run load_data() first.")
            return []

        df = self.df_transactions.copy()
        if user_id:
            df = df[df['user_id'] == user_id]

        df = df[df['type'] == 'EXPENSE']
        anomalies = []

        # Overall spending anomalies
        Q1 = df['amount'].quantile(0.25)
        Q3 = df['amount'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR

        large_expenses = df[df['amount'] > upper_bound]
        for _, expense in large_expenses.iterrows():
            anomalies.append({
                'type': 'large_expense',
                'description': expense['description'],
                'amount': expense['amount'],
                'category': expense['category'],
                'date': expense['transaction_date'].strftime('%Y-%m-%d'),
                'severity': 'high' if expense['amount'] > Q3 + 3 * IQR else 'medium'
            })

        # Category-based anomalies
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            if len(cat_data) > 5:  # Need sufficient data
                cat_mean = cat_data['amount'].mean()
                cat_std = cat_data['amount'].std()
                threshold = cat_mean + 2 * cat_std

                cat_anomalies = cat_data[cat_data['amount'] > threshold]
                for _, expense in cat_anomalies.iterrows():
                    if expense['id'] not in [a.get('transaction_id') for a in anomalies]:
                        anomalies.append({
                            'type': 'category_anomaly',
                            'transaction_id': expense['id'],
                            'description': expense['description'],
                            'amount': expense['amount'],
                            'category': expense['category'],
                            'date': expense['transaction_date'].strftime('%Y-%m-%d'),
                            'expected_range': f"${cat_mean:.2f} ± ${2*cat_std:.2f}",
                            'severity': 'medium'
                        })

        return sorted(anomalies, key=lambda x: x['amount'], reverse=True)

    def create_visualizations(self, user_id: int = None, output_dir: str = "reports"):
        """Create financial visualizations"""
        if self.df_transactions is None:
            print("❌ No data loaded. Please run load_data() first.")
            return

        os.makedirs(output_dir, exist_ok=True)

        df = self.df_transactions.copy()
        if user_id:
            df = df[df['user_id'] == user_id]

        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Personal Finance Dashboard', fontsize=16, fontweight='bold')

        # 1. Monthly Income vs Expenses
        monthly_data = df.groupby([df['transaction_date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        if not monthly_data.empty:
            monthly_data.plot(kind='bar', ax=axes[0,0], color=['#2E8B57', '#DC143C'])
            axes[0,0].set_title('Monthly Income vs Expenses')
            axes[0,0].set_xlabel('Month')
            axes[0,0].set_ylabel('Amount ($)')
            axes[0,0].tick_params(axis='x', rotation=45)

        # 2. Expense Categories Pie Chart
        expense_cats = df[df['type'] == 'EXPENSE'].groupby('category')['amount'].sum()
        if not expense_cats.empty:
            axes[0,1].pie(expense_cats.values, labels=expense_cats.index, autopct='%1.1f%%', startangle=90)
            axes[0,1].set_title('Expenses by Category')

        # 3. Daily Spending Trend
        daily_expenses = df[df['type'] == 'EXPENSE'].groupby(df['transaction_date'].dt.date)['amount'].sum()
        if not daily_expenses.empty:
            daily_expenses.plot(kind='line', ax=axes[1,0], color='#FF6B6B')
            axes[1,0].set_title('Daily Spending Trend')
            axes[1,0].set_xlabel('Date')
            axes[1,0].set_ylabel('Amount ($)')
            axes[1,0].tick_params(axis='x', rotation=45)

        # 4. Savings Rate Over Time
        monthly_summary = df.groupby([df['transaction_date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        if 'INCOME' in monthly_summary.columns and 'EXPENSE' in monthly_summary.columns:
            savings_rate = ((monthly_summary['INCOME'] - monthly_summary['EXPENSE']) / monthly_summary['INCOME'] * 100).fillna(0)
            savings_rate.plot(kind='line', ax=axes[1,1], color='#4ECDC4', marker='o')
            axes[1,1].set_title('Monthly Savings Rate (%)')
            axes[1,1].set_xlabel('Month')
            axes[1,1].set_ylabel('Savings Rate (%)')
            axes[1,1].tick_params(axis='x', rotation=45)
            axes[1,1].axhline(y=20, color='green', linestyle='--', alpha=0.7, label='Target: 20%')
            axes[1,1].legend()

        plt.tight_layout()
        plt.savefig(f"{output_dir}/finance_dashboard.png", dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ Visualizations saved to {output_dir}/finance_dashboard.png")

    def export_report(self, report_data: Dict, output_file: str = "financial_report.json"):
        """Export report to JSON file"""
        # Convert numpy types to native Python types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj

        report_data = convert_types(report_data)

        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        print(f"✅ Report exported to {output_file}")

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

# Data Import/Export Utilities
class DataImporter:
    """Utility class for importing data from various sources"""

    @staticmethod
    def import_from_csv(file_path: str, user_id: int, api_base_url: str = "http://localhost:8080/api") -> bool:
        """Import transactions from CSV file"""
        try:
            df = pd.read_csv(file_path)
            required_columns = ['description', 'amount', 'type', 'category', 'date']

            if not all(col in df.columns for col in required_columns):
                print(f"❌ CSV must contain columns: {required_columns}")
                return False

            # Convert and validate data
            df['amount'] = pd.to_numeric(df['amount'])
            df['type'] = df['type'].str.upper()
            df = df[df['type'].isin(['INCOME', 'EXPENSE'])]

            # Import via API
            success_count = 0
            for _, row in df.iterrows():
                try:
                    response = requests.post(f"{api_base_url}/transactions", json={
                        "userId": user_id,
                        "description": row['description'],
                        "amount": row['amount'],
                        "type": row['type'],
                        "category": row['category']
                    })
                    if response.status_code == 200:
                        success_count += 1
                except Exception as e:
                    print(f"Error importing row: {e}")

            print(f"✅ Successfully imported {success_count}/{len(df)} transactions")
            return True

        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
            return False

def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description='Personal Finance Tracker Analytics')
    parser.add_argument('--user-id', type=int, help='User ID to analyze')
    parser.add_argument('--month', type=int, help='Month for report (1-12)')
    parser.add_argument('--year', type=int, default=datetime.now().year, help='Year for report')
    parser.add_argument('--output-dir', default='reports', help='Output directory for reports')
    parser.add_argument('--export-csv', help='Export data to CSV file')
    parser.add_argument('--import-csv', help='Import data from CSV file')

    args = parser.parse_args()

    # Database configuration
    db_config = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'finance_tracker'),
        username=os.getenv('DB_USER', 'finance_user'),
        password=os.getenv('DB_PASSWORD', 'your_password_here')
    )

    analyzer = FinanceAnalyzer(db_config)

    if not analyzer.load_data(args.user_id):
        return

    try:
        if args.month:
            # Generate monthly report
            report = analyzer.generate_monthly_report(args.year, args.month, args.user_id)
            if report:
                print(f"\n📊 Monthly Report for {args.month}/{args.year}")
                print(f"Total Income: ${report['summary']['total_income']:,.2f}")
                print(f"Total Expenses: ${report['summary']['total_expenses']:,.2f}")
                print(f"Net Savings: ${report['summary']['net_savings']:,.2f}")
                print(f"Savings Rate: {report['summary']['savings_rate']:.1f}%")

                analyzer.export_report(report, f"{args.output_dir}/monthly_report_{args.month}_{args.year}.json")

        # Generate trends analysis
        trends = analyzer.calculate_trends(6, args.user_id)
        if trends:
            print(f"\n📈 6-Month Trends:")
            print(f"Income Trend: {trends['income_trend_percent']:+.1f}%")
            print(f"Expense Trend: {trends['expense_trend_percent']:+.1f}%")

        # Detect anomalies
        anomalies = analyzer.detect_anomalies(args.user_id)
        if anomalies:
            print(f"\n⚠️  Detected {len(anomalies)} spending anomalies:")
            for anomaly in anomalies[:5]:  # Show top 5
                print(f"  • {anomaly['description']}: ${anomaly['amount']:,.2f} ({anomaly['category']})")

        # Create visualizations
        analyzer.create_visualizations(args.user_id, args.output_dir)

        # Handle CSV import
        if args.import_csv and args.user_id:
            DataImporter.import_from_csv(args.import_csv, args.user_id)

        # Handle CSV export
        if args.export_csv:
            if analyzer.df_transactions is not None:
                df_export = analyzer.df_transactions.copy()
                if args.user_id:
                    df_export = df_export[df_export['user_id'] == args.user_id]
                df_export.to_csv(args.export_csv, index=False)
                print(f"✅ Data exported to {args.export_csv}")

    finally:
        analyzer.close_connection()

if __name__ == "__main__":
    main()