package com.llm.taskmanager.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.llm.taskmanager.model.Project;
import com.llm.taskmanager.model.Task;
import com.llm.taskmanager.model.TaskHistory;
import com.llm.taskmanager.repository.ProjectRepository;
import com.llm.taskmanager.repository.TaskRepository;
import com.llm.taskmanager.repository.TaskHistoryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

import java.time.ZonedDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private ProjectRepository projectRepository;

    @Mock
    private TaskRepository taskRepository;

    @Mock
    private TaskHistoryRepository taskHistoryRepository;

    @Mock
    private KafkaTemplate<String, Task> kafkaTemplate;

    private TaskService taskService;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        taskService = new TaskService(projectRepository, taskRepository, taskHistoryRepository, kafkaTemplate);
        objectMapper = new ObjectMapper();
    }

    @Test
    void createTask_ShouldSaveAndSendToKafka() throws Exception {
        // Given
        Project project = new Project();
        project.setId(UUID.randomUUID());
        project.setName("Test Project");

        JsonNode inputData = objectMapper.readTree("{\"prompt\": \"Test input\"}");
        JsonNode metadata = objectMapper.readTree("{\"priority\": \"high\"}");

        Task task = new Task();
        task.setId(UUID.randomUUID());
        task.setProject(project);
        task.setUserId(UUID.randomUUID());
        task.setTaskType("TEST");
        task.setInputData(inputData);
        task.setPriority(1);
        task.setMetadata(metadata);

        when(taskRepository.save(any(Task.class))).thenReturn(task);

        // When
        taskService.createTask(task);

        // Then
        verify(taskRepository).save(any(Task.class));
        verify(kafkaTemplate).send("tasks", task);
    }

    @Test
    void updateTaskStatus_ShouldUpdateStatusAndCreateHistory() {
        // Given
        UUID taskId = UUID.randomUUID();
        UUID changedBy = UUID.randomUUID();
        Task task = new Task();
        task.setId(taskId);
        task.setStatus("pending");

        when(taskRepository.findById(taskId)).thenReturn(java.util.Optional.of(task));
        when(taskRepository.save(any(Task.class))).thenReturn(task);
        when(taskHistoryRepository.save(any(TaskHistory.class))).thenReturn(new TaskHistory());

        // When
        taskService.updateTaskStatus(taskId, "processing", changedBy, "Starting processing");

        // Then
        verify(taskRepository).save(any(Task.class));
        verify(taskHistoryRepository).save(any(TaskHistory.class));
    }

    @Test
    void getTasksByProject_ShouldReturnTasksList() {
        // Given
        UUID projectId = UUID.randomUUID();
        List<Task> expectedTasks = Arrays.asList(new Task(), new Task());

        when(taskRepository.findByProjectId(projectId)).thenReturn(expectedTasks);

        // When
        List<Task> actualTasks = taskService.getTasksByProject(projectId);

        // Then
        assertEquals(expectedTasks.size(), actualTasks.size());
        verify(taskRepository).findByProjectId(projectId);
    }

    @Test
    void getPendingTasksByProject_ShouldReturnPendingTasks() {
        // Given
        UUID projectId = UUID.randomUUID();
        List<Task> expectedTasks = Arrays.asList(new Task(), new Task());

        when(taskRepository.findPendingTasksByProjectOrderByPriority(projectId)).thenReturn(expectedTasks);

        // When
        List<Task> actualTasks = taskService.getPendingTasksByProject(projectId);

        // Then
        assertEquals(expectedTasks.size(), actualTasks.size());
        verify(taskRepository).findPendingTasksByProjectOrderByPriority(projectId);
    }
}
