# Evidence Processor

## Overview

Evidence Processor is a modular document processing system designed to organize large collections of documents into a searchable knowledge base.

The project is intended to work alongside **Document Extractor**. Document Extractor is responsible for extracting text and metadata from source documents, while Evidence Processor imports that data into a database and progressively builds additional layers of structured information.

The long-term goal is to transform unstructured documents into a searchable repository that supports timelines, research, reporting, legal analysis, and historical documentation.

---

## Project Goals

* Store extracted document text in a database.
* Preserve original document information.
* Break documents into logical segments.
* Build chronological timeline events.
* Extract people, organizations, locations, and topics.
* Generate reports and exports.
* Provide a searchable WebUI.
* Support future AI-assisted analysis without modifying original data.

---

## Design Philosophy

Evidence Processor is built around small, independent processing stages.

Each stage has a single responsibility.

Each stage can be tested independently.

Each stage should be able to run without requiring later stages.

Whenever possible, stages should never modify data created by earlier stages.

---

## Planned Processing Pipeline

1. Verify database connectivity.
2. Create or validate database schema.
3. Import extracted documents.
4. Classify document type.
5. Build document segments.
6. Generate timeline events.
7. Extract entities and topics.
8. Generate reports.
9. Provide WebUI access.
10. Support AI-assisted research and narrative generation.

---

## Data Preservation

Original extracted text is considered the source of truth.

Derived information such as summaries, timeline events, tags, and relationships should be reproducible and may be regenerated as AI models improve.

---

## Development Philosophy

* Keep modules small.
* Keep responsibilities isolated.
* Log every major operation.
* Design for recovery after interruption.
* Avoid duplicate processing.
* Prefer configuration over hardcoded values.
* Build one working stage before moving to the next.

---

## Project Status

This project is currently in the planning and architectural design phase.
Implementation will proceed incrementally, with each processing stage completed and verified before development continues to the next stage.
# evidence-processor
