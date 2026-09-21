# AI Enablement - Claude Code kickoff

A static HTML presentation for the Palo Alto 2026 hackathon kickoff. The material covers AI adoption levels, agentic system architecture, Claude Code, hallucinations, guardrails, SDLC, team collaboration, FinOps, quality regressions, and failure analysis.

## Open the presentation

No web server is required. Open `index.html` directly in a browser.

Controls:

- `→`, `Space`, `PageDown` - next slide
- `←`, `PageUp` - previous slide
- `Home`, `End` - first or last slide
- `O` - overview of all slides
- `F` - full screen
- `?` - help

The URL may include a slide number, for example `index.html#/18`.

## Print or export to PDF

Use the browser print dialog and select landscape orientation. The print stylesheet places each slide on a separate 16:9 page.

## Scope

The deck is an introduction and contains no exercises. Its modular structure allows the presenter to skip a complete section without breaking the narrative. Current sources and caveats are listed in `SOURCES.md`.

Polish presenter notes are available as [`SCENARIUSZ.md`](SCENARIUSZ.md) and as a print-ready A4 PDF: [`output/pdf/SCENARIUSZ.pdf`](output/pdf/SCENARIUSZ.pdf).

## Validation

```bash
npm test
```

The script checks slide structure, metadata, and references to local files.

To regenerate the printable presenter script, run `scripts/generate_scenario_pdf.py` with a Python environment that includes ReportLab.
