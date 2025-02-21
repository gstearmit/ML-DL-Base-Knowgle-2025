package com.llm.taskmanager.service;

import com.llm.taskmanager.model.Task;
import com.llm.taskmanager.repository.ProjectRepository;
import com.llm.taskmanager.repository.TaskRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

import java.time.LocalDateTime;
import java.util.UUID;

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
    private KafkaTemplate<String, Task> kafkaTemplate;

    private TaskService taskService;

    @BeforeEach
    void setUp() {
        taskService = new TaskService(projectRepository, taskRepository, kafkaTemplate);
    }

    @Test
    void createTask_ShouldSaveAndSendToKafka() {
        // Given
        Task task = new Task();
        task.setId(UUID.randomUUID());
        task.setInput("Test input");
        task.setModels(new String[]{"gpt-4"});
        task.setPriority(1);

        when(taskRepository.save(any(Task.class))).thenReturn(task);

        // When
        taskService.createTask(task);

        // Then
        verify(taskRepository).save(any(Task.class));
        verify(kafkaTemplate).send("tasks", task);
    }
} 