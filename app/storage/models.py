from pydantic import BaseModel
from typing import Optional

class Finding(BaseModel):
    tool : str
    category : str
    severity : str
    file : str
    line : int
    message : str
    code_snippet : Optional[str] = None

    def to_markdown(self) -> str:
        icon = {"high" : "🔴", "medium" : "🟡", "low" : "⚪"}.get(self.severity, "⚠️")
        return f"- {icon} **{self.tool.title()}** ({self.category}): {self.message} (Line {self.line})"
    