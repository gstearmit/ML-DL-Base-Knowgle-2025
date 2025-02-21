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

    @GetMapping("/tasks")
    public ResponseEntity<List<Task>> getAllTasks() {
        return ResponseEntity.ok(taskService.getAllTasks());
    }

    @GetMapping("/tasks/{id}")
    public ResponseEntity<Task> getTask(@PathVariable UUID id) {
        return ResponseEntity.ok(taskService.getTask(id));
    }

    @PostMapping("/tasks")
    public ResponseEntity<TaskResponse> createTask(@Valid @RequestBody TaskRequest request) {
        Task task = new Task();
        task.setInput(request.getInput());
        task.setModels(request.getModels());
        task.setPriority(request.getPriority());

        Task createdTask = taskService.createTask(task);

        return ResponseEntity.ok(TaskResponse.builder()
                .taskId(createdTask.getId())
                .status(createdTask.getStatus())
                .createdAt(createdTask.getCreatedAt())
                .build());
    }
} 