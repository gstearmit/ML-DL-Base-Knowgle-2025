from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram("Microservice Architecture on AWS", show=False):
    internet = User("Internet")

    with Cluster("AWS Region"):
        route53 = Route53("DNS")

        with Cluster("VPC"):
            elb = ELB("Load Balancer")

            with Cluster("Availability Zone 1"):
                with Cluster("Document Processing"):
                    doc_process_instances = [EC2("Instance 1"), EC2("Instance 2")]
                    doc_process_python = Python("Python Script (FastAPI + Celery)")
                    tesseract = EC2("Tesseract OCR")
                    nifi = EC2("Apache NiFi")
                s3_doc = S3("Document Storage")

            with Cluster("Availability Zone 2"):
                with Cluster("AI Core"):
                    ai_core_instances = [EC2("Instance 1"), EC2("Instance 2")]
                    ai_core_python = Python("Python Script (FastAPI)")

            with Cluster("Vector Database"):
                vector_db = RDS("Pinecone / Weaviate")

            with Cluster("Message Queue"):
                kafka = Kafka("Kafka Cluster")

            with Cluster("Output Generation"):
                output_gen_instances = [EC2("Instance 1"), EC2("Instance 2")]
                output_gen_python = Python("Python Script (FastAPI)")

            with Cluster("Backend"):
              api_gateway = EC2("API Gateway (Nginx)")

    internet >> route53
    route53 >> elb

    elb >> doc_process_instances
    elb >> ai_core_instances
    elb >> output_gen_instances
    elb >> api_gateway # Thêm API Gateway vào Load Balancer

    doc_process_instances >> s3_doc
    doc_process_instances >> doc_process_python
    doc_process_instances >> nifi #Document process sử dụng nifi
    doc_process_python >> tesseract

    doc_process_python >> kafka
    nifi >> kafka

    kafka >> ai_core_instances

    ai_core_instances >> ai_core_python
    ai_core_python >> vector_db

    vector_db >> ai_core_python #AI core đọc từ vector DB
    ai_core_instances >> kafka #AI core publish message queue
    # ai_core_instances >> output_gen_instances

    output_gen_instances >> output_gen_python

    # Kết nối API Gateway tới các microservice
    api_gateway >> doc_process_instances
    api_gateway >> ai_core_instances
    api_gateway >> output_gen_instances