package com.llm.taskmanager.model;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.ZonedDateTime;
import java.util.UUID;

@Data
public class TaskRequest {
    @NotNull
    private UUID projectId;

    @NotNull
    private UUID userId;

    @NotBlank
    private String taskType;

    private JsonNode inputData;

    private Integer priority = 1;

    private ZonedDateTime deadline;

    private UUID parentTaskId;

    private Integer executionOrder;

    private JsonNode metadata;
}
