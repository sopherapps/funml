# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.2.0] - 2023-01-28

### Added

- Result helpers: `if_ok`, `if_err`, `is_ok`, `is_err`.
- Option helpers: `if_some`, `if_none`, `is_some`, `is_none`.
- Sequence helpers: `imap`, `ifilter`, `ireduce`.

### Changed

- Changed creation of records to use classes decorated with `record`.
- Changed creation of enums to use classes subclassed from `funml.Enum`.
- Removed `map` and `filter` methods of `IList`.

### Fixed

- Fixed equality check of Result.ERR as originally Result.ERR(TypeError()) was not equal to Result.ERR(TypeError()).

## [0.0.1] - 2023-01-26

### Added

- Initial release
- pattern matching
- piping 
- immutable lists, enums, and records
- `Option` for handling potentially-None data
- `Result` to return from procedures that may raise an exception
- mkdocs documentation

### Changed

### Fixed
