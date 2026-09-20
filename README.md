# Medical Document Processor

[![CI](https://github.com/Shamanchi/medical-doc-processor/actions/workflows/ci.yml/badge.svg)](https://github.com/Shamanchi/medical-doc-processor/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/r/shamanchi/medical-doc-processor)
[![License: Shamanchi](https://img.shields.io/badge/License-Shamanchi-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

**Процессор медицинских документов** — извлечение структурированных данных из медицинских документов (назначения, выписки, лабораторные результаты) с валидацией по клиническим стандартам.

> **Источник темы**: `Hands-On-AI-Engineering / P-103 (medical_prescription_digitizer), P-152 (medical_document_parser)` → портфолио `medical-doc-processor`

---

## 🎯 Задача

- Парсинг медицинских PDF/сканов (рецепты, выписки, анализы)
- Извлечение сущностей: лекарства, дозировки, диагнозы, коды МКБ-10, ЛПУ, врачи
- Нормализация по справочникам (АТХ, МКБ-10, НЛС)
- Валидация дозировок, взаимодействий, противопоказаний
- Экспорт в FHIR / HL7 / JSON для интеграции с МИС/ЭМК

---

## 🏗 Архитектура

```mermaid
flowchart TD
    A[Медицинский документ] --> B[OCR / PDF Parser]
    B --> C[Medical NER (BioBERT / spaCy)]
    C --> D[Entity Linking (АТХ, МКБ-10, НЛС)]
    D --> E[Валидация: дозировки, взаимодействия]
    E --> F[Нормализация в FHIR/JSON]
    F --> G[Отчёт + флаги рисков]
```

**Слои:**
- `api/` — `/documents` (upload), `/extract` (извлечение), `/validate` (проверка), `/fhir` (экспорт)
- `services/` — `parser`, `ner`, `linker`, `validator`, `fhir_exporter`
- `core/` — `config`, `logging`, `exceptions`, `metrics`, `terminology` (АТХ/МКБ/НЛС кэш)

---

## 🚀 Quickstart

```bash
git clone https://github.com/Shamanchi/medical-doc-processor.git
cd medical-doc-processor
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload

# Docker
docker compose up --build
```

---

## 📦 API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/documents` | Загрузить медицинский документ |
| `POST` | `/api/v1/extract` | Извлечь сущности |
| `POST` | `/api/v1/validate` | Валидировать назначения |
| `POST` | `/api/v1/fhir` | Экспорт в FHIR Bundle |
| `GET` | `/api/v1/health` | Health-check |

---

## ⚙️ Конфигурация (`.env`)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `OPENAI_API_KEY` | Ключ OpenAI | — |
| `MEDICAL_NER_MODEL` | Модель NER | `d4data/biomedical-ner-all` |
| `TERMINOLOGY_CACHE_TTL` | TTL кэша терминологии (сек) | `86400` |
| `VALIDATION_STRICT` | Строгая валидация | `true` |

---

## 🧪 Тесты

```bash
pytest tests/unit -v
pytest tests/integration -v -m integration
```

---

## 🐳 Docker

```bash
docker compose up --build -d
```

---

## 📄 Лицензия

Лицензия Shamanchi 1.0 (source-available) — см. [LICENSE](LICENSE).
---

## 📞 Контакты

- Telegram: @PavelYrevichh
- Email: Lietman46@mail.ru
- GitHub: Shamanchi
- FL.ru: https://www.fl.ru/users/Shamanchi