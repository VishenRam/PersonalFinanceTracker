import React, { useState, useEffect } from 'react';
import AuthForm from './Auth/AuthForm'
import Dashboard from './Dashboard/Dashboard'

const App = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const (savedUser) = localStorage.getItem('financeUser');
        if (savedUser){
            setUser(JSON.parse(savedUser));
        }
    }, []);

    const handleLogin = (userData) => {
        setUSer(userData);
        localStorage.setItem('financeUser', JSON.stringify(userData));
    };

    const handleLogout = () => {
        setUser(null);
        localStorage.removeItem('financeUser');
    };

    return user ? (
        <Dashboard user={user} onLogout={handleLogout} />
    ) : (
        <div className="container">
            <div className="header>
            <h1>Personal Finance Tracker</h1>
            <p>Take control of your financial future</p>
            </div>
            <AuthForm onLogin={handleLogin} />
        </div>
    );
};

export Default App;