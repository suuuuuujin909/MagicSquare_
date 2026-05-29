"""FR-01 input verification — 4x4 size contract (AC-FR-01-01)."""

from typing import Any

from src.boundary.errors import BoundaryValidationError

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."
EXPECTED_SIZE = 4


class BoundaryValidator:
  """Validates 4x4 grid contract before Control/Domain work."""

  def validate(self, grid: Any) -> None:
    """Return only when grid satisfies BR-01 size contract; else raise BoundaryValidationError."""
    if not self._is_valid_size(grid):
      raise BoundaryValidationError(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)

  def _is_valid_size(self, grid: Any) -> bool:
    if grid is None or not isinstance(grid, list):
      return False
    if len(grid) != EXPECTED_SIZE:
      return False
    for row in grid:
      if not isinstance(row, list) or len(row) != EXPECTED_SIZE:
        return False
    return True
