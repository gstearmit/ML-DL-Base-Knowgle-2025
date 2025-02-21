package com.llm.taskmanager.model;

import lombok.Data;
import javax.persistence.*;
import java.util.UUID;
import java.time.LocalDateTime;

@Entity
@Table(name = "tasks")
@Data
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "project_id")
    private Project project;

    @Column(nullable = false)
    private String input;

    @Column(nullable = false)
    private String[] models;

    @Column(nullable = false)
    private Integer priority;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "status")
    private String status;
} 