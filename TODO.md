EvidenceProcessor TODO

[x] 00 - Project Setup
    [x] Create folder structure
    [x] Add README.md
    [x] Add TODO.md
    [x] Add docker-compose.yml
    [x] Add requirements.txt
    [x] Add Dockerfile
    [x] Add entrypoint.sh
    [x] Add VERSION file
    [x] Add release.sh

[x] 01 - Startup / MariaDB Foundation
    [x] Create common.py
    [x] Create logger.py
    [x] Create database.py
    [x] Create check_config.py
    [x] Create initialize_database.py
    [x] Create check_mariadb.py
    [x] Seed default config files into /data/config
    [x] Stop startup if database.password is still CHANGE_ME
    [x] Automatically create MariaDB database
    [x] Automatically create MariaDB application user
    [x] Verify application user can connect
    [x] Confirm repeat startup is idempotent

[x] 02 - Startup Cleanup
    [x] Remove duplicate print output
    [x] Standardize startup logging
    [x] Add startup summary banner
    [x] Decide how to handle/remove admin credentials after initialization
    [x] Add maintenance method to reset/remove test DB user if needed

[ ] 03 - Schema Creator
    [x] Create schema.py
    [x] Create create_schema.py
    [x] Create schema_version table
    [x] Create documents table
    [x] Create document_text table
    [x] Create document_segments table
    [x] Create timeline_events table

    [ ] Create people table
    [ ] Create organizations table
    [ ] Create topics table
    [ ] Create relationship tables
    [ ] Create processing_log table

    [ ] Create check_schema.py
    [ ] Verify schema version
    [ ] Verify required tables
    [ ] Verify required indexes
    [ ] Integrate check_schema.py into startup

[ ] 04 - Document Import
    [ ] Recursively scan import folder
    [ ] Detect supported file types
    [ ] Calculate SHA256
    [ ] Skip unchanged files
    [ ] Detect modified files
    [ ] Insert document metadata
    [ ] Record processing status

[ ] 05 - Text Extraction
    [ ] Extract text from PDF
    [ ] Extract text from TXT
    [ ] OCR image-only PDFs
    [ ] Store extracted text
    [ ] Record extraction method
    [ ] Record extraction errors

[ ] 06 - Document Classifier
    [ ] Classify each document
    [ ] Email Chain
    [ ] Single Email
    [ ] Memo
    [ ] Letter
    [ ] Form
    [ ] Policy
    [ ] Court Filing
    [ ] Medical Record
    [ ] Unknown

[ ] 07 - Segment Builder
    [ ] Email chains become multiple segments
    [ ] Memos become one segment
    [ ] Letters become one segment
    [ ] Forms become one segment
    [ ] Unknown documents become one review segment
    [ ] Store segment confidence
    [ ] Mark needs_review when uncertain

[ ] 08 - Timeline Builder
    [ ] Create one event from each segment
    [ ] Preserve date
    [ ] Preserve time
    [ ] Create factual event summary
    [ ] Link event to segment
    [ ] Link segment to document

[ ] 09 - Entity and Topic Extraction
    [ ] Extract people
    [ ] Extract organizations
    [ ] Extract locations
    [ ] Extract topics
    [ ] Link entities to documents
    [ ] Link entities to timeline events
    [ ] Link topics to timeline events

[ ] 10 - Reports / Export
    [ ] Date range report
    [ ] Person report
    [ ] Organization report
    [ ] Topic report
    [ ] Supporting documents report
    [ ] Review-needed report
    [ ] Export CSV
    [ ] Export XLSX

[ ] 11 - WebUI
    [ ] Dashboard
    [ ] Document search
    [ ] Timeline view
    [ ] Date range filter
    [ ] Person filter
    [ ] Organization filter
    [ ] Topic filter
    [ ] Source document view
    [ ] Export buttons

[ ] 12 - AI Narrative Tools
    [ ] Generate date-range explanation
    [ ] Generate case chronology
    [ ] Generate person summary
    [ ] Generate organization summary
    [ ] Generate topic summary
    [ ] Generate book chapter draft

[ ] 13 - Maintenance
    [ ] Backup database
    [ ] Restore database
    [ ] Reprocess selected document
    [ ] Rebuild derived tables
    [ ] Log processing errors
    [ ] Schema migrations
    [ ] Remove administrator credentials after initial database setup
    [ ] Support automatic database credential rotation