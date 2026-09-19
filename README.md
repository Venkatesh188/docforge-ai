# DocForge-AI

[![PyPI version](https://badge.fury.io/py/docforge-ai.svg)](https://pypi.org/project/docforge-ai/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-powered documentation generator that transforms project ideas into professional software documentation using multi-agent orchestration.**

## Problem

Writing comprehensive software documentation (PRDs, architecture docs, test specs) is time-consuming and often inconsistent. Teams spend weeks producing documents that follow different formats and miss critical sections.

## Who This Is For

- **Developers** who need to quickly scaffold professional documentation for new projects
- **Technical leads** standardizing documentation across teams
- **Startups** preparing investor-ready technical documentation
- **Anyone** who wants enterprise-grade docs without the enterprise timeline

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DocForge CLI                             │
├─────────────────────────────────────────────────────────────────┤
│                    DocForge Core Orchestrator                   │
├──────────────────┬──────────────────┬───────────────────────────┤
│  CrewAI Agents   │  Local Storage   │    Prompt Templates       │
│  (10 Specialized │  (JSON + MD)     │    (10 Doc Types)         │
│   Roles)         │                  │                           │
├──────────────────┴──────────────────┴───────────────────────────┤
│                      OpenAI API (GPT-4)                         │
└─────────────────────────────────────────────────────────────────┘
```

**Key design decisions:**
- **Multi-agent system**: Each document type has a specialized CrewAI agent (Senior Program Manager for charters, Lead Solution Architect for SRS, etc.)
- **PRD-first workflow**: Generate requirements first, validate, then expand to other docs
- **Self-contained**: No database dependencies—uses local file storage
- **Template-driven**: Customizable prompts in `prompts/` directory

## Quick Start

### Install

```bash
pip install docforge-ai
```

### Configure

```bash
docforge-ai init
# Edit .env with your OpenAI API key
```

### Generate

```bash
# Generate a PRD (recommended starting point)
docforge-ai generate "AI-powered chatbot for customer service" --docs srs

# Review, then generate additional docs
docforge-ai continue ai-powered-chatbot-for-customer-service ARCH TEST DEPLOY
```

### Output

Documents are saved to `generated-docs/<project-name>/`:
```
generated-docs/ai-powered-chatbot/
├── README.md
├── 01_srs.md              # Software Requirements Specification
├── 02_architecture.md     # System Architecture
├── 03_test_specification.md
└── 04_deployment_guide.md
```

## Supported Document Types

| Type | Alias | Agent Role |
|------|-------|------------|
| Software Requirements | `srs`, `prd` | Lead Solution Architect |
| System Architecture | `arch`, `hld` | Principal Systems Architect |
| Low-Level Design | `lld`, `design` | Senior Software Architect |
| Test Specification | `test` | QA Lead |
| Deployment Guide | `deploy` | DevOps Lead |
| Operations Manual | `ops` | Operations Manager |
| Project Charter | `charter` | Senior Program Manager |
| Business Case | `business` | Business Analyst |
| Market Requirements | `market` | Product Manager |
| Vision Brief | `vision` | Product Strategist |

## Demo

[![DocForge-AI Demo](https://img.youtube.com/vi/LMP-9WBePdY/0.jpg)](https://youtu.be/LMP-9WBePdY)

**Manual demo path:**
1. `pip install docforge-ai`
2. `docforge-ai init` → add your OpenAI API key to `.env`
3. `docforge-ai generate "E-commerce platform for handmade crafts" --docs srs`
4. Open `generated-docs/e-commerce-platform/01_srs.md`

## Development

```bash
git clone https://github.com/Venkatesh188/docforge-ai.git
cd docforge-ai
pip install -e ".[dev]"
pytest
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Required | — |
| `OPENAI_MODEL` | Model to use | `gpt-4o-mini` |
| `DOCFORGE_GENERATED_DOCS_PATH` | Output directory | `generated-docs` |

See `.env.template` for all options.

## Attribution

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) for multi-agent orchestration
- Powered by [OpenAI](https://openai.com/) for content generation

## License

MIT — see [LICENSE](LICENSE)
