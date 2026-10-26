from enum import StrEnum

class ErrorCode(StrEnum):
    FORBIDDEN = "forbidden"
    INTERNAL_ERROR = "internal_error"
    INVALID_CURSOR = "invalid_cursor"
    INVALID_LIMIT = "invalid_limit"
    INVALID_OPERATIONS = "invalid_operations"
    INVALID_REQUEST = "invalid_request"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    NOT_FOUND = "not_found"
    RATE_LIMITED = "rate_limited"
    TOO_MANY_OPERATIONS = "too_many_operations"
    UNAVAILABLE = "unavailable"
    UNKNOWN_OP = "unknown_op"

    def __str__(self) -> str:
        return str(self.value)
