from pathlib import Path
from typing import Type, Optional, Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ChinaExplainerInput(BaseModel):
    """Input schema for ChinaEducationExplainer."""
    question: Any = Field(
        ..., description="Question or instruction about the Chinese education ecosystem."
    )
    knowledge_path: Optional[Any] = Field(
        default=None,
        description="Optional absolute path to the China education markdown file."
    )


class ChinaEducationExplainer(BaseTool):
    name: str = "ChinaEducationExplainer"
    description: str = (
        "Provides grounded context on the Chinese education ecosystem from the knowledge base."
    )
    args_schema: Type[BaseModel] = ChinaExplainerInput

    def _run(self, question: Any, knowledge_path: Optional[Any] = None) -> str:  # type: ignore[override]
        def normalize_text(value: Any, fallback: str) -> str:
            if isinstance(value, str):
                return value
            return fallback

        def normalize_path(value: Optional[Any]) -> Optional[Path]:
            if value is None:
                return None
            if isinstance(value, str):
                lowered = value.strip().lower()
                if lowered in {"", "none", "null", "nil"}:
                    return None
                try:
                    return Path(value)
                except Exception:
                    return None
            return None

        default_path = Path(__file__).resolve().parents[3] / 'knowledge' / 'china_education.md'
        normalized_path = normalize_path(knowledge_path)
        path = normalized_path if normalized_path else default_path
        question_text = normalize_text(question, "Explain China’s education ecosystem at a high level.")
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            return f"Error reading China education file at {path}: {exc}"

        preface = (
            "Answer the user's question using the following factual reference on the Chinese education ecosystem.\n"
            "Cite only facts present in the reference; format clearly.\n\n"
        )
        return preface + text[:2000]


