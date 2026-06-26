EvidenceProcessor TODO

[ ] 00 - Project Setup
    [ ] Create folder structure
    [ ] Add README.md
    [ ] Add .env.example
    [ ] Add docker-compose.yml
    [ ] Add requirements.txt

[ ] 01 - MariaDB Connection Check
    [ ] Create check_mariadb.py
    [ ] Read DB settings from .env
    [ ] Run SELECT 1
    [ ] Exit cleanly on success
    [ ] Exit with error if DB unavailable

[ ] 02 - Schema Creator
    [ ] Create create_schema.py
    [ ] Create documents table
    [ ] Create document_text table
    [ ] Create document_segments table
    [ ] Create timeline_events table
    [ ] Create people table
    [ ] Create topics table
    [ ] Create relationship tables
    [ ] Create processing_log table

[ ] 03 - Document Loader
    [ ] Recursively scan TXT folder
    [ ] Calculate SHA256 for each TXT
    [ ] Skip unchanged files
    [ ] Detect changed files
    [ ] Insert document metadata
    [ ] Insert full extracted text
    [ ] Stop safely if MariaDB unavailable

[ ] 04 - Document Classifier
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

[ ] 05 - Segment Builder
    [ ] Email chains become multiple segments
    [ ] Memos become one segment
    [ ] Letters become one segment
    [ ] Forms become one segment
    [ ] Unknown documents become one review segment
    [ ] Store segment confidence
    [ ] Mark needs_review when uncertain

[ ] 06 - Timeline Builder
    [ ] Create one event from each segment
    [ ] Preserve date
    [ ] Preserve time
    [ ] Create short factual event summary
    [ ] Link event back to segment
    [ ] Link segment back to document

[ ] 07 - Entity and Topic Extraction
    [ ] Extract people
    [ ] Extract organizations
    [ ] Extract locations
    [ ] Extract topics
    [ ] Link entities to timeline events
    [ ] Link topics to timeline events

[ ] 08 - Reports / Export
    [ ] Date range report
    [ ] Person report
    [ ] Topic report
    [ ] Supporting documents report
    [ ] Review-needed report
    [ ] Export CSV
    [ ] Export XLSX

[ ] 09 - WebUI
    [ ] Dashboard
    [ ] Document search
    [ ] Timeline view
    [ ] Date range filter
    [ ] Person filter
    [ ] Topic filter
    [ ] Source document view
    [ ] Export buttons

[ ] 10 - AI Narrative Tools
    [ ] Generate date-range explanation
    [ ] Generate case chronology
    [ ] Generate person summary
    [ ] Generate topic summary
    [ ] Generate book chapter draft from selected date range

[ ] 11 - Maintenance
    [ ] Backup DB
    [ ] Restore DB
    [ ] Reprocess selected document
    [ ] Rebuild derived tables
    [ ] Log errors
    [ ] Version schema