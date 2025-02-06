from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.queue import Kafka
from diagrams.aws.compute import EC2
from diagrams.onprem.client import User

with Diagram("System Architecture Design (Microservice Architecture)", show=False):
    user = User("Người dùng")

    with Cluster("Task Management"):
        task_manager = Python("Task Manager\n(DeepSeek R1)")

    with Cluster("Tài khoản LLM"):
        account_manager = Python("Account Manager")

    kafka = Kafka("Kafka Broker")

    with Cluster("LLM Workers"):
        with Cluster("OpenAI"):
            openai_worker = EC2("OpenAI Worker")
        with Cluster("Gemini"):
            gemini_worker = EC2("Gemini Worker")
        with Cluster("Claude"):
            claude_worker = EC2("Claude Worker")
        with Cluster("DeepSeek"):
            deepseek_worker = EC2("DeepSeek Worker")
        with Cluster("Qwen-2.5"):
            qwen_worker = EC2("Qwen Worker")

    with Cluster("Kết quả"):
        result_aggregator = Python("Result Aggregator")
        evaluator = Python("Evaluator\n(DeepSeek R1)")

    user >> task_manager
    task_manager >> account_manager
    task_manager >> kafka
    account_manager >> kafka

    kafka >> openai_worker
    kafka >> gemini_worker
    kafka >> claude_worker
    kafka >> deepseek_worker
    kafka >> qwen_worker

    openai_worker >> result_aggregator
    gemini_worker >> result_aggregator
    claude_worker >> result_aggregator
    deepseek_worker >> result_aggregator
    qwen_worker >> result_aggregator

    result_aggregator >> evaluator
    evaluator >> user