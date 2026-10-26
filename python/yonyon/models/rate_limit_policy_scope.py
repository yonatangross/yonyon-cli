from enum import StrEnum

class RateLimitPolicyScope(StrEnum):
    IP = "ip"

    def __str__(self) -> str:
        return str(self.value)
