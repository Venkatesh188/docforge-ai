# Portfolio: DocForge-AI

**Interview talking points for Applied AI / GenAI roles**

---

## 1. Problem Statement

**What problem does this solve?**

Software documentation is a bottleneck. Teams spend weeks writing PRDs, architecture docs, and test specs—often inconsistently. Documents miss critical sections, follow different formats, and quickly become outdated.

**Why does this matter?**

Poor documentation leads to misaligned teams, scope creep, and technical debt. Enterprise companies spend significant resources on technical writing that could be standardized and accelerated.

**Framing for interview:**
> "I built DocForge-AI to solve a problem I kept seeing: teams spend weeks producing documentation that's inconsistent and often incomplete. I wanted to see if multi-agent AI could produce enterprise-grade docs from a single project idea."

---

## 2. What I Built

**Core system:**
- A CLI tool that generates 10+ types of software documentation from natural language project descriptions
- Multi-agent architecture using CrewAI where each document type has a specialized AI agent (e.g., "Principal Systems Architect" for architecture docs, "QA Lead" for test specs)
- PRD-first workflow: generate requirements → validate → expand to other documents
- Self-contained design with local file storage (no database dependencies)

**Technical implementation:**
- Python package published to PyPI (`pip install docforge-ai`)
- CrewAI for multi-agent orchestration
- OpenAI GPT-4 for content generation
- Template-driven prompts in markdown for customization
- Async document generation with quality validation

**Framing for interview:**
> "DocForge-AI is a multi-agent documentation generator. You give it a project idea, and it uses specialized AI agents to produce a complete documentation suite—PRD, architecture, test specs, deployment guide. It's published on PyPI and designed to be self-contained."

---

## 3. Key Design Decisions

### Why multi-agent vs. single prompt?

Different document types require different expertise and tone. A PRD needs business context; an architecture doc needs technical depth. By giving each document type its own "persona" (agent role + specialized prompt), the output quality is significantly better than a single monolithic prompt.

### Why PRD-first workflow?

Most document generation tools try to create everything at once. DocForge-AI enforces a validate-then-expand pattern: generate the PRD, let the user review it, then use that validated PRD as context for all subsequent documents. This ensures consistency across the documentation suite.

### Why self-contained (no database)?

Many AI tools require Postgres, Redis, or cloud services. DocForge-AI uses local JSON for metadata and markdown files for output. This makes it instantly usable (`pip install` → `docforge-ai init` → generate) and keeps the project scope focused.

**Framing for interview:**
> "Three key decisions: First, multi-agent architecture—different documents need different personas. Second, PRD-first workflow—validate requirements before expanding. Third, self-contained design—no database, just install and use."

---

## 4. Impact & Proof

### Published Package
- **PyPI**: [pypi.org/project/docforge-ai](https://pypi.org/project/docforge-ai/)
- `pip install docforge-ai` works today

### Demo
- **YouTube walkthrough**: [youtu.be/LMP-9WBePdY](https://youtu.be/LMP-9WBePdY)
- End-to-end: idea → PRD → architecture → test spec in under 5 minutes

### Code Quality
- Comprehensive test suite (`pytest`)
- CI/CD pipeline with GitHub Actions
- Type hints and documentation throughout

**Framing for interview:**
> "The project is live on PyPI with real users. The demo shows end-to-end generation in under 5 minutes. The codebase has tests, CI/CD, and is structured for maintainability."

---

## 5. What I'd Ship Next (Production Roadmap)

### Immediate improvements
1. **Evaluation pipeline**: Automated quality scoring for generated docs (coherence, completeness, technical accuracy)
2. **RAG integration**: Ingest existing codebase to generate docs that reference actual implementations
3. **Streaming output**: Show real-time generation progress instead of waiting for completion

### Production hardening
4. **Cost controls**: Token budgets, caching for similar prompts, model fallback (GPT-4 → 3.5 for drafts)
5. **Multi-model support**: Anthropic Claude, local Llama for air-gapped environments
6. **Web UI**: Browser interface for non-CLI users

### Enterprise features
7. **Template marketplace**: Company-specific document templates
8. **Audit trail**: Track who generated what, when, with what prompts
9. **Integration hooks**: Confluence, Notion, GitHub Wiki export

**Framing for interview:**
> "For production, I'd add an evaluation pipeline to measure document quality, RAG integration to reference actual code, and cost controls with token budgets. The architecture already supports adding new AI providers or output formats."

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Stack** | Python, CrewAI, OpenAI, Pydantic |
| **PyPI** | `pip install docforge-ai` |
| **Demo** | [YouTube](https://youtu.be/LMP-9WBePdY) |
| **Key metric** | 10 document types, single CLI command |
| **Design pattern** | Multi-agent orchestration, PRD-first workflow |

---

## Code Tour (for technical interviews)

Point reviewers to:
- `backend/app/services/document_agents.py` — Multi-agent configuration and CrewAI integration
- `docforge.py` — CLI entry point and core orchestration
- `prompts/` — Template-driven prompts for each document type
- `backend/app/services/local_storage_service.py` — Self-contained storage layer
