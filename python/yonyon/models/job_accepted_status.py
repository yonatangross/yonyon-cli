from enum import StrEnum

class JobAcceptedStatus(StrEnum):
    ACCEPTED = "accepted"

    def __str__(self) -> str:
        return str(self.value)
