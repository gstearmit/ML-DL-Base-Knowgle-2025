package com.llm.taskmanager.model;

import lombok.Data;
import javax.persistence.*;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "task_history")
@Data
public class TaskHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "history_id")
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;

    @Column(name = "status_from")
    private String statusFrom;

    @Column(name = "status_to", nullable = false)
    private String statusTo;

    @Column(name = "changed_at")
    private ZonedDateTime changedAt;

    @Column(name = "changed_by")
    private UUID changedBy;

    @Column(name = "reason")
    private String reason;

    @PrePersist
    protected void onCreate() {
        changedAt = ZonedDateTime.now();
    }
}
