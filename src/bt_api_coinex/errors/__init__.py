from __future__ import annotations

from typing import Any

from bt_api_base.error import (
    ErrorCategory,
    ErrorTranslator,
    UnifiedError,
    UnifiedErrorCode,
)


class CoinExErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        message = str(raw_error.get("message", raw_error.get("msg", "")))
        lower = message.lower()
        code = raw_error.get("code")

        if code in (0, "0"):
            return None
        if "balance" in lower or "insufficient" in lower:
            error_code = UnifiedErrorCode.INSUFFICIENT_BALANCE
        elif "order" in lower and "not found" in lower:
            error_code = UnifiedErrorCode.ORDER_NOT_FOUND
        elif "duplicate" in lower:
            error_code = UnifiedErrorCode.DUPLICATE_ORDER
        elif "rate" in lower or "limit" in lower:
            error_code = UnifiedErrorCode.RATE_LIMIT_EXCEEDED
        elif "auth" in lower or "key" in lower or "signature" in lower:
            error_code = UnifiedErrorCode.INVALID_API_KEY
        else:
            return super().translate(raw_error, venue)

        return UnifiedError(
            code=error_code,
            category=ErrorCategory.BUSINESS,
            venue=venue,
            message=message or error_code.name,
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
