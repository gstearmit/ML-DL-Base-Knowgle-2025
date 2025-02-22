package com.llm.taskmanager.repository;

import com.llm.taskmanager.model.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TaskRepository extends JpaRepository<Task, UUID> {
    List<Task> findByProjectId(UUID projectId);
    List<Task> findByProjectIdAndStatus(UUID projectId, String status);
    List<Task> findByUserId(UUID userId);
    List<Task> findByUserIdAndStatus(UUID userId, String status);
    List<Task> findByStatus(String status);
    List<Task> findByParentTaskId(UUID parentTaskId);
    List<Task> findByAssignedWorkerId(UUID workerId);
    
    @Query("SELECT t FROM Task t WHERE t.project.id = ?1 ORDER BY t.priority DESC, t.createdAt ASC")
    List<Task> findByProjectIdOrderByPriorityAndCreatedAt(UUID projectId);
    
    @Query("SELECT t FROM Task t WHERE t.status = 'pending' OR t.status = 'in_queue' ORDER BY t.priority DESC, t.createdAt ASC")
    List<Task> findPendingTasksOrderByPriority();
    
    @Query("SELECT t FROM Task t WHERE t.project.id = ?1 AND (t.status = 'pending' OR t.status = 'in_queue') ORDER BY t.priority DESC, t.createdAt ASC")
    List<Task> findPendingTasksByProjectOrderByPriority(UUID projectId);
    
    @Query("SELECT COUNT(t) FROM Task t WHERE t.project.id = ?1 AND t.status = ?2")
    long countByProjectIdAndStatus(UUID projectId, String status);
}
