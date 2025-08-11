package com.financetracker.repository;

import com.financetracker.entity.Transactions;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TransactionRepository extends JpaRepository<Transactions, Long>
{
    List<Transactions> findByUserIdOrderByTransactionDateDesc(Long userId);

    @Query("SELECT t FROM Transactions t WHERE t.user.id = :userId AND t.transactionDate BETWEEN :startDate AND :endDate")
    List<Transactions> findByUserIdAndDateRange(@Param("userId") Long userId,
                                                @Param("startDate") LocalDateTime startDate,
                                                @Param("endDate") LocalDateTime endDate);

    @Query("SELECT t.category, SUM(t.amount) FROM Transaction t WHERE t.user_id = :userId AND t.type = 'EXPENSE GROUP BY t.category")
    List<Object[]> findExpensesByCategory(@Param("userId") Long userId);
}
