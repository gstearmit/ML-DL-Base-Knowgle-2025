package com.llm.taskmanager.model;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.databind.JsonNode;
import com.vladmihalcea.hibernate.type.json.JsonBinaryType;

import javax.persistence.*;
import org.hibernate.annotations.Type;
import org.hibernate.annotations.TypeDef;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "tasks")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@TypeDef(name = "jsonb", typeClass = JsonBinaryType.class)
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "task_id")
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(name = "task_type", nullable = false)
    private String taskType;

    @Column(name = "priority")
    @Builder.Default
    private Integer priority = 1;

    @Column(name = "status", nullable = false)
    @Builder.Default
    private String status = "pending";

    @Type(type = "jsonb")
    @Column(name = "input_data", columnDefinition = "jsonb")
    private JsonNode inputData;

    @Type(type = "jsonb")
    @Column(name = "output_data", columnDefinition = "jsonb")
    private JsonNode outputData;

    @Column(name = "error_message")
    private String errorMessage;

    @Column(name = "created_at")
    private ZonedDateTime createdAt;

    @Column(name = "updated_at")
    private ZonedDateTime updatedAt;

    @Column(name = "started_at")
    private ZonedDateTime startedAt;

    @Column(name = "completed_at")
    private ZonedDateTime completedAt;

    @Column(name = "deadline")
    private ZonedDateTime deadline;

    @Column(name = "assigned_worker_id")
    private UUID assignedWorkerId;

    @Column(name = "retry_count")
    @Builder.Default
    private Integer retryCount = 0;

    @Column(name = "max_retries")
    @Builder.Default
    private Integer maxRetries = 3;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_task_id")
    private Task parentTask;

    @Column(name = "execution_order")
    private Integer executionOrder;

    @Type(type = "jsonb")
    @Column(name = "metadata", columnDefinition = "jsonb")
    private JsonNode metadata;

    @PrePersist
    protected void onCreate() {
        createdAt = ZonedDateTime.now();
        updatedAt = ZonedDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = ZonedDateTime.now();
    }
}
