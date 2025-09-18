from pathlib import Path
from typing import Type, Optional, Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class BootcampFAQInput(BaseModel):
    """Input schema for BootcampFAQTool."""
    question: Any = Field(..., description="Prospective client's question about the bootcamp")
    faq_path: Optional[Any] = Field(
        default=None, description="Optional absolute path to the bootcamp FAQ markdown file."
    )


class BootcampFAQTool(BaseTool):
    name: str = "BootcampFAQTool"
    description: str = (
        "Provides education bootcamp program details and policies from the knowledge base to answer client Q&A."
    )
    args_schema: Type[BaseModel] = BootcampFAQInput

    def _run(self, question: Any, faq_path: Optional[Any] = None) -> str:  # type: ignore[override]
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

        default_path = Path(__file__).resolve().parents[3] / 'knowledge' / 'bootcamp_faq.md'
        normalized_path = normalize_path(faq_path)
        path = normalized_path if normalized_path else default_path
        question_text = normalize_text(question, "Answer common education languages bootcamp questions on refunds and workload.")
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            return f"Error reading bootcamp FAQ at {path}: {exc}"

        header = (
            "Use the following official Bootcamp FAQ as the single source of truth. "
            "Answer the user's question precisely; if not covered, say what is known and offer to clarify.\n\n"
        )
        return header + text[:1500]


