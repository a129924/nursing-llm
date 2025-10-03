from dataclasses import dataclass

from nursing_llm_server.core.enums.role import Role


@dataclass(frozen=True)
class Message:
    role: Role
    content: str
