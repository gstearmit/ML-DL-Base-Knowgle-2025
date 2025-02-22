package com.llm.taskmanager.repository;

import com.llm.taskmanager.model.Project;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ProjectRepository extends JpaRepository<Project, UUID> {
    List<Project> findByUserId(UUID userId);
    Optional<Project> findByUserIdAndName(UUID userId, String name);
    List<Project> findByStatus(String status);
    List<Project> findByUserIdAndStatus(UUID userId, String status);
    boolean existsByUserIdAndName(UUID userId, String name);
}
