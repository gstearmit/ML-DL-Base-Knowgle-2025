package com.llm.taskmanager.controller;

import com.llm.taskmanager.model.Project;
import com.llm.taskmanager.model.Task;
import com.llm.taskmanager.model.TaskRequest;
import com.llm.taskmanager.model.TaskResponse;
import com.llm.taskmanager.service.TaskService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api")
@Slf4j
public class TaskController {
    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @PostMapping("/projects")
    public ResponseEntity<Project> createProject(@Valid @RequestBody Project project) {
        return ResponseEntity.ok(taskService.createProject(project));
    }

    @GetMapping("/projects/{projectId}/tasks")
    public ResponseEntity<List<Task>> getTasksByProject(@PathVariable UUID projectId) {
        return ResponseEntity.ok(taskService.getTasksByProject(projectId));
    }

    @GetMapping("/projects/{projectId}/tasks/status/{status}")
    public ResponseEntity<List<Task>> getTasksByProjectAndStatus(
            @PathVariable UUID projectId,
            @PathVariable String status) {
        return ResponseEntity.ok(taskService.getTasksByProjectAndStatus(projectId, status));
    }

    @GetMapping("/projects/{projectId}/tasks/pending")
    public ResponseEntity<List<Task>> getPendingTasksByProject(@PathVariable UUID projectId) {
        return ResponseEntity.ok(taskService.getPendingTasksByProject(projectId));
    }

    @GetMapping("/tasks/{id}")
    public ResponseEntity<Task> getTask(@PathVariable UUID id) {
        return ResponseEntity.ok(taskService.getTask(id));
    }

    @PostMapping("/tasks")
    public ResponseEntity<TaskResponse> createTask(@Valid @RequestBody TaskRequest request) {
        Task task = Task.builder()
            .project(taskService.getProject(request.getProjectId()))
            .userId(request.getUserId())
            .taskType(request.getTaskType())
            .inputData(request.getInputData())
            .priority(request.getPriority() != null ? request.getPriority() : 1)
            .deadline(request.getDeadline())
            .parentTask(request.getParentTaskId() != null ? 
                taskService.getTask(request.getParentTaskId()) : null)
            .executionOrder(request.getExecutionOrder())
            .metadata(request.getMetadata())
            .build();

        Task createdTask = taskService.createTask(task);

        return ResponseEntity.ok(TaskResponse.builder()
                .taskId(createdTask.getId())
                .projectId(createdTask.getProject().getId())
                .taskType(createdTask.getTaskType())
                .status(createdTask.getStatus())
                .priority(createdTask.getPriority())
                .createdAt(createdTask.getCreatedAt())
                .startedAt(createdTask.getStartedAt())
                .completedAt(createdTask.getCompletedAt())
                .deadline(createdTask.getDeadline())
                .errorMessage(createdTask.getErrorMessage())
                .parentTaskId(createdTask.getParentTask() != null ? createdTask.getParentTask().getId() : null)
                .executionOrder(createdTask.getExecutionOrder())
                .inputData(createdTask.getInputData())
                .outputData(createdTask.getOutputData())
                .metadata(createdTask.getMetadata())
                .build());
    }

    @PutMapping("/tasks/{taskId}/status")
    public ResponseEntity<Task> updateTaskStatus(
            @PathVariable UUID taskId,
            @RequestParam String status,
            @RequestParam UUID changedBy,
            @RequestParam(required = false) String reason) {
        return ResponseEntity.ok(taskService.updateTaskStatus(taskId, status, changedBy, reason));
    }
}
