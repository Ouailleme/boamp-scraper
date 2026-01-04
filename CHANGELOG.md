# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial SDK structure with TenderScraper class
- Pydantic v2 models (Tender, TenderCategory, SearchFilters)
- Async and sync search support
- Mock data for testing (real BOAMP scraping TODO)
- 3 usage examples:
  - basic.py: Basic search
  - advanced_filters.py: Filtering by category and budget
  - export_csv.py: Export to CSV with timestamp
- Structured logging with timestamps
- 8 unit tests with pytest
- CONTRIBUTING.md with coding standards
- GitHub Actions CI/CD workflow
- Badges in README (Python version, License, GitHub stats, Code style)

### Changed
- README updated with complete usage examples
- Logging improved with detailed search parameters

### Fixed
- None yet

## [0.1.0] - 2026-01-04

### Added
- Initial release
- Basic BOAMP scraper functionality
- Mock data for testing
- Examples and documentation
- MIT License

[Unreleased]: https://github.com/Ouailleme/boamp-scraper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Ouailleme/boamp-scraper/releases/tag/v0.1.0

