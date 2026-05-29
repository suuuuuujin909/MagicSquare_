"""Control orchestration — RED stub."""

from typing import Any

from src.boundary.validator import BoundaryValidator


def resolve(grid: Any) -> list[int]:
  """Domain resolution entry point (AC-FR01-05 isolation target)."""
  raise NotImplementedError("resolve is not implemented")


class MagicSquareControl:
  """Delegates to boundary validation, then domain resolve on success."""

  def __init__(self, validator: BoundaryValidator | None = None) -> None:
    self._validator = validator or BoundaryValidator()

  def handle(self, grid: Any) -> list[int]:
    self._validator.validate(grid)
    return resolve(grid)
