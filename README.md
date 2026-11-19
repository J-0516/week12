# week12

## 데이터

- **출처:** 주어진 실습용 데이터(`scores_2026.csv`). 외부 공개 데이터셋이나 별도 원문 출처 링크는 제공되지 않았습니다.
- **저장소 주소:** https://github.com/J-0516/week12
- **행 수:** 원본 데이터는 114행이며, 열 이름을 제외한 데이터 행은 114개입니다.
- **열 수:** 5열

| 열 | 설명 |
|---|---|
| `학번` | 학생 번호로 문자형 식별자에 가깝게 읽습니다. |
| `이름` | 학생 이름을 나타냅니다. |
| `반` | 학생이 속한 반으로, 정제 후 `1반` 또는 `2반`만 유지합니다. |
| `과목` | `수학`, `영어`, `프로그래밍` 과목을 나타냅니다. |
| `점수` | 0~100 사이의 정수 점수입니다. |

### 빈 칸 처리

원본의 `점수` 열에는 빈 칸이 6개 있습니다. 빈 칸은 점수가 0점이거나 결측치를 0으로 대체한 것이 아니며, 점수 평균 계산이 가능한 유효한 관측치가 아니므로 `dropna(subset=["점수"])`로 해당 행을 삭제했습니다.

평균에 값을 대입하는 방식은 일부러 삽입된 빈 칸의 의미를 추정하거나 평균을 왜곡할 수 있으므로 사용하지 않았습니다. 이 규칙을 적용하면 빈 칸이 있는 6개 행이 제거됩니다.

### 정제 조건

- `점수`가 없는 행 삭제
- 완전히 동일한 중복 행 삭제
- `반`과 `과목` 문자열 양 끝의 공백 제거
- `점수`를 수치형으로 변환한 뒤 0 이상 100 이하의 정수만 유지
- 정제 후 정확히 100행이 남는지 확인

## 파일 목록

| 파일 | 내용 |
|---|---|
| `scores_2026.csv` | 실습용 성적 데이터. **114행 5열**, UTF-8. 일부러 지저분하게 만들어져 있습니다. |
| `scores_2026_cp949.csv` | 위와 내용이 같고 인코딩만 CP949. 인코딩 오류를 겪어 보는 용도입니다. |
| `mini.csv` | 손계산 검증용 **10행** 데이터. |
| `prompts.txt` | 오늘 AI에게 줄 프롬프트 원문 (A~E). |
| `analysis.py` | CSV 데이터를 정제하고, 필터링·그룹화·통계 분석 결과를 출력합니다. |
| `test_analysis.py` | `analysis.py`의 정제 결과와 주요 집계값을 pytest로 검증합니다. |

## scores_2026.csv 의 열

| 열 | 뜻 | 자료형 |
|---|---|---|
| 학번 | 학생 번호 | 문자 |
| 이름 | 학생 이름 | 문자 |
| 반 | 1반 또는 2반 | 문자 |
| 과목 | 프로그래밍 · 영어 · 수학 | 문자 |
| 점수 | 0~100 사이의 정수 | 정수 |

## 일부러 넣어 둔 오염 (정답은 보지 말고 직접 찾아보세요)

<details>
<summary>펼쳐 보기</summary>

- 점수가 비어 있는 행 **6개**
- 모든 열이 완전히 같은 중복 행 **4개**
- 점수가 0~100 밖인 행 **4개** (999 세 개, -5 하나)
- 반 이름 뒤에 공백이 붙은 행 2개, 과목 이름 뒤에 공백이 붙은 행 1개

→ 규칙대로 정제하면 **정확히 100행**이 남습니다.
→ 정제 후 반은 2종류, 과목은 3종류가 됩니다.

</details>

## mini.csv 의 정답

<details>
<summary>먼저 종이로 풀고 나서 펼쳐 보세요</summary>

- 정제 후 **7행**
- 1반 평균 **80.0** (4명, 합계 320)
- 2반 평균 **70.0** (3명, 합계 210)

</details>

### 결론

점수 누락·중복·범위 밖 데이터를 정제한 뒤, 과목을 구분하지 않고 전체 점수의 단순 평균으로 비교하면 1반은 78.24점으로 2반의 71.44점보다 6.80점 높아 전체 평균 기준에서는 1반이 더 잘했다고 볼 수 있습니다. 다만 과목별 평균은 2반이 수학·영어·프로그래밍 모두에서 더 높았고, 두 반의 과목별 점수 개수도 서로 달랐으므로 전체 평균만으로 어느 반이 모든 과목에서 더 우수하다고 단정하기는 어렵습니다.

현재 pytest 테스트 4개는 정제 후 100행·두 반 유지·점수 합계 일치와 `mini.csv`의 1반 평균을 확인하며, 어느 반의 전체 평균이 높은지는 별도의 비교 분석 결과입니다.

### 라이선스
MIT License

Copyright (c) 2026 장준호

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
