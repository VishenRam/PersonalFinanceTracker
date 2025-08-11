package com.financetracker.service;

import com.financetracker.entity.Budget;
import com.financetracker.entity.User;
import com.financetracker.repository.BudgetRepository;
import com.financetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.HashMap;
import java.util.Map;

@Service
public class BudgetService
{
    @Autowired
    private BudgetRepository budgetRepository;

    @Autowired
    private UserRepository userRepository;

    public Budget createOrUpdateBudget(Long userId, String category, Double amount, Integer month, Integer year)
    {
        User user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));

        Optional<Budget> existingBudget = budgetRepository
                .findByUserIdAndCategoryAndMonthAndYear(userId, category, month, year);

        if(existingBudget.isPresent())
        {
            Budget budget = existingBudget.get();
            budget.setAmount(amount);
            return budgetRepository.save(budget);
        }
        else
        {
            Budget budget = new Budget(category, amount, month, year, user);
            return budgetRepository.save(budget);
        }
    }

    public List<Budget> getUserBudgets(Long userId, Integer month, Integer year)
    {
        return budgetRepository.findByUserIdAndMonthAndYear(userId, month, year);
    }

    public void deleteBudget(Long budgetId)
    {
        budgetRepository.deleteById(budgetId);
    }
}

