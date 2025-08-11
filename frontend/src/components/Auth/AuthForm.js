import React, { useState } from 'react';
import apiService from '../../services/apiService';
import styles from '../../styles/components/Auth.module.css';

const AuthForm = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });

    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            let result;
            if (isLogin) {
                result = await apiService.login(formData.email, formData.password);
            }else {
                result = await apiService.register(formData.name, formData.email, formData.password)
            }

            if (result.error) {
                setMessage(result.error);
            } else {
                if (isLogin) {
                    onLogin(result);
                } else {
                    setMessage('Registrationm successful! Please login.');
                    setIsLogin(true);
                }
            }
        } catch (error) {
            setMessage('An error occured. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className={styles.authContainer}>
            <div className="card">
                <h2 className={styles.title}>
                    {isLogin ? 'Login' : 'Register'}
                </h2>

                {message && (
                    <div className={`alert ${message.includes('error') || message.includes('Invalid') ? 'alert-error' : 'alert-success'}`}>
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                    <div className="form-group">
                        <label>Full Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputCharge}
                            required={!isLogin}
                        />
                    </div>
                )};

                <div className="form-group">
                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <button type="submit" className={`btn ${sty;es.submitBtn}`} disabled={loading}>
                    {loading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
                </button>
                </form>

                <p className={styles.switchText}>
                    {isLogin ? "Don't have am account? " : "Already have an account? "}
                    <span
                        className={styles.switchLink}
                        onClick={() => setIsLogin(!isLogin)}
                    >
                        {isLogin ? 'Register' : 'Login'}
                    </span>
                </p>
            </div>
        </div>
    );
};

export default AuthForm;