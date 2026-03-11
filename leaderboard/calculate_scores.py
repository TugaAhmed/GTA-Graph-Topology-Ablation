from pathlib import Path
import pandas as pd
from sklearn.metrics import f1_score

# Ground truth labels for evaluation
GROUND_TRUTH = Path(__file__).resolve().parent.parent / "data" / "train.csv"


def calculate_scores(submission_path: Path):

    submission_df = pd.read_csv(submission_path)
    gt_df = pd.read_csv(GROUND_TRUTH)

    # Ensure required columns exist
    required_cols = ["graph_index", "label"]

    for col in required_cols:
        if col not in submission_df.columns:
            raise ValueError(f"Submission missing column: {col}")

    # Merge predictions with ground truth
    merged = submission_df.merge(
        gt_df,
        on="graph_index",
        suffixes=("_pred", "_true")
    )

    y_pred = merged["label_pred"]
    y_true = merged["label_true"]

    f1 = f1_score(y_true, y_pred)

    return {
        "validation_f1_score": f1
    }
