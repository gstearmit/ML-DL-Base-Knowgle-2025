package com.llm.taskmanager.service;

import com.llm.taskmanager.model.Project;
import com.llm.taskmanager.model.Task;
import com.llm.taskmanager.repository.ProjectRepository;
import com.llm.taskmanager.repository.TaskRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@Slf4j
public class TaskService {
    private final ProjectRepository projectRepository;
    private final TaskRepository taskRepository;
    private final KafkaTemplate<String, Task> kafkaTemplate;

    public TaskService(ProjectRepository projectRepository, TaskRepository taskRepository, KafkaTemplate<String, Task> kafkaTemplate) {
        this.projectRepository = projectRepository;
        this.taskRepository = taskRepository;
        this.kafkaTemplate = kafkaTemplate;
    }

    public Project createProject(Project project) {
        project.setCreatedAt(LocalDateTime.now());
        project.setUpdatedAt(LocalDateTime.now());
        return projectRepository.save(project);
    }

    public Task createTask(Task task) {
        task.setCreatedAt(LocalDateTime.now());
        task.setStatus("PENDING");
        Task savedTask = taskRepository.save(task);
        
        // Send task to Kafka for processing
        kafkaTemplate.send("tasks", savedTask);
        
        return savedTask;
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public Task getTask(UUID id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found"));
    }
} 