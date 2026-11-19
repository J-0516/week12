from pathlib import Path
import pytest

import pandas as pd

from analysis import clean_data


data_dir = Path(__file__).resolve().parent
scores_df = pd.read_csv(data_dir / "scores_2026.csv", encoding="utf-8")
mini_df = pd.read_csv(data_dir / "mini.csv", encoding="utf-8")

cleaned_scores_df = clean_data(scores_df)
cleaned_mini_df = clean_data(mini_df)


def test_clean_data_leaves_100_rows():
    assert len(cleaned_scores_df) == 100


def test_clean_data_keeps_only_two_classes():
    assert set(cleaned_scores_df["반"].unique()) == {"1반", "2반"}


def test_grouped_score_total_matches_overall_total():
    grouped_total = cleaned_scores_df.groupby("반")["점수"].sum().sum()
    overall_total = cleaned_scores_df["점수"].sum()
    assert grouped_total == overall_total


def test_mini_data_class_one_average_is_80():
    class_averages = cleaned_mini_df.groupby("반")["점수"].mean()
    assert class_averages["1반"] == 80.0
