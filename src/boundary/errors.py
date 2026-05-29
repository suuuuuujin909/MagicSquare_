"""Boundary-layer validation errors (contract surface for Track A)."""


class BoundaryValidationError(Exception):
  """Raised when input fails FR-01 boundary checks."""

  def __init__(self, code: str, message: str) -> None:
    super().__init__(message)
    self.code = code
    self.message = message
