from enum import StrEnum

class CreateJobBodyOp(StrEnum):
    ABOUT = "about"
    PROJECTS = "projects"
    SERVICES = "services"

    def __str__(self) -> str:
        return str(self.value)
