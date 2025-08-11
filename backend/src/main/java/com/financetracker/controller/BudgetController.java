package com.financetracker.controller;

import com.financetracker.entity.User;
import com.financetracker.entity.Transactions;
import com.financetracker.entity.Budget;
import com.financetracker.service.UserService;
import com.financetracker.service.TransactionService;
import com.financetracker.service.BudgetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.parameters.P;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/budgets")
@CrossOrigin(origins = "*")
public class BudgetController
{
    @Autowired
    private BudgetService budgetService;

    @PostMapping
    public ResponseEntity<?> createOrUpdateBudget(@RequestBody Map<String, Object> request)
    {
        try
        {
            Long userId = Long.valueOf(request.get("userId").toString());
            String category = (String) request.get("category");
            Double amount = Double.valueOf(request.get("amount").toString());
            Integer month = Integer.valueOf(request.get("month").toString());
            Integer year = Integer.valueOf(request.get("year").toString());

            Budget budget = budgetService.createOrUpdateBudget(userId, category, amount, month, year);
            return ResponseEntity.ok(budget);
        }
        catch (Exception e)
        {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Budget>> getUserBudgets(@PathVariable Long userId,
                                                       @RequestParam Integer month,
                                                       @RequestParam Integer year)
    {
        List<Budget> budgets = budgetService.getUserBudgets(userId, month, year);
        return ResponseEntity.ok(budgets);
    }

    @DeleteMapping("/{budgetId}")
    public ResponseEntity<?> deleteBudget(@PathVariable Long budgetId)
    {
        budgetService.deleteBudget(budgetId);
        return ResponseEntity.ok(Map.of("message", "Budget deleted successfully"));
    }
}


