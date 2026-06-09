# Issue 5: Quality flags

## What to build

Detect and display four data quality flags on each column card: high null rate (>50%), constant column (only one distinct value), suspected ID column (cardinality ratio >95%), and numeric-as-string (object dtype but >90% of non-null values parse as numeric). Flags should be visually distinct from regular metrics — rendered as badges or highlighted labels.

## Acceptance criteria

- [ ] "High null rate" badge appears on columns where null rate > 50%
- [ ] "Constant column" badge appears on columns with exactly 1 unique value
- [ ] "Suspected ID" badge appears on columns where unique count / row count > 0.95
- [ ] "Numeric as string" badge appears on object-dtype columns where >90% of non-null values parse as numeric
- [ ] Flags are visually distinct from surrounding metrics (e.g. coloured badge/chip)
- [ ] Columns with no flags render cleanly with no empty badge area
- [ ] All four flags are independently testable with hand-crafted CSV fixtures

## Blocked by

- Issue 4: Per-column profiling
