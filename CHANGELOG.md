# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.3.4] - 2023-02-10

### Added

### Changed

- Changed typings of `Expression`, `Pipeline` and `Operation` to be subscriptable like `Callable` is.

### Fixed

## [0.3.3] - 2023-02-09

### Added

- Add ability to curry functions i.e. transform functions with multiple args into functions with fewer args

### Changed

### Fixed

## [0.3.2] - 2023-02-08

### Added

### Changed

- Signature of `__rshift__` for `Pipeline` and `Expression` returns either a `Pipeline` or `Any` result of executing the
  pipeline.

### Fixed

## [0.3.1] - 2023-02-07

### Added

- Added `AsyncPipeline` to handle the pipelines that have asynchronous routines

### Changed

### Fixed

## [0.3.0] - 2023-01-30

### Added

- Added `Pipeline`'s to move all piping to them

### Changed

- Removed `Context`
- Removed `let` and `Assignment`'s as these had side effects

### Fixed

- Made expressions pure to avoid unexpected outcomes.

## [0.2.0] - 2023-01-28

### Added

- Result helpers: `if_ok`, `if_err`, `is_ok`, `is_err`.
- Option helpers: `if_some`, `if_none`, `is_some`, `is_none`.
- Sequence helpers: `imap`, `ifilter`, `ireduce`.
- Pipeline helper: `funml.execute()`.

### Changed

- Changed creation of records to use classes decorated with `record`
- Changed creation of enums to use classes subclassed from `funml.Enum`
- Removed `map` and `filter` methods of `IList`

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

### Changed

### Fixed
