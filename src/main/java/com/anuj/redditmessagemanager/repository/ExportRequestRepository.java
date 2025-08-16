package com.anuj.redditmessagemanager.repository;

import com.anuj.redditmessagemanager.entity.ExportRequest;
import com.anuj.redditmessagemanager.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ExportRequestRepository extends JpaRepository<ExportRequest, Long> {

    Optional<ExportRequest> findByExportId(String exportId);

    List<ExportRequest> findByUserOrderByCreatedAtDesc(User user);

    Page<ExportRequest> findByUserOrderByCreatedAtDesc(User user, Pageable pageable);

    List<ExportRequest> findByExportStatus(ExportRequest.ExportStatus status);

    @Query("SELECT er FROM ExportRequest er WHERE er.user = :user AND er.exportStatus = :status ORDER BY er.createdAt DESC")
    List<ExportRequest> findByUserAndStatus(@Param("user") User user, 
                                          @Param("status") ExportRequest.ExportStatus status);

    @Query("SELECT er FROM ExportRequest er WHERE er.createdAt < :cutoffDate AND er.exportStatus IN :statuses")
    List<ExportRequest> findOldRequests(@Param("cutoffDate") LocalDateTime cutoffDate, 
                                       @Param("statuses") List<ExportRequest.ExportStatus> statuses);

    @Query("SELECT COUNT(er) FROM ExportRequest er WHERE er.user = :user AND er.exportStatus = :status")
    long countByUserAndStatus(@Param("user") User user, 
                             @Param("status") ExportRequest.ExportStatus status);

    @Query("SELECT COUNT(er) FROM ExportRequest er WHERE er.user = :user AND er.createdAt BETWEEN :startDate AND :endDate")
    long countByUserAndDateRange(@Param("user") User user, 
                                @Param("startDate") LocalDateTime startDate, 
                                @Param("endDate") LocalDateTime endDate);

    boolean existsByExportId(String exportId);

    void deleteByExportStatusAndCreatedAtBefore(ExportRequest.ExportStatus status, LocalDateTime cutoffDate);

    @Query("SELECT er FROM ExportRequest er WHERE er.exportStatus = 'IN_PROGRESS' AND er.createdAt < :timeout")
    List<ExportRequest> findStuckRequests(@Param("timeout") LocalDateTime timeout);
}
