from enum import StrEnum

class JobStatus(StrEnum):
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
