## 0.0.1e

### Added
- Added additional configuration validation.
- Added validation for administrator credentials.
- Added configuration sanity checks for database port and timeout.

### Changed
- Standardized startup logging across all startup scripts.
- Simplified `entrypoint.sh` to act only as the startup orchestrator.
- Moved detailed startup logging into the Python modules.
- Improved startup validation and error reporting.
- Confirmed repeat startup is fully idempotent.

### Fixed
- Removed duplicate startup messages.
- Fixed inconsistent logging between startup scripts.
- Improved first-run startup behavior.

## 0.0.1d

### Added
- Added `check_config.py` startup validation.
- Added `initialize_database.py` to automatically create the database and application user.
- Updated `entrypoint.sh` to use a staged startup process.
- Configuration validation now stops startup if `database.password` is still `CHANGE_ME`.

### Changed
- Startup now initializes the MariaDB database before performing the application connection test.
- Improved startup logging and script documentation.

### Notes
- Administrator credentials are temporarily stored in `config.yaml` for development and testing.
- A future release will move administrator credentials out of the configuration file after the initialization workflow is finalized.