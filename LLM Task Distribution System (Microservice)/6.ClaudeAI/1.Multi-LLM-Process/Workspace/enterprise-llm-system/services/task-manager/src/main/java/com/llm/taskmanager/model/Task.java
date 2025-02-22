package com.llm.taskmanager.model;

import lombok.Data;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import javax.persistence.*;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "tasks")
@Data
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
    private Integer priority = 1;

    @Column(name = "status", nullable = false)
    private String status = "pending";

    @Column(name = "input_data", columnDefinition = "jsonb", nullable = false)
    private String inputDataJson;

    @Column(name = "output_data", columnDefinition = "jsonb")
    private String outputDataJson;

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
    private Integer retryCount = 0;

    @Column(name = "max_retries")
    private Integer maxRetries = 3;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_task_id")
    private Task parentTask;

    @Column(name = "execution_order")
    private Integer executionOrder;

    @Column(name = "metadata", columnDefinition = "jsonb")
    private String metadataJson;

    @Transient
    private JsonNode inputData;

    @Transient
    private JsonNode outputData;

    @Transient
    private JsonNode metadata;

    public JsonNode getInputData() {
        if (inputData == null && inputDataJson != null) {
            try {
                inputData = new ObjectMapper().readTree(inputDataJson);
            } catch (Exception e) {
                throw new RuntimeException("Error parsing input data", e);
            }
        }
        return inputData;
    }

    public void setInputData(JsonNode inputData) {
        this.inputData = inputData;
        try {
            this.inputDataJson = new ObjectMapper().writeValueAsString(inputData);
        } catch (Exception e) {
            throw new RuntimeException("Error serializing input data", e);
        }
    }

    public JsonNode getOutputData() {
        if (outputData == null && outputDataJson != null) {
            try {
                outputData = new ObjectMapper().readTree(outputDataJson);
            } catch (Exception e) {
                throw new RuntimeException("Error parsing output data", e);
            }
        }
        return outputData;
    }

    public void setOutputData(JsonNode outputData) {
        this.outputData = outputData;
        try {
            this.outputDataJson = new ObjectMapper().writeValueAsString(outputData);
        } catch (Exception e) {
            throw new RuntimeException("Error serializing output data", e);
        }
    }

    public JsonNode getMetadata() {
        if (metadata == null && metadataJson != null) {
            try {
                metadata = new ObjectMapper().readTree(metadataJson);
            } catch (Exception e) {
                throw new RuntimeException("Error parsing metadata", e);
            }
        }
        return metadata;
    }

    public void setMetadata(JsonNode metadata) {
        this.metadata = metadata;
        try {
            this.metadataJson = new ObjectMapper().writeValueAsString(metadata);
        } catch (Exception e) {
            throw new RuntimeException("Error serializing metadata", e);
        }
    }

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
