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