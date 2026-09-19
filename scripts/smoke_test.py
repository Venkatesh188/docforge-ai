#!/usr/bin/env python3
"""
DocForge-AI Smoke Test

Verifies that the core DocForge functionality works correctly.
Run without API key for basic validation, or with OPENAI_API_KEY set for full test.

Usage:
    python scripts/smoke_test.py           # Basic checks (no API key needed)
    python scripts/smoke_test.py --full    # Full test (requires OPENAI_API_KEY)
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
SKIP = "\033[93m○\033[0m"


def run_check(name: str, check_fn) -> bool:
    """Run a check and print result."""
    try:
        result = check_fn()
        if result:
            print(f"  {PASS} {name}")
            return True
        else:
            print(f"  {FAIL} {name}")
            return False
    except Exception as e:
        print(f"  {FAIL} {name}: {e}")
        return False


def check_imports() -> bool:
    """Verify core modules can be imported."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
    from app.core.simple_config import Settings, settings
    from app.services.local_storage_service import LocalStorageService
    from app.models import DocumentType
    return True


def check_document_types() -> bool:
    """Verify all expected document types exist."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
    from app.models import DocumentType
    
    expected = [
        "project_charter", "srs", "architecture", "low_level_design",
        "test_specification", "deployment_guide", "operations_manual",
        "business_case", "market_requirements", "vision_brief"
    ]
    actual = [dt.value for dt in DocumentType]
    return all(exp in actual for exp in expected)


def check_prompt_files() -> bool:
    """Verify prompt template files exist."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    required = ["charter.md", "requirements.md", "architecture.md", "design.md", 
                "testing.md", "deployment.md", "operations.md"]
    return all((prompts_dir / f).exists() for f in required)


def check_cli_help() -> bool:
    """Verify CLI help command works."""
    result = subprocess.run(
        [sys.executable, "-m", "docforge.docforge", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.returncode == 0 and "docforge-ai" in result.stdout.lower() or "generate" in result.stdout.lower()


def check_cli_list_docs() -> bool:
    """Verify list-docs command works."""
    result = subprocess.run(
        [sys.executable, "-m", "docforge.docforge", "list-docs"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.returncode == 0 and "document" in result.stdout.lower()


def check_local_storage() -> bool:
    """Verify local storage service initializes correctly."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
    from app.services.local_storage_service import LocalStorageService
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = LocalStorageService(base_dir=Path(tmpdir))
        return storage.projects_dir.exists() and storage.documents_dir.exists()


def check_config_validation() -> bool:
    """Verify configuration validation works."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
    from app.core.simple_config import Settings
    
    config = Settings()
    validation = config.validate_config()
    return "valid" in validation and "errors" in validation


def check_api_key_present() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


def run_full_generation_test() -> bool:
    """Run a full document generation test (requires API key)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [sys.executable, "-m", "docforge.docforge", "generate", 
             "Test project for smoke test", "--docs", "srs", "--name", "smoke-test"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
            env={**os.environ, "DOCFORGE_GENERATED_DOCS_PATH": tmpdir}
        )
        
        if result.returncode != 0:
            print(f"    Output: {result.stdout[:500]}")
            print(f"    Error: {result.stderr[:500]}")
            return False
        
        generated_dir = Path(tmpdir) / "smoke-test"
        return generated_dir.exists() and any(generated_dir.glob("*.md"))


def print_manual_checklist():
    """Print manual demo checklist."""
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                    MANUAL DEMO CHECKLIST                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Install:                                                    │
│     pip install docforge-ai                                     │
│                                                                 │
│  2. Initialize:                                                 │
│     docforge-ai init                                            │
│     # Add OPENAI_API_KEY to .env                                │
│                                                                 │
│  3. Generate PRD:                                               │
│     docforge-ai generate "E-commerce platform" --docs srs       │
│                                                                 │
│  4. Verify output:                                              │
│     - Check generated-docs/e-commerce-platform/                 │
│     - Open 01_srs.md                                            │
│     - Verify professional formatting, no placeholders           │
│                                                                 │
│  5. Generate additional docs:                                   │
│     docforge-ai continue e-commerce-platform ARCH TEST          │
│                                                                 │
│  6. Verify consistency:                                         │
│     - Architecture doc references PRD requirements              │
│     - Test spec covers features from PRD                        │
│                                                                 │
│  Expected time: ~3-5 minutes for full demo                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")


def main():
    """Run smoke tests."""
    full_test = "--full" in sys.argv
    
    print("\n" + "=" * 60)
    print("  DocForge-AI Smoke Test")
    print("=" * 60)
    
    print("\n[1/3] Core Module Checks")
    checks_passed = 0
    total_checks = 0
    
    checks = [
        ("Import core modules", check_imports),
        ("Document types defined", check_document_types),
        ("Prompt templates exist", check_prompt_files),
        ("Configuration validation", check_config_validation),
        ("Local storage initialization", check_local_storage),
    ]
    
    for name, fn in checks:
        total_checks += 1
        if run_check(name, fn):
            checks_passed += 1
    
    print("\n[2/3] CLI Checks")
    cli_checks = [
        ("CLI help command", check_cli_help),
        ("CLI list-docs command", check_cli_list_docs),
    ]
    
    for name, fn in cli_checks:
        total_checks += 1
        if run_check(name, fn):
            checks_passed += 1
    
    print("\n[3/3] Integration Checks")
    has_api_key = check_api_key_present()
    
    if has_api_key:
        print(f"  {PASS} API key configured")
        if full_test:
            total_checks += 1
            if run_check("Full generation test", run_full_generation_test):
                checks_passed += 1
        else:
            print(f"  {SKIP} Full generation test (run with --full)")
    else:
        print(f"  {SKIP} API key not configured (set OPENAI_API_KEY for full test)")
        print(f"  {SKIP} Full generation test skipped")
    
    print("\n" + "-" * 60)
    print(f"  Result: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("  Status: READY")
    else:
        print("  Status: ISSUES FOUND")
    
    print_manual_checklist()
    
    return 0 if checks_passed == total_checks else 1


if __name__ == "__main__":
    sys.exit(main())
