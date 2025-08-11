import React from 'react';

const TabNavigation = ({ activeTab, setActiveTab }) => {
    const tabs = [
        { key: 'overview', label: 'Overview'},
        { key: 'transactions', label: 'Transactions'},
        { key: 'budgets', label: 'Budgets'}
    ];

    return (
        <div className="tabs">
            {tabs.map(tab => (
            <button
                key={tab.key}
                className={`tab ${activeTab === tab.key ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.key)}
            >
                {tab.label}
            </button>
            ))}
        </div>
    );
};

export default TabNavigation;