from pathlib import Path
from typing import Type, Optional, Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ProfileResponderInput(BaseModel):
    """Input schema for ProfileResponder."""
    prompt: Any = Field(..., description="User prompt or instruction for introduction/bio.")
    persona_path: Optional[Any] = Field(
        default=None,
        description="Optional absolute path to persona markdown. Overrides default if provided."
    )


class ProfileResponder(BaseTool):
    name: str = "ProfileResponder"
    description: str = (
        "Returns Coco's persona/biography content from the knowledge base to ground introductions."
    )
    args_schema: Type[BaseModel] = ProfileResponderInput

    def _run(self, prompt: Any, persona_path: Optional[Any] = None) -> str:  # type: ignore[override]
        def normalize_prompt(value: Any) -> str:
            if isinstance(value, str):
                return value
            # If LLM mistakenly passes schema dict, fall back to a sensible default
            return "Introduce yourself to the class in 3 sentences."

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

        default_path = Path(__file__).resolve().parents[3] / 'knowledge' / 'persona_coco.md'
        prompt_text = normalize_prompt(prompt)
        normalized_path = normalize_path(persona_path)
        path = normalized_path if normalized_path else default_path
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            return f"Error reading persona file at {path}: {exc}"

        header = (
            "You asked for an introduction/profile. Here is Coco's persona reference. "
            "Use it as factual grounding and adapt style to the prompt.\n\n"
        )
        # Clip to reduce token usage
        clipped = text[:800]
        return header + clipped


