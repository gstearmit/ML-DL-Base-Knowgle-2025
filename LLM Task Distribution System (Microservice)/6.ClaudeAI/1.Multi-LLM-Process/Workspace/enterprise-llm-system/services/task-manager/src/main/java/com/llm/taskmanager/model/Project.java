package com.llm.taskmanager.model;

import lombok.Data;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import javax.persistence.*;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "projects")
@Data
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

    @Column(name = "metadata", columnDefinition = "jsonb")
    private String metadataJson;

    @Column(name = "settings", columnDefinition = "jsonb")
    private String settingsJson;

    @Transient
    private JsonNode metadata;

    @Transient
    private JsonNode settings;

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

    public JsonNode getSettings() {
        if (settings == null && settingsJson != null) {
            try {
                settings = new ObjectMapper().readTree(settingsJson);
            } catch (Exception e) {
                throw new RuntimeException("Error parsing settings", e);
            }
        }
        return settings;
    }

    public void setSettings(JsonNode settings) {
        this.settings = settings;
        try {
            this.settingsJson = new ObjectMapper().writeValueAsString(settings);
        } catch (Exception e) {
            throw new RuntimeException("Error serializing settings", e);
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
