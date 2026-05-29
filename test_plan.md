# Magic Square 4×4 — 테스트 계획서 (Track A: FR-01 입력 크기 검증)

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-FR01-SIZE-001 |
| **버전** | 1.0 |
| **작성 역할** | Senior QA Lead |
| **기준 PRD** | `docs/PRD_MagicSquare.md` (또는 동등 세션 산출 PRD) |
| **앵커 AC** | **AC-FR01-01** (+ 격리 검증 **AC-FR01-05**) |
| **앵커 FR** | **FR-01** Input Verification (Boundary), **BR-01** |
| **스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **Dual-Track** | Track A (Boundary) — 본 문서 범위 |

---

## 1. 목적 및 범위

### 1.1 목적

선택 샘플 **AC-FR01-01** (`grid = None` → 크기 계약 위반)을 중심으로, FR-01의 **4×4 행렬 크기 검증**에 대한 pytest 단위 테스트 범위·우선순위·경계값·격리 전략·커버리지 측정 방법을 정의한다.

### 1.2 In-Scope (본 계획서)

| 구분 | 내용 |
|------|------|
| 계층 | **Boundary** (`BoundaryValidator` 또는 동등 진입점) |
| 규칙 | **BR-01** — 입력은 항상 4행×4열 정수 행렬 |
| AC | **AC-FR01-01**, **AC-FR01-05** |
| 오류 계약 | 구현 코드명: `INVALID_SIZE` — PRD §13 대응: `E-BND-001` |
| 메시지 | `Grid must be 4x4.` (PRD 원문: `Input matrix must be 4x4.` — 팀이 하나로 확정할 때까지 본 계획은 **요청 샘플 문구**를 기준으로 한다) |

### 1.3 Out-of-Scope (본 계획서 — 명시적 제외)

| 항목 | 관련 AC | 비고 |
|------|---------|------|
| 빈칸(0) 개수 검증 | AC-FR01-02 | 별도 TP-FR01-BLANK |
| 셀 값 범위 `0 \| 1..16` | AC-FR01-03 | 별도 TP |
| 0 제외 중복 | AC-FR01-04 | 별도 TP |
| **4×4 정상 입력 통과** | (AC-FR01-06 후보) | **AC-FR01-01 범위 외 — 본 문서에 테스트 케이스로 포함하지 않음** |
| Domain 불변식(마방진 합=34 등) | FR-04 | Track B |
| Solver 두 조합 시도 | FR-05 | Control/Domain |

---

## 2. 오류 계약 (검증 기준)

### 2.1 실패 응답 형식 (pydantic)

Boundary 실패 시 **값 반환 금지**, 구조화된 예외/오류 객체 반환.

| 필드 | 타입 | AC-FR01-01 기대값 |
|------|------|-------------------|
| `code` | `str` | `"INVALID_SIZE"` |
| `message` | `str` | `"Grid must be 4x4."` |

> **PRD 추적:** §13 `E-BND-001` — Layer: Boundary, Domain resolver 호출 **금지**.

### 2.2 예외 타입 (구현 시)

- 권장: `BoundaryValidationError` (또는 pydantic `ValidationError` 래핑) + `error_code: str` 필드
- 테스트 Assert: `code` / `message` 우선 (메시지 언어는 PRD Open Question — 코드 필드가 SSOT)

---

## 3. pytest 단위 테스트 — 범위 및 우선순위

### 3.1 테스트 피라미드 (본 슬라이스)

```
P0  BoundaryValidator.validate_size / validate (크기 선행 검사만)
P1  Boundary 진입 Facade (CLI/API adapter가 validator 호출)
P2  Control 오케스트레이션 — FR-01 실패 시 resolve 미호출 (통합에 가깝지만 mock으로 단위화 가능)
```

### 3.2 우선순위 정의

| 우선순위 | ID 접두사 | 대상 | AC | 실행 시점 |
|----------|-----------|------|-----|-----------|
| **P0** | `UT-BND-SIZE-` | `grid is None` → `INVALID_SIZE` | AC-FR01-01 | Track A RED **1순위** |
| **P0** | `UT-BND-SIZE-` | 동일 실패 + Domain 진입점 **0회** | AC-FR01-05 | P0와 동일 테스트 클래스, mock assert 병행 |
| **P1** | `UT-BND-SIZE-` | 빈 리스트, 열 없음, 3×4 / 4×3 / 5×5 | AC-FR01-01 | P0 GREEN 직후 |
| **P2** | `UT-BND-ISO-` | Control `resolve` / `DomainResolver` spy — FR-01 실패 경로 전수 | AC-FR01-05 | P1 완료 후 |
| **제외** | — | 4×4 유효 행렬 통과 | — | **본 계획 미포함** (FR-01 성공 경로 TP 별도) |

### 3.3 권장 테스트 모듈 구조 (구현 전 설계)

```
tests/
  unit/
    boundary/
      test_input_size_validation.py    # AC-FR01-01, 05 (본 계획)
    control/
      test_resolve_not_called_on_bnd_failure.py  # P2 (선택)
```

### 3.4 AAA 패턴 (필수)

모든 테스트는 **Arrange → Act → Assert** 순서를 주석 또는 빈 줄로 구분한다.

```text
# Arrange: grid = None
# Act:   result = boundary_validator.validate(grid)
# Assert: code == INVALID_SIZE, domain_entry.call_count == 0
```

### 3.5 명명 규칙

- 함수: `test_<조건>_<기대결과>`
- 예: `test_grid_none_raises_invalid_size_without_domain_call`

---

## 4. 경계값 케이스 목록

모든 행은 **AC-FR01-01** 범위. 기대 결과는 동일 오류 계약(`INVALID_SIZE` / `Grid must be 4x4.`) unless noted.

| TC ID | 입력 `grid` | 크기 판정 | 기대 `code` | AC | 비고 |
|-------|-------------|-----------|-------------|-----|------|
| **TC-SIZE-001** | `None` | 미정의 (null) | `INVALID_SIZE` | AC-FR01-01, 05 | **앵커 샘플** — 명시적 `None` |
| **TC-SIZE-002** | `[]` | 0×? | `INVALID_SIZE` | AC-FR01-01, 05 | 빈 리스트 |
| **TC-SIZE-003** | `[[]] * 4` | 4×0 (행 4, 열 0) | `INVALID_SIZE` | AC-FR01-01, 05 | 행 존재·열 없음; `len(row)==0` |
| **TC-SIZE-004** | 3×4 행렬 (예: TD-03 변형) | 3×4 | `INVALID_SIZE` | AC-FR01-01, 05 | PRD ES-01 / TD-03 계열 |
| **TC-SIZE-005** | 4×3 행렬 | 4×3 | `INVALID_SIZE` | AC-FR01-01, 05 | 열 수 불일치 |
| **TC-SIZE-006** | 5×5 행렬 | 5×5 | `INVALID_SIZE` | AC-FR01-01, 05 | 확대 크기 |
| **TC-SIZE-007** | `[[0]*4 for _ in range(4)]` (4×4, 값 무관) | 4×4 | — | **제외** | **AC-FR01-01 범위 외 — 본 계획 테스트 목록에 넣지 않음** (빈칸 개수 등은 FR-01 다른 AC) |

### 4.1 3×4 / 4×3 / 5×5 구체 Arrange 예시 (고정 데이터)

**TC-SIZE-004 (3×4)** — PRD TD-03:

```python
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
```

**TC-SIZE-005 (4×3):**

```python
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
```

**TC-SIZE-006 (5×5):**

```python
grid = [[1, 2, 3, 4, 5] for _ in range(5)]
```

### 4.2 검증 순서 (구현 가이드 — 테스트 관점)

FR-01은 **크기(BR-01) → 빈칸 수 → 값 범위 → 중복** 순으로 실패해야 한다.  
본 계획 케이스는 모두 **1단계에서 실패**해야 하며, 후속 검증 로직이 호출되더라도 **Domain 진입은 0회** (AC-FR01-05).

---

## 5. 예외·특이 케이스 목록

| TC ID | 시나리오 | 입력 | 기대 | AC | 테스트 의도 |
|-------|----------|------|------|-----|----------------|
| **TC-EX-001** | `None` vs 미전달 | `validate(None)` vs `validate()` (시그니처 허용 시) | 동일 `INVALID_SIZE` | AC-FR01-01 | optional 인자 혼동 방지 |
| **TC-EX-002** | 비정형 중첩 | `grid = [1, 2, 3, 4]` (1차원) | `INVALID_SIZE` | AC-FR01-01 | 타입/형태 계약 |
| **TC-EX-003** | 비정형 중첩 | `grid = [[1, 2], "row"]` | `INVALID_SIZE` | AC-FR01-01 | 행 원소 비-list |
| **TC-EX-004** | `[[]] * 4` 별칭 | 동일 객체 4행 참조 | `INVALID_SIZE` | AC-FR01-01 | TC-SIZE-003과 동일 기대 |
| **TC-EX-005** | 불균일 행 길이 | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `INVALID_SIZE` | AC-FR01-01 | 직사각형 아님 → 크기 불일치로 귀속 |
| **TC-EX-006** | pydantic 모델 경유 | `GridInput(matrix=None)` | `INVALID_SIZE` | AC-FR01-01 | Boundary DTO 검증 레이어 |
| **TC-EX-007** | 이중 실패 | 3×4 + 값 17 포함 | `INVALID_SIZE` **만** (크기 우선) | AC-FR01-01 | 오류 코드 단일성; `E-BND-003` 노출 금지 |
| **TC-EX-008** | 부수 효과 | 동일 `grid` 객체 2회 호출 | 동일 오류, 입력 변형 없음 | NFR | §14 no side effects |

---

## 6. Domain 해결 진입점 호출 횟수 검증 전략 (mock / spy)

### 6.1 “Domain 해결 진입점” 정의 (테스트 대상 명칭)

PRD **AC-FR01-05** (“Domain resolver를 호출하지 않는다”)를 ECB에 맞게 다음 **단일 진입점**으로 고정한다.

| 후보 컴포넌트 | Layer | 본 계획에서의 spy 대상 |
|---------------|-------|------------------------|
| `Control.resolve` (또는 `MagicSquareService.solve`) | Control | **권장 — 1차 spy** |
| `Solver.run` | Control | resolve 내부 호출 시 간접 검증 |
| `BlankFinder` / `MissingNumberFinder` / `MagicSquareValidator` | Entity | resolve 우회 호출 방지용 **2차 spy** (선택) |

**본 계획 SSOT:** `Control.resolve` (이름은 구현 시 확정, 테스트는 `resolve` 심볼에 패치).

### 6.2 패턴 A — `unittest.mock.patch` (P0/P1 기본)

```python
# Arrange
with patch("src.control.magic_square_control.resolve") as resolve_mock:
    # Act
    with pytest.raises(BoundaryValidationError) as exc:
        boundary_validator.validate(grid=None)
    # Assert — AC-FR01-01
    assert exc.value.code == "INVALID_SIZE"
    # Assert — AC-FR01-05
    resolve_mock.assert_not_called()
```

### 6.3 패턴 B — `MagicMock` + `call_count` (P2)

```python
resolve_spy = MagicMock()
control = MagicSquareControl(resolve=resolve_spy)
with pytest.raises(BoundaryValidationError):
    control.handle(grid=None)
assert resolve_spy.call_count == 0
```

### 6.4 패턴 C — pytest `mocker` fixture (pytest-mock 사용 시)

```python
def test_grid_none(mocker):
    spy = mocker.patch("src.control.magic_square_control.resolve")
    ...
    spy.assert_not_called()
```

### 6.5 검증 매트릭스 (경계값 × spy)

| TC ID | `resolve.call_count` | `BlankFinder.find` (선택) |
|-------|----------------------|---------------------------|
| TC-SIZE-001 ~ 006 | **0** | **0** (패치 시) |
| TC-EX-001 ~ 008 | **0** | **0** |
| TC-SIZE-007 | *(테스트 없음)* | *(테스트 없음)* |

### 6.6 실패 시 진단

| 관측 | 원인 추정 | 조치 |
|------|-----------|------|
| `resolve` 1회 호출 | Boundary가 실패 전에 Control 위임 | FR-01 선행 검증 순서 수정 |
| `BlankFinder` 호출 | 크기 검증 우회 | BR-01 검사를 최상단으로 이동 |
| 예외 없이 `None` 반환 | 실패 정책 미구현 | §13 예외 정책 적용 |

---

## 7. 커버리지 목표

PRD §14 Non-Functional Requirements 및 프로젝트 Dual-Track 정책.

| 계층 | 패키지 (예정) | 목표 | 본 계획 기여 |
|------|---------------|------|----------------|
| **Domain (Entity)** | `src/entity/` | **≥ 95%** | 간접 — FR-01 실패 시 **미실행** 증명 (호출 0) |
| **Boundary** | `src/boundary/` | **≥ 85%** | **직접** — `validate` / size check 분기 전수 |
| **Control** | `src/control/` | ≥ 85% (Boundary와 동일 정책 적용 시) | P2 — 실패 경로에서 `resolve` 미호출 분기 |

### 7.1 본 슬라이스 최소 커버리지 (Gate)

| 모듈 | 최소 line/branch |
|------|------------------|
| `boundary_validator.py` (가칭) — size 검사 함수 | **100% branch** on size failure paths |
| `magic_square_control.py` — FR-01 실패 분기 | **해당 분기 100%** |

전체 리포지토리 80% (`.cursor/rules` REFACTOR)와 **충돌 시 PRD §14 (95/85) 우선**.

---

## 8. pytest-cov 측정 전략

### 8.1 설치

```bash
pip install pytest pytest-cov pydantic
```

### 8.2 기본 실행 (로컬)

```bash
pytest --cov=src --cov-report=term-missing
```

### 8.3 FR-01 크기 검증 슬라이스만 (권장 CI 단계)

```bash
pytest tests/unit/boundary/test_input_size_validation.py \
  --cov=src/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 8.4 Domain 95% 게이트 (Track B 병행 후 전체)

```bash
pytest tests/unit/entity tests/unit/control \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 8.5 설정 파일 (권장 `pyproject.toml` 초안)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
show_missing = true
fail_under = 85  # Boundary gate; Domain은 별도 job에서 95
```

### 8.6 측정 해석

| 리포트 항목 | QA 확인 |
|-------------|---------|
| `term-missing` 미커버 라인 | size 검사 `else` 누락 여부 |
| Branch coverage | `None` / `[]` / ragged row 분기 각각 실행 여부 |
| `src/entity` 실행 라인 | FR-01 실패 테스트 실행 시 **0**이 이상적 (해당 테스트만 단독 실행 시) |

### 8.7 Dual-Track 실행 순서 (TDD)

1. **RED:** TC-SIZE-001 (`None`) — 실패 확인  
2. **GREEN:** 최소 size 검사 구현  
3. **RED:** TC-SIZE-002~006 + AC-FR01-05 spy  
4. **GREEN:** 일반화된 `is_valid_4x4_shape`  
5. **REFACTOR:** 커버리지 gate 통과, 테스트 삭제/완화 금지  

---

## 9. 추적성 (Traceability)

| Concept | Rule | FR | AC | Error | Test Data | TC ID |
|---------|------|-----|-----|-------|-----------|-------|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01 | INVALID_SIZE / E-BND-001 | `None` | TC-SIZE-001 |
| Boundary 격리 | — | FR-01 | AC-FR01-05 | — | — | 모든 TC-SIZE/EX |
| Invalid size | BR-01 | FR-01 | AC-FR01-01 | E-BND-001 | TD-03 | TC-SIZE-004 |
| Track A RED | §15.1 | FR-01 | AC-FR01-01, 05 | — | ES-01 | TC-SIZE-004 |

---

## 10. 승인·변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | 초안 — AC-FR01-01 앵커, 경계값·mock·cov 전략 |

---

## 부록 A — PRD 코드 매핑

| 구현 (본 계획) | PRD §13 |
|----------------|---------|
| `INVALID_SIZE` | `E-BND-001` |
| `Grid must be 4x4.` | `Input matrix must be 4x4.` |

## 부록 B — 제외 케이스 명시 (재확인)

**다음은 AC-FR01-01 테스트 플랜에 포함하지 않는다.**

- `grid` = 유효 4×4 행렬 (예: TD-01, TD-02) — FR-01 **성공** 경로  
- 빈칸 2개·값 범위·중복 — AC-FR01-02 ~ 04  
- `E-DOM-001` — FR-05 / TD-07  

---

*End of Test Plan*
