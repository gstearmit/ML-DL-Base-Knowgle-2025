from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache
from diagrams.aws.network import Route53

with Diagram("Microservice Architecture", show=False):
    dns = Route53("User Interface")
    
    with Cluster("Processing Cluster"):
        ai_models = [ECS("GPT-4"), ECS("Claude"), ECS("Gemini")]
        queue = ElastiCache("Task Queue")
        
    vector_db = ElastiCache("VectorDB")
    
    dns >> ai_models >> queue >> vector_db