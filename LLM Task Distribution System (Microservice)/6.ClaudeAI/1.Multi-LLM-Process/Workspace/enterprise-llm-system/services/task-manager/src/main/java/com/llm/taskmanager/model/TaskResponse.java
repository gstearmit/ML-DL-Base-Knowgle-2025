package com.llm.taskmanager.model;

import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
public class TaskResponse {
    private UUID taskId;
    private String status;
    private LocalDateTime createdAt;
} 