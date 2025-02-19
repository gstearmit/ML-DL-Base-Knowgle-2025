@Workspace/
├── docker-compose.yml
├── .env
├── configs/
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   ├── keycloak/
│   │   └── realm-config.json
│   ├── kafka/
│   │   └── server.properties
│   ├── redis/
│   │   └── redis.conf
│   ├── postgresql/
│   │   └── postgresql.conf
│   └── prometheus/
│       └── prometheus.yml
├── k8s/
│   ├── 01-namespace.yaml
│   ├── 02-storage-class.yaml
│   ├── 03-persistent-volumes.yaml
│   ├── 04-secrets.yaml
│   ├── 05-configmaps.yaml
│   └── deployments/
│       ├── layer1-client-access/
│       ├── layer2-security/
│       ├── layer3-processing/
│       ├── layer4-orchestration/
│       ├── layer5-queue/
│       ├── layer6-resource/
│       ├── layer7-llm-engine/
│       ├── layer8-result/
│       ├── layer9-monitoring/
│       └── layer10-reliability/
└── scripts/
    ├── init-db.sh
    ├── setup-minio.sh
    └── health-check.sh