# Data Provenance — Agent Rule

Every data file, chart, or table committed to this repo MUST document its source.

## Requirements by file type

| Type | Requirement |
|------|-------------|
| Python scripts | Docstring with data source name, acquisition URL, and update instructions |
| Markdown tables | Inline footnote with source and retrieval date |
| External data (CSV, JSON) | Companion `.md` or `.txt` file with provenance |
| Mathematical simulations | Label "Pure mathematical model" and document all parameters |

## Reference example

See `articles/2026-quadruple-long-life/analysis/src/` — every script has a docstring following this format:

```python
"""
ChNN — Description

Data source: <name>
  Acquisition: <URL or method>
  Update: <how to refresh data>
"""
```

## Why

The repo is public. Readers must be able to verify and reproduce every number. If a data source link rots, the description should be enough to find an alternative.
