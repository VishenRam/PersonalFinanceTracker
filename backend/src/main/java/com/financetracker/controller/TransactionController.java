package com.financetracker.controller;

import com.financetracker.entity.Transactions;
import com.financetracker.service.TransactionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/transactions")
@CrossOrigin(origins = "*")
public class TransactionController
{
    @Autowired
    private TransactionService transactionService;

    @PostMapping
    public ResponseEntity<?> createTransaction(@RequestBody Map<String, String> request)
    {
        try
        {
            Long userId = Long.valueOf(request.get("userId").toString());
            String description = (String) request.get("description");
            Double amount = Double.valueOf(request.get("amount").toString());
            Transactions.TransactionType type = Transactions.TransactionType.valueOf((String) request.get("type"));
            String category = (String) request.get("category");

            Transactions transactions = transactionService.createTransaction(userId, description, amount, type, category);
            return ResponseEntity.ok(transactions);
        }
        catch (Exception e)
        {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Transactions>> getUserTransactions(@PathVariable Long userId)
    {
        List<Transactions> transactions = transactionService.getUserTransactions(userId);
        return ResponseEntity.ok(transactions);
    }

    @GetMapping("/user/{userId}/expenses-by-category")
    public ResponseEntity<Map<String, Double>> getExpensesByCategory(@PathVariable Long userId)
    {
        Map<String, Double> expenses = transactionService.getExpensesByCategory(userId);
        return ResponseEntity.ok(expenses);
    }

    @DeleteMapping("/{transactionId")
    public ResponseEntity<?> deleteTransaction(@PathVariable Long transactionId)
    {
        transactionService.deleteTransaction(transactionId);
        return ResponseEntity.ok(Map.of("message", "Transaction deleted successfully"));
    }
}
