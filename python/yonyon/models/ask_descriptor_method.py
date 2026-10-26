from enum import StrEnum

class AskDescriptorMethod(StrEnum):
    POST = "POST"

    def __str__(self) -> str:
        return str(self.value)
