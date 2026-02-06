#!/usr/bin/env python3
import sys
import os

def check_specs():
    """
    Verifies that mandatory Spec-Kit artifacts exist.
    """
    mandatory_files = [
        "constitution.md",
        "specs/_meta.md",
        "specs/functional.md",
        "specs/technical.md",
        "specs/personas.md",
        "specs/ui.md",
        "specs/security.md",
        "specs/acceptance_criteria.md",
        "skills/README.md",
        "skills/skill_ingest_trend_feeds/README.md",
        "skills/skill_generate_media_asset/README.md",
        "skills/skill_execute_publish_intent/README.md",
        "research/tooling_strategy.md"
    ]

    print("Running spec compliance check...")
    missing = []
    for f in mandatory_files:
        if not os.path.exists(f):
            missing.append(f)
            print(f"MISSING: {f}")
        else:
            print(f"OK: {f}")

    if missing:
        print(f"\nFAIL: {len(missing)} mandatory artifacts missing.")
        sys.exit(1)

    print("\nSUCCESS: All mandatory artifacts are present.")
    # In a real SDD workflow, we might also check for coherence and test coverage.
    sys.exit(0)

if __name__ == "__main__":
    check_specs()
