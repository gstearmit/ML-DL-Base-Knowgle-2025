package com.llm.taskmanager.repository;

import com.llm.taskmanager.model.TaskHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TaskHistoryRepository extends JpaRepository<TaskHistory, UUID> {
    List<TaskHistory> findByTaskId(UUID taskId);
    List<TaskHistory> findByTaskIdOrderByChangedAtDesc(UUID taskId);
    List<TaskHistory> findByChangedBy(UUID userId);
}
