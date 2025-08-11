package com.financetracker.service;

import com.financetracker.entity.Transactions;
import com.financetracker.entity.User;
import com.financetracker.repository.TransactionRepository;
import com.financetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

@Service
public class TransactionService {
    @Autowired
    private TransactionRepository transactionRepository;

    @Autowired
    private UserRepository userRepository;

    public Transactions createTransaction(Long userId, String description, Double amount, Transactions.TransactionType type, String category)
    {
        User user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));

        Transactions transactions = new Transactions(description, amount, type, category, user);
        return transactionRepository.save(transactions);

    }

    public List<Transactions> getUserTransactions(Long userId)
    {
        return transactionRepository.findByUserIdOrderByTransactionDateDesc(userId);
    }

    public List<Transactions> getTransactionsByDateRange(Long userId, LocalDateTime startDate, LocalDateTime endDate)
    {
        return transactionRepository.findByUserIdAndDateRange(userId, startDate, endDate);
    }

    public Map<String, Double> getExpensesByCategory(Long userId)
    {
        List<Object[]> results = transactionRepository.findExpensesByCategory(userId);
        Map<String, Double> expenses = new HashMap<>();

        for (Object[] result : results)
        {
            String category = (String) result[0];
            Double amount = (Double) result[1];
            expenses.put(category, amount);
        }

        return expenses;
    }

    public void deleteTransaction(Long transactionId)
    {
        transactionRepository.deleteById(transactionId);
    }

}
