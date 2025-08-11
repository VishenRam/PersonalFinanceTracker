export const formatCurrency = (amount) => {
    return new Int1.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount)
};
export const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
};
