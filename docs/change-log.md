# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.3.18] - 2023-03-20

### Added

- Add ability to construct IList from generator

### Changed

### Fixed

## [0.3.17] - 2023-03-17

### Added

### Changed

- Added `IList` to the list of exports of the `funml` package

### Fixed

## [0.3.16] - 2023-03-02

### Added

- Add the `get_annotations` class method to records so as to hide the potentially unevaluated `__annotations__`

### Changed

### Fixed

## [0.3.15] - 2023-02-27

### Added

- Add __repr__ to data types of Record, Enum and IList

### Changed

### Fixed

- Fix incomplete json parsing of records due to nested typing.ForwardRefs in field annotations.

## [0.3.14] - 2023-02-27

### Added

### Changed

### Fixed

- Fixed incompatible JSON error produced wit to_json on enums that have no associated data or whose data is `str`

## [0.3.13] - 2023-02-25

### Added

- Added `to_json` and `from_json` builtin expressions

### Changed

- Changed `IList` to a generic subscriptable type just like `List` e.g. `IList[str]`

### Fixed

- Fixed how records load lazy annotations

## [0.3.12] - 2023-02-23

### Added

### Changed

### Fixed

- Fix TypeError: isinstance() arg 2 must be a type or tuple of types when records have Enum fields

## [0.3.11] - 2023-02-21

### Added

### Changed

### Fixed

- Fix TypeError: isinstance() argument 2 cannot be a parameterized generic in python 3.11

## [0.3.10] - 2023-02-16

### Added

### Changed

### Fixed

- Fix TypeError in records: isinstance() argument cannot be a parameterized generic

## [0.3.9] - 2023-02-16

### Added

- Extend types in record to handle "..." and "bool | None" etc.

### Changed

### Fixed

## [0.3.8] - 2023-02-15

### Added

- Expose the `Record` type on the root `funml` package

### Changed

### Fixed

## [0.3.7] - 2023-02-15

### Added

- Add `to_dict` to convert a record into a dictionary

### Changed

### Fixed

## [0.3.6] - 2023-02-15

### Added

### Changed

- Records can have fields with subscripted builtin types like `list[str]` thanks to `from __future__ import annotations`.
- Records can define default values

### Fixed

## [0.3.5] - 2023-02-13

### Added

### Changed

- Remove typings of `Expression`, `Pipeline` and `Operation`.

### Fixed

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
