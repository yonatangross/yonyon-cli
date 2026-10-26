from enum import StrEnum

class ApiVersionRootStatus(StrEnum):
    DEPRECATED = "deprecated"
    STABLE = "stable"

    def __str__(self) -> str:
        return str(self.value)
