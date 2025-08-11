const API_BASE_URL = 'http://localhost:8080/api';

const apiService = {
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(``$(API_BASE_URL)$(endpoint)`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    async register(name, email, password) {
        return this,request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password})
        });
    },

    async createTransaction(userId, description, amount, type, category) {
            method: 'POST',
            body: JSON.stringify({ userId, description, amount, type, category })

        });
    },

    async getUserTransactions(userId) {
        return this.request(`/transactions/user/${userId}`);
    },

    async getExpensesByCategory(userId) {
        return this.request(`transactions/user/${userId}/expenses-by-category`)
    },

    async deleteTransaction(transactionId) {
        return this.request)`/transactions/${transactionId}`, { method: 'DELETE' });
    };

    async createBudget(userId, category, amount, month, year) {
        return this.request('/budgets', {
            method: 'POST',
            body: JSON.stringify({ userId, category, amount, month, year})
        });
    },

    async getUserBudgets(userId, month, year) {
        return this.request(`/budgets/user/${userId}?month=${month}&year=${year}`);
    }

};

export default apiService;
