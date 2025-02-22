package com.llm.taskmanager.model;

import lombok.Data;
import com.fasterxml.jackson.databind.JsonNode;
import com.vladmihalcea.hibernate.type.json.JsonBinaryType;

import javax.persistence.*;
import org.hibernate.annotations.Type;
import org.hibernate.annotations.TypeDef;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "projects")
@Data
@TypeDef(name = "jsonb", typeClass = JsonBinaryType.class)
public class Project {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "project_id")
    private UUID id;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(name = "project_name", nullable = false)
    private String name;

    @Column(name = "project_description")
    private String description;

    @Column(name = "api_key", nullable = false)
    private UUID apiKey;

    @Column(name = "status")
    private String status = "active";

    @Column(name = "priority")
    private Integer priority = 1;

    @Column(name = "created_at")
    private ZonedDateTime createdAt;

    @Column(name = "updated_at")
    private ZonedDateTime updatedAt;

    @Column(name = "deadline")
    private ZonedDateTime deadline;

    @Type(type = "jsonb")
    @Column(name = "metadata", columnDefinition = "jsonb")
    private JsonNode metadata;

    @Type(type = "jsonb")
    @Column(name = "settings", columnDefinition = "jsonb")
    private JsonNode settings;

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
