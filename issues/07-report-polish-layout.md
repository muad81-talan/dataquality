# Issue 7: Report polish & layout

## What to build

Unify the report into a cohesive, readable page: summary section at the top, per-column cards with consistent layout, quality flag badges visually prominent, charts and metrics well-spaced, and the upload form accessible again (e.g. "Analyze another file" button). The goal is a report a data engineer would be comfortable sharing as a screenshot or screen share.

## Acceptance criteria

- [ ] Summary section (dataset metrics) appears at the top of the report, above column cards
- [ ] Each column card has a consistent structure: name + type header, metrics, flags, chart
- [ ] Quality flag badges are visually distinct and immediately noticeable (color, position)
- [ ] An "Analyze another file" button or link returns the user to the upload form
- [ ] Report is readable on a standard laptop screen without horizontal scrolling
- [ ] Long column lists (50+ columns) do not break the layout
- [ ] The page is usable without any external CSS or JS CDN (fully self-contained)

## Blocked by

- Issue 5: Quality flags
- Issue 6: Visualizations
