import React from 'react';
import { formatCurrency } from '../../utils/formatters';

const StatsGrid = ({ stats }) => {
    return (
        <div className="stats-grid">
            <div className="stat-card">
                <div className="stat-value">{formatCurrency(stats.balance)}</div>
                <div className="stat-label">Current Balance</div>
            </div>
            <div className="stat-card">
                <div className="stat-value">{formatCurrency(stats.totalncome)}</div>
                <div className="stat-label">Total Income</div>
            </div>
            <div className="stat-card">
                <div className="stat-value">{stats.transactionCount}</div>
                <div className="stat-label">Transactions</div>
            </div>
        </div>
    );
};

export default StatsGrid;