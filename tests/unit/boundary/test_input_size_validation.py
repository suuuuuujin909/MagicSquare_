"""AC-FR-01-01 input size validation — Track A RED tests."""

from unittest.mock import patch

import pytest

from src.boundary.errors import BoundaryValidationError
from src.boundary.validator import BoundaryValidator
from src.control.magic_square_control import MagicSquareControl

INVALID_SIZE_CODE = "INVALID_SIZE"
PRD_SECTION_8_1_MESSAGE = "Grid must be 4x4."


class TestInputSizeValidationAcFr0101:
  """AC-FR-01-01, PRD §8.1 INVALID_SIZE — FR-01 4x4 size contract only (RED)."""

  @pytest.fixture
  def validator(self) -> BoundaryValidator:
    return BoundaryValidator()

  def test_grid_none_raises_invalid_size_error_code(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — explicit None must fail size contract."""
    # AC-FR-01-01
    # Given: grid is explicitly None
    grid = None

    # When: boundary validates input size
    # Then: INVALID_SIZE is raised with contract message
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.code == INVALID_SIZE_CODE

  def test_grid_empty_list_raises_invalid_size_error_code(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list is not 4x4."""
    # AC-FR-01-01
    # Given: grid is an empty list (zero rows)
    grid: list[list[int]] = []

    # When: boundary validates input size
    # Then: INVALID_SIZE is raised
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.code == INVALID_SIZE_CODE
    assert exc_info.value.message == PRD_SECTION_8_1_MESSAGE

  def test_grid_four_rows_zero_cols_raises_invalid_size_error_code(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — four rows with no columns."""
    # AC-FR-01-01
    # Given: grid has four rows but each row has zero columns
    grid = [[]] * 4

    # When: boundary validates input size
    # Then: INVALID_SIZE is raised
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.code == INVALID_SIZE_CODE
    assert exc_info.value.message == PRD_SECTION_8_1_MESSAGE

  def test_grid_three_by_four_raises_invalid_size_error_code(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — row count must be four."""
    # AC-FR-01-01
    # Given: grid is 3 rows by 4 columns (TD-03 style invalid size)
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # When: boundary validates input size
    # Then: INVALID_SIZE is raised (not blank-count or value-range codes)
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.code == INVALID_SIZE_CODE
    assert exc_info.value.message == PRD_SECTION_8_1_MESSAGE

  def test_grid_none_resolve_called_zero_times_isolation(self) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — domain resolve must not run on size failure."""
    # AC-FR-01-01
    # Given: grid is None and control orchestrates validate-then-resolve
    grid = None
    control = MagicSquareControl()

    # When: handle is invoked with resolve spied
    # Then: resolve is never called because boundary fails first
    with patch("src.control.magic_square_control.resolve") as resolve_mock:
      with pytest.raises(BoundaryValidationError):
        control.handle(grid)

      resolve_mock.assert_not_called()
      assert resolve_mock.call_count == 0

  def test_grid_none_message_exact_match_prd_section_8_1(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message must match contract verbatim."""
    # AC-FR-01-01
    # Given: grid is None
    grid = None

    # When: boundary validates input size
    # Then: message equals PRD §8.1 string byte-for-byte
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.message == PRD_SECTION_8_1_MESSAGE
    assert repr(exc_info.value.message) == repr(PRD_SECTION_8_1_MESSAGE)

  def test_grid_three_by_four_with_invalid_cell_still_invalid_size_only_scope(
    self, validator: BoundaryValidator
  ) -> None:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — size failure precedes AC-FR-01-02~05 / FR-02~05."""
    # AC-FR-01-01
    # Given: wrong shape (3x4) plus out-of-range cell (would be AC-FR-01-03 if shape passed)
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 17]]

    # When: boundary validates input size first
    # Then: only INVALID_SIZE is reported (no blank-count / duplicate / domain codes)
    with pytest.raises(BoundaryValidationError) as exc_info:
      validator.validate(grid)

    assert exc_info.value.code == INVALID_SIZE_CODE
    assert exc_info.value.code != "INVALID_BLANK_COUNT"
    assert exc_info.value.code != "INVALID_CELL_VALUE"
    assert exc_info.value.code != "DUPLICATE_VALUE"
    assert exc_info.value.code != "E-DOM-001"
