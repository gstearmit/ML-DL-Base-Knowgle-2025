package com.llm.taskmanager.service;

import com.llm.taskmanager.model.Project;
import com.llm.taskmanager.model.Task;
import com.llm.taskmanager.model.TaskHistory;
import com.llm.taskmanager.repository.ProjectRepository;
import com.llm.taskmanager.repository.TaskRepository;
import com.llm.taskmanager.repository.TaskHistoryRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

@Service
@Slf4j
public class TaskService {
    private final ProjectRepository projectRepository;
    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final KafkaTemplate<String, Task> kafkaTemplate;

    public TaskService(
            ProjectRepository projectRepository,
            TaskRepository taskRepository,
            TaskHistoryRepository taskHistoryRepository,
            KafkaTemplate<String, Task> kafkaTemplate) {
        this.projectRepository = projectRepository;
        this.taskRepository = taskRepository;
        this.taskHistoryRepository = taskHistoryRepository;
        this.kafkaTemplate = kafkaTemplate;
    }

    public Project createProject(Project project) {
        project.setCreatedAt(ZonedDateTime.now());
        project.setUpdatedAt(ZonedDateTime.now());
        return projectRepository.save(project);
    }

    public Task createTask(Task task) {
        task.setCreatedAt(ZonedDateTime.now());
        task.setUpdatedAt(ZonedDateTime.now());
        task.setStatus("pending");
        Task savedTask = taskRepository.save(task);
        
        // Send task to Kafka for processing
        kafkaTemplate.send("tasks", savedTask);
        
        return savedTask;
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public List<Task> getTasksByProject(UUID projectId) {
        return taskRepository.findByProjectId(projectId);
    }

    public List<Task> getTasksByProjectAndStatus(UUID projectId, String status) {
        return taskRepository.findByProjectIdAndStatus(projectId, status);
    }

    public List<Task> getPendingTasksByProject(UUID projectId) {
        return taskRepository.findPendingTasksByProjectOrderByPriority(projectId);
    }

    public Project getProject(UUID id) {
        return projectRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Project not found"));
    }

    public Task getTask(UUID id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found"));
    }

    public Task updateTaskStatus(UUID taskId, String newStatus, UUID changedBy, String reason) {
        Task task = getTask(taskId);
        String oldStatus = task.getStatus();
        task.setStatus(newStatus);
        task.setUpdatedAt(ZonedDateTime.now());

        if (newStatus.equals("processing")) {
            task.setStartedAt(ZonedDateTime.now());
        } else if (newStatus.equals("completed") || newStatus.equals("failed")) {
            task.setCompletedAt(ZonedDateTime.now());
        }

        Task updatedTask = taskRepository.save(task);

        // Create task history entry
        TaskHistory history = new TaskHistory();
        history.setTask(task);
        history.setStatusFrom(oldStatus);
        history.setStatusTo(newStatus);
        history.setChangedBy(changedBy);
        history.setReason(reason);
        taskHistoryRepository.save(history);

        return updatedTask;
    }
}
