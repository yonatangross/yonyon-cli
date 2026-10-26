from enum import StrEnum

class JobAcceptedOp(StrEnum):
    ABOUT = "about"
    PROJECTS = "projects"
    SERVICES = "services"

    def __str__(self) -> str:
        return str(self.value)
