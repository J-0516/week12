import pandas as pd
import pytest

df = pd.read_csv("scores_2026.csv", encoding="utf-8")

print("행과 열:", df.shape)
print("점수 빈칸:", df["점수"].isna().sum())
print("중복 행:", df.duplicated().sum())
print("반 종류:", df["반"].unique())
print("과목 종류:", df["과목"].unique())
print("점수 통계:\n", df["점수"].describe())

def clean_data(data):
    required_columns = {"반", "과목", "점수"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        missing_names = ", ".join(sorted(missing_columns))
        raise ValueError(f"필수 열이 없습니다: {missing_names}")

    cleaned_df = data.copy()

    cleaned_df = cleaned_df.dropna(subset=["점수"])
    print(f"점수 빈칸 삭제 후: {len(cleaned_df)}행")

    cleaned_df = cleaned_df.drop_duplicates()
    print(f"중복 행 삭제 후: {len(cleaned_df)}행")

    cleaned_df["반"] = cleaned_df["반"].str.strip()
    cleaned_df["과목"] = cleaned_df["과목"].str.strip()
    print(f"반·과목 공백 제거 후: {len(cleaned_df)}행")

    cleaned_df["점수"] = pd.to_numeric(cleaned_df["점수"], errors="raise")
    valid_scores = (
        cleaned_df["점수"].between(0, 100)
        & cleaned_df["점수"].mod(1).eq(0)
    )
    cleaned_df = cleaned_df.loc[valid_scores].copy()
    cleaned_df["점수"] = cleaned_df["점수"].astype(int)
    print(f"0~100 사이 정수 범위 밖 점수 삭제 후: {len(cleaned_df)}행")

    return cleaned_df


cleaned_df = clean_data(df)
print("정제 후 행 수:", len(cleaned_df))

# ① 과목이 수학인 행만 필터링하고 행 수를 출력합니다.
math_df = cleaned_df[cleaned_df["과목"] == "수학"]
print("수학 행 수:", len(math_df))

# ② 반별 평균과 과목·반별 평균을 각각 계산합니다.
class_average = cleaned_df.groupby("반")["점수"].mean()
subject_class_average = cleaned_df.groupby(["과목", "반"])["점수"].mean()
print("반별 평균:")
print(class_average)
print("과목·반별 평균:")
print(subject_class_average)

# ③ 반별 개수, 평균, 중앙값, 최댓값을 한 표로 출력합니다.
class_statistics = (
    cleaned_df.groupby("반")["점수"]
    .agg(["count", "mean", "median", "max"])
    .rename(columns={
        "count": "개수",
        "mean": "평균",
        "median": "중앙값",
        "max": "최댓값",
    })
    .round(2)
)
print(class_statistics)

# ④ 반별 합계와 전체 합계, 행 개수가 일치하는지 확인합니다.
grouped_score_total = cleaned_df.groupby("반")["점수"].sum().sum()
overall_score_total = cleaned_df["점수"].sum()
grouped_row_count = cleaned_df.groupby("반")["점수"].count().sum()
print("그룹별 점수 합계:", grouped_score_total)
print("전체 점수 합계:", overall_score_total)
print("점수 합계 일치:", grouped_score_total == overall_score_total)
print("그룹별 개수 합계:", grouped_row_count)
print("전체 행 개수:", len(cleaned_df))

# ⑤ 1반 수학 점수의 개수와 평균을 그룹화 결과와 비교합니다.
spot_check_scores = cleaned_df.loc[
    (cleaned_df["반"] == "1반") & (cleaned_df["과목"] == "수학"),
    "점수",
]
if spot_check_scores.empty:
    raise ValueError("스팟 체크 대상인 1반 수학 데이터가 없습니다.")

spot_check_average = round(spot_check_scores.mean(), 2)
grouped_average = subject_class_average.loc[("수학", "1반")]
print(spot_check_scores)
print("1반 수학 점수 개수:", len(spot_check_scores))
print("직접 계산한 평균:", spot_check_average)
print("그룹화 결과 평균:", grouped_average)
