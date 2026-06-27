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

[ ] 02 - Startup Cleanup
    [ ] Remove duplicate print output
    [ ] Standardize startup logging
    [ ] Add startup summary banner
    [ ] Decide how to handle/remove admin credentials after initialization
    [ ] Add maintenance method to reset/remove test DB user if needed

[ ] 03 - Schema Creator
    [ ] Create create_schema.py
    [ ] Create documents table
    [ ] Create document_text table
    [ ] Create document_segments table
    [ ] Create timeline_events table
    [ ] Create people table
    [ ] Create topics table
    [ ] Create relationship tables
    [ ] Create processing_log table
    [ ] Add schema version tracking

[ ] 04 - Document Loader
    [ ] Recursively scan TXT folder
    [ ] Calculate SHA256 for each TXT
    [ ] Skip unchanged files
    [ ] Detect changed files
    [ ] Insert document metadata
    [ ] Insert full extracted text
    [ ] Stop safely if MariaDB unavailable

[ ] 05 - Document Classifier
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

[ ] 06 - Segment Builder
    [ ] Email chains become multiple segments
    [ ] Memos become one segment
    [ ] Letters become one segment
    [ ] Forms become one segment
    [ ] Unknown documents become one review segment
    [ ] Store segment confidence
    [ ] Mark needs_review when uncertain

[ ] 07 - Timeline Builder
    [ ] Create one event from each segment
    [ ] Preserve date
    [ ] Preserve time
    [ ] Create short factual event summary
    [ ] Link event back to segment
    [ ] Link segment back to document

[ ] 08 - Entity and Topic Extraction
    [ ] Extract people
    [ ] Extract organizations
    [ ] Extract locations
    [ ] Extract topics
    [ ] Link entities to timeline events
    [ ] Link topics to timeline events

[ ] 09 - Reports / Export
    [ ] Date range report
    [ ] Person report
    [ ] Topic report
    [ ] Supporting documents report
    [ ] Review-needed report
    [ ] Export CSV
    [ ] Export XLSX

[ ] 10 - WebUI
    [ ] Dashboard
    [ ] Document search
    [ ] Timeline view
    [ ] Date range filter
    [ ] Person filter
    [ ] Topic filter
    [ ] Source document view
    [ ] Export buttons

[ ] 11 - AI Narrative Tools
    [ ] Generate date-range explanation
    [ ] Generate case chronology
    [ ] Generate person summary
    [ ] Generate topic summary
    [ ] Generate book chapter draft from selected date range

[ ] 12 - Maintenance
    [ ] Backup DB
    [ ] Restore DB
    [ ] Reprocess selected document
    [ ] Rebuild derived tables
    [ ] Log errors
    [ ] Version schema