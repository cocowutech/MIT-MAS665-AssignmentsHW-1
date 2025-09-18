#!/usr/bin/env python
import sys
import os
import warnings
import urllib.request
from datetime import datetime

from edu_sales.crew import EduSales

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def define_llm_model():
    # Provide sane defaults; allow overrides via env
    if not (os.getenv("LLM_MODEL") and os.getenv("LLM_PROVIDER")):
        os.environ["LLM_PROVIDER"] = os.getenv("LLM_PROVIDER", "perplexity")
        os.environ["LLM_MODEL"] = os.getenv("LLM_MODEL", "perplexity/llama-3.1-sonar-large-128k")
    # Map MODEL for libraries that read generic MODEL env

    if not os.getenv("MODEL"):
        os.environ["MODEL"] = os.environ.get("LLM_MODEL")
    # Map common provider keys to LLM_API_KEY if not set
    for k in ("PERPLEXITY_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
        if os.getenv(k) and not os.getenv("LLM_API_KEY"):
            os.environ["LLM_API_KEY"] = os.environ[k]
            break

def run():
    """
    Run the crew.
    """
    # Ensure provider/model env is set and valid (prefer Gemini)
    define_llm_model()

    # Allow overriding inputs from CLI for ad-hoc questions:
    # Example:
    #   uv run run_crew "Introduce yourself in 2 sentences" "What is Gaokao?" "Director" "partnership intro" "Can we get a refund?"
    print("Using sys.argv: ", sys.argv[1:] if len(sys.argv) > 1 else "Using default examples due to no arguments provided")
    intro_cli = sys.argv[1] if len(sys.argv) > 1 else None
    china_cli = sys.argv[2] if len(sys.argv) > 2 else None
    email_recipient_cli = sys.argv[3] if len(sys.argv) > 3 else None
    email_purpose_cli = sys.argv[4] if len(sys.argv) > 4 else None
    bootcamp_cli = sys.argv[5] if len(sys.argv) > 5 else None

    inputs = {
        # Intro
        'intro_prompt': intro_cli or 'Introduce yourself to the class in 3 sentences.',
        # China ecosystem
        'china_question': china_cli or 'Explain China\'s education system to a new parent.',
        # Email draft
        'email_recipient': email_recipient_cli or 'Admissions Director',
        'email_purpose': email_purpose_cli or 'introducing our APAC-friendly AI language education bootcamp cohort and proposing a partner call',
        'email_cta': 'Would next Tuesday 10:00–10:30am GMT+8 work for a quick intro call?',
        # Bootcamp Q&A
        'bootcamp_question': bootcamp_cli or 'What is the refund policy and typical weekly workload?',
        # Context fields to inject knowledge directly into prompts
        'persona_context': _read_knowledge('persona_coco.md'),
        'china_context': _read_knowledge('china_education.md'),
        'faq_context': _read_knowledge('bootcamp_faq.md'),
        # Enforce language and format at runtime too
        'output_language': 'English',
        'output_style': 'human-friendly; no code; no JSON; no backticks; no tool names',
    }
    
    # Clean stale outputs before running to avoid mixing previous incorrect content
    try:
        out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'outputs')
        out_dir = os.path.abspath(out_dir)
        if os.path.isdir(out_dir):
            for name in [
                'intro.md',
                'china_ecosystem.md',
                'email_draft.md',
                'bootcamp_qa.md',
            ]:
                p = os.path.join(out_dir, name)
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    except Exception:
        pass

    # Pre-run validation: required contexts are present
    _validate_context(inputs)

    try:
        result = EduSales().crew().kickoff(inputs=inputs)
        if result is not None:
            print("\n=== Crew Run Completed ===\n")
            print(result)
        # Post-run validation: ensure English/plain text
        _validate_plain_english_outputs()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def _read_knowledge(name: str) -> str:
    try:
        import os
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge'))
        path = os.path.join(base, name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    return ''


def _validate_context(inputs: dict) -> None:
    missing = []
    for key in ['persona_context', 'china_context', 'faq_context']:
        if not inputs.get(key):
            missing.append(key)
    if missing:
        raise RuntimeError(f"Missing required context: {', '.join(missing)}. Populate knowledge files in knowledge/.")


def _validate_plain_english_outputs() -> None:
    # Ensure outputs exist and appear plain text English (heuristic checks)
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
    targets = ['intro.md', 'china_ecosystem.md', 'email_draft.md', 'bootcamp_qa.md']
    for name in targets:
        path = os.path.join(out_dir, name)
        if not os.path.exists(path):
            raise RuntimeError(f"Expected output not found: {name}")
        try:
            text = ''
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            # No code fences or JSON braces dominance
            if '```' in text or text.strip().startswith('{') or text.strip().startswith('['):
                raise RuntimeError(f"Output contains code/JSON formatting: {name}")
            # Basic language heuristic: ensure mostly ASCII and common English words present
            ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(len(text), 1)
            if ascii_ratio < 0.95:
                raise RuntimeError(f"Output may not be English/plain text: {name}")
        except Exception as ex:
            raise RuntimeError(f"Validation failed for {name}: {ex}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        EduSales().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EduSales().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        EduSales().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    print("🚀 Starting Coco's (Rong Wu) MIT AI Studio Crew AI Example")
    print("=" * 50)
    run()
