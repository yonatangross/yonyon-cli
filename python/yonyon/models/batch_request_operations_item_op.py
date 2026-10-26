from enum import StrEnum

class BatchRequestOperationsItemOp(StrEnum):
    ABOUT = "about"
    PROJECTS = "projects"
    SERVICES = "services"

    def __str__(self) -> str:
        return str(self.value)
