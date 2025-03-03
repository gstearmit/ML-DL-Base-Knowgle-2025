III. Object Storage (MinIO)

MinIO/S3 được sử dụng để lưu trữ các tệp gốc, tệp đã xử lý, và kết quả trực quan hóa.

### 1. Cấu Trúc Bucket và Tổ Chức

```
documentai/
├── raw-documents/                # Tài liệu gốc người dùng tải lên
│   └── {user_id}/
│       └── {document_id}/
│           └── original.{ext}
├── processed-documents/          # Tài liệu đã xử lý
│   └── {user_id}/
│       └── {document_id}/
│           ├── extracted_text.txt
│           ├── metadata.json
│           └── chunks/
│               ├── chunk_0.txt
│               ├── chunk_1.txt
│               └── ...
├── visualizations/               # Kết quả trực quan hóa
│   └── {user_id}/
│       └── {visualization_id}/
│           ├── diagram.svg
│           ├── diagram.png
│           └── metadata.json
└── exports/                      # Kết quả chuẩn hóa
    └── {user_id}/
        └── {export_id}/
            ├── agile_stories.docx
            ├── jira_export.json
            └── gantt_chart.pdf
```

### 2. Quản Lý Vòng Đời Object

```python
# Ví dụ về chính sách vòng đời object trong MinIO
lifecycle_config = {
    "Rules": [
        {
            "ID": "delete-old-temp-files",
            "Status": "Enabled",
            "Filter": {
                "Prefix": "temp/"
            },
            "Expiration": {
                "Days": 1
            }
        },
        {
            "ID": "archive-old-documents",
            "Status": "Enabled",
            "Filter": {
                "Prefix": "raw-documents/"
            },
            "Transition": {
                "Days": 90,
                "StorageClass": "GLACIER"
            }
        }
    ]
}
```