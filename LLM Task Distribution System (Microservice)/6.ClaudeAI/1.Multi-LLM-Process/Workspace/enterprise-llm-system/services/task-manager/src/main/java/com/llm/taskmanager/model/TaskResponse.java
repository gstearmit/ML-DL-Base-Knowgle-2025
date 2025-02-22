package com.llm.taskmanager.model;

import lombok.Builder;
import lombok.Data;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.ZonedDateTime;
import java.util.UUID;

@Data
@Builder
public class TaskResponse {
    private UUID taskId;
    private UUID projectId;
    private String taskType;
    private String status;
    private Integer priority;
    private ZonedDateTime createdAt;
    private ZonedDateTime startedAt;
    private ZonedDateTime completedAt;
    private ZonedDateTime deadline;
    private String errorMessage;
    private UUID parentTaskId;
    private Integer executionOrder;
    private JsonNode inputData;
    private JsonNode outputData;
    private JsonNode metadata;
}
