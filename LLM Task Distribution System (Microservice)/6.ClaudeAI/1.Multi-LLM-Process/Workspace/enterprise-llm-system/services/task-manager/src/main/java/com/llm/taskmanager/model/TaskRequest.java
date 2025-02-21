package com.llm.taskmanager.model;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class TaskRequest {
    @NotBlank
    private String input;

    @NotNull
    private String[] models;

    @NotNull
    private Integer priority;

    private String userId;
} 