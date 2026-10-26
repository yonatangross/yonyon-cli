from enum import StrEnum

class ChatRequestMessagesItemRole(StrEnum):
    ASSISTANT = "assistant"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
