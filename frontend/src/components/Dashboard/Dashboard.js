import React, { useState, useEffect } from 'react';
import apiService from '../../services/apiService';
import StatsGrid from './StatsGrid';
import TabNavigation from './TabNavigation';
import TransactionList from '../Transactions/TransactionList';
import TransactionFrom from '../Transactions/TransactionForm';
import BudgetList from '../Budgets/BudgetList';
import BudgetForm from '../Budgets/BudgetForm';
import ExpensePieChart from '../Charts/ExpensePieChart';
import Modal from '../UI/Modal';
import styles from '../../styles/components/Dashboard.module.css';

const Dashboard = ({ user, logout }) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [transactions, setTransactions] = useState([]);
    const [budgets, setBudgets] = useState([]);
    const [expensesByCategory, setExpensesByCategory] = useState({});
    const [showModal, setShowModal] = useState(false);
    const [modalType, setModalType] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect (() => {
        loadData();
    }, [user]);

    const loadData = async () => {
        try {
            const [transactionsData, expensesData, budgetsData] = await Promise.all ([
                apiService.getUserTransactions(user.userId);
                apiService.getExpensesByCategory(user.userId);
                apiService.getUserBudgets(user.userId, new Date().getMonth() + 1, new Date().getFullYear())
                ]);

                setTransactions(transactionsData);
                setExpensesByCategory(expensesData);
                setBudgets(budgetsData);
        } catch (error) {
            console.error ('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    consts calculateStats = () => {
        const totalIncome = transactions
            .filter(t => t.type === 'INCOME')
            .reduce((sum, t) => sum + t.amount, 0);

        const totalExpenses = transactions
            .filter(t => t.type === 'EXPENSE')
            .reduce((sum, t) => sum + t.amount, 0);

        const balance = totalIncome - totalExpenses;

        return { totalIncome, totalExpenses, balance, transactionCount: transactions.length };
    };

    const openModal = (type) => {
        setModalType(type);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setModalType('');
    };

    if (loading) {
        return (
            <div className="container">
                <div className={styles.loading}>
                    Loading...
                </div>
            </div>
        );
    }

    const stats = calculateStats();

    return (
        <div className="container">
            <div className="header">
                <h1>Welcome back, {user.name}!</h1>
                <p>Track your finances and achieve your goals</p>
                <button className="btn btn-secondary" onClick={onLogout}>Logout</button>
            </div>

            <StatsGrid stats={stats} />
            <TabNavigation activeTab={activeTab} setActiveTa={setActiveTab} />

            <div className={`tab-content ${activeTab === 'overview' ? 'active' : ''}`}>
                <div className="dashboard">
                    <div className="card">
                        <h3>Expense Categories</h3>
                        <Expense PieChart data={expensesByCategory} />
                    </div>
                    <div className="card">
                        <h3>Recent Transactions</h3>
                        <TransactionList
                          transactions={transactions.slice(0, 5)}
                          onDelete={loadData}
                        />
                        <button
                            className="btn"
                            onClick={() => setActiveTab('transactions')}
                            style={{ marginTop: '15px'}}
                        >
                            View All
                        </button>
                    </div>
                </div>
        </div>

        <div className={`tab-content ${activeTab === 'transactions' ? 'active' : ''}`}>
            <div className="card">
                <div className={styles.cardHeader}>
                    <h3>All Transactions</h3>
                    <button className="btn" onClick={() => openModal('transaction')}>
                        Add Transaction
                    </button>
                </div>
                <BudgetList budgets={budgets} expenses={expensesByCategory} onDelete={loadData} />
            </div>
        </div>

        {showModal && (
            <Modal onClose={closeModal}>
                {modalType === 'transaction' && (
                    <TransactionForm user={user} onSubmit={() => { loadData(); closeModal();}} />
                )}
                {modalType === 'budget' && (
                    <BudgetForm user={user} onSubmit={() => { loadData(); closeModal(); }} />
                )}
            </Modal>
        )}
    </div>
    );
};

export default Dashboard