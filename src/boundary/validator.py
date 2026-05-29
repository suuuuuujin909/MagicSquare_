"""FR-01 input verification — RED stub (size check not implemented)."""

from typing import Any


class BoundaryValidator:
  """Validates 4x4 grid contract before Control/Domain work."""

  def validate(self, grid: Any) -> None:
    """Return only when grid satisfies BR-01 size contract; else raise BoundaryValidationError."""
    # RED: deliberate no-op — tests must fail until size validation is implemented.
    return None
