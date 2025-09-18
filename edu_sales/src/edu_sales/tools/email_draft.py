from typing import Type, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class EmailDraftInput(BaseModel):
    """Input schema for EmailDraftTool."""
    recipient: str = Field(..., description="Recipient name or role")
    purpose: str = Field(..., description="Purpose/context of the email")
    call_to_action: str = Field(..., description="Specific next step you want the reader to take")
    tone: Optional[str] = Field(default="friendly, professional", description="Tone/style guidance")
    length: Optional[str] = Field(default="short", description="short | medium | long")


class EmailDraftTool(BaseTool):
    name: str = "EmailDraftTool"
    description: str = (
        "Generates a structured email skeleton (subject + body sections) given context; the agent will polish."
    )
    args_schema: Type[BaseModel] = EmailDraftInput

    def _run(
        self,
        recipient: str,
        purpose: str,
        call_to_action: str,
        tone: Optional[str] = None,
        length: Optional[str] = None,
    ) -> str:  # type: ignore[override]
        subject = f"Re: {purpose[:80]}" if len(purpose) > 0 else "Quick note"
        opener = f"Hi {recipient}," if recipient else "Hello," 

        bullets = (
            "- Context: " + purpose + "\n"
            "- Value: Brief benefit/outcome\n"
            "- Next step: " + call_to_action
        )

        signature = (
            "Best regards,\n"
            "Coco\n"
            "Program Lead | [Your Bootcamp]\n"
            "hello@yourbootcamp.com"
        )

        body = (
            f"{opener}\n\n"
            f"I hope you're well. {purpose}.\n\n"
            f"Key points:\n{bullets}\n\n"
            f"If helpful, I'm happy to share more details or hop on a quick call.\n\n"
            f"{signature}"
        )

        return f"Subject: {subject}\n\n{body}"


