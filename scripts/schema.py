#!/usr/bin/env python3
"""
==============================================================================
Evidence Processor

File:
    schema.py

Purpose:
    Define the Evidence Processor application database schema.

Responsibilities:
    - Define the current schema version.
    - Create application tables.
    - Create application indexes.
    - Record the installed schema version.

This script should not:
    - Load config.yaml.
    - Open database connections.
    - Create databases.
    - Create users.
    - Process documents.
==============================================================================
"""

CURRENT_SCHEMA_VERSION = 1


def create_schema_version_table(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_version (
            id INT NOT NULL PRIMARY KEY,
            version INT NOT NULL,
            installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def create_documents_table(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            original_filename VARCHAR(512) NOT NULL,
            stored_filename VARCHAR(512) DEFAULT NULL,
            file_path TEXT DEFAULT NULL,
            file_type VARCHAR(100) DEFAULT NULL,
            file_hash_sha256 CHAR(64) DEFAULT NULL,
            source VARCHAR(255) DEFAULT NULL,
            notes TEXT DEFAULT NULL,
            imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def create_document_text_table(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_text (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            document_id BIGINT UNSIGNED NOT NULL,
            extraction_method VARCHAR(100) DEFAULT NULL,
            full_text LONGTEXT NOT NULL,
            extracted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,

            CONSTRAINT fk_document_text_document
                FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def create_document_segments_table(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_segments (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            document_id BIGINT UNSIGNED NOT NULL,
            segment_number INT UNSIGNED NOT NULL,
            page_number INT UNSIGNED DEFAULT NULL,
            segment_type VARCHAR(100) DEFAULT NULL,
            segment_text LONGTEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,

            CONSTRAINT fk_document_segments_document
                FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def create_timeline_events_table(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS timeline_events (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            document_id BIGINT UNSIGNED DEFAULT NULL,
            segment_id BIGINT UNSIGNED DEFAULT NULL,
            event_date DATE DEFAULT NULL,
            event_datetime DATETIME DEFAULT NULL,
            event_title VARCHAR(512) DEFAULT NULL,
            event_description LONGTEXT NOT NULL,
            event_source_text LONGTEXT DEFAULT NULL,
            confidence_score DECIMAL(5,2) DEFAULT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,

            CONSTRAINT fk_timeline_events_document
                FOREIGN KEY (document_id)
                REFERENCES documents(id)
                ON DELETE SET NULL,

            CONSTRAINT fk_timeline_events_segment
                FOREIGN KEY (segment_id)
                REFERENCES document_segments(id)
                ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def create_indexes(cursor) -> None:
    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents (file_hash_sha256);",
        "CREATE INDEX IF NOT EXISTS idx_documents_imported_at ON documents (imported_at);",
        "CREATE INDEX IF NOT EXISTS idx_document_text_document_id ON document_text (document_id);",
        "CREATE INDEX IF NOT EXISTS idx_document_segments_document_id ON document_segments (document_id);",
        "CREATE INDEX IF NOT EXISTS idx_document_segments_page_number ON document_segments (page_number);",
        "CREATE INDEX IF NOT EXISTS idx_timeline_events_document_id ON timeline_events (document_id);",
        "CREATE INDEX IF NOT EXISTS idx_timeline_events_segment_id ON timeline_events (segment_id);",
        "CREATE INDEX IF NOT EXISTS idx_timeline_events_event_date ON timeline_events (event_date);",
    ]

    for statement in index_statements:
        cursor.execute(statement)


def set_schema_version(cursor) -> None:
    cursor.execute(
        """
        INSERT INTO schema_version (id, version)
        VALUES (1, %s)
        ON DUPLICATE KEY UPDATE
            version = VALUES(version),
            updated_at = CURRENT_TIMESTAMP;
        """,
        (CURRENT_SCHEMA_VERSION,),
    )


def get_schema_version(cursor):
    cursor.execute(
        """
        SELECT version
        FROM schema_version
        WHERE id = 1;
        """
    )

    result = cursor.fetchone()

    if not result:
        return None

    return result.get("version")


def create_schema(cursor) -> None:
    create_schema_version_table(cursor)
    create_documents_table(cursor)
    create_document_text_table(cursor)
    create_document_segments_table(cursor)
    create_timeline_events_table(cursor)
    create_indexes(cursor)
    set_schema_version(cursor)