"""Prometheus metrics."""
from prometheus_client import Counter, Histogram, Gauge, Info

app_info = Info("medical_doc_processor", "Medical Document Processor info")
app_info.info({"version": "0.1.0"})

http_requests_total = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
http_request_duration_seconds = Histogram("http_request_duration_seconds", "HTTP latency", ["method", "endpoint"])

documents_processed_total = Counter("documents_processed_total", "Documents processed", ["status"])
entities_extracted_total = Counter("entities_extracted_total", "Entities extracted", ["entity_type"])
validation_checks_total = Counter("validation_checks_total", "Validations performed", ["result"])
fhir_exports_total = Counter("fhir_exports_total", "FHIR exports")

extraction_latency_seconds = Histogram("extraction_latency_seconds", "NER extraction latency", buckets=[0.5, 1, 2, 5, 10, 30])
validation_latency_seconds = Histogram("validation_latency_seconds", "Validation latency", buckets=[0.1, 0.5, 1, 2, 5, 10])

active_documents = Gauge("active_documents", "Active documents")