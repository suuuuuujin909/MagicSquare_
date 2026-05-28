# MagicSquare_

4×4 마방진(1~16 배치, 행·열·대각선 합 동일)을 다루는 프로그램 프로젝트입니다.  
현재 단계는 **문제 인식·정의**이며, 구현 코드는 아직 포함하지 않습니다.

## 프로젝트 목표

「마방진 그림을 만드는 것」이 아니라, **4×4에 1~16을 배치했을 때 다중 제약(합·중복·범위)을 명시적 규칙으로 일관되게 판정·반복·고정하는 것**이 핵심 과제입니다.  
프로그램과 TDD는 손검산의 변동을 줄이고, 완성(전 제약 동시 만족)의 기준이 흔들리지 않게 하기 위한 수단으로 둡니다.

## 저장소 구조

```
MagicSquare_/
├── README.md
├── Report/
│   └── 01.MagicSquare-Problem-Definition-Report.md   # STEP 1~5 문제 정의 보고서
└── Prompting/
    └── 01.cursor_4x4_magic_square_problem_observa-prompt.md   # Cursor 대화·프롬프트 기록
```

## 문서

| 문서 | 설명 |
|------|------|
| [문제 정의 보고서](Report/01.MagicSquare-Problem-Definition-Report.md) | 관찰(STEP 1) → Why 체인(STEP 2~4) → 진짜 문제 정의(STEP 5) |
| [프롬프트 기록](Prompting/01.cursor_4x4_magic_square_problem_observa-prompt.md) | 문제 정의 단계를 진행한 Cursor 대화보내기 |

## 범위

**포함:** 문제 상황 관찰, 제약·불변식, 판정 기준, TDD 관점의 Why 정리  

**미포함 (다음 단계):** 구현 설계, 코드, 알고리즘, 인수 조건·입출력 계약 확정

## 다음 단계

- 사용 시나리오·인수 조건 정리
- 입출력 계약 확정 (검증 중심 vs 생성 포함, 진단 depth, 동치 정책)
- 첫 검증 명세 작성 (TDD RED 목록)

## 링크

- GitHub: https://github.com/suuuuuujin909/MagicSquare_
