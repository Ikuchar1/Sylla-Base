# <COURSE> — Processing Log

Append-only. Newest at the bottom. Format: `## [YYYY-MM-DD] operation | description`

- `/process-notes` appends one entry per file, with its fingerprint
  (`git hash-object <file> | cut -c1-8`) after `@`. A file whose fingerprint no longer
  matches its newest entry has changed; it's re-ingested and logged as `update`.
  `## [YYYY-MM-DD] ingest | <file> @ <hash> → N pages created, M updated`
- `/lint-wiki` appends one entry per run:
  `## [YYYY-MM-DD] lint | N findings, M fixed`
