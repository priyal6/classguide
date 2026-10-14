import json
from dataclasses import dataclass
from os import path
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

@dataclass(fronzen=True)
class TrainingConfig:
    data_path: Path
    output_dir: Path
    test_size: float = 0.2
    random_state: int = 42

    def __post_init__(self) -> None:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.data_path}")
        if self.data_path.suffix != ".csv":
            raise ValueError("data_path must point to a CSV file")
        if not self.output_dir.parent.exists():
            raise FileNotFoundError(
                f"Parent directory for output_dir does not exist: {self.output_dir.parent}"
            )
        if not 0 < self.test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
        if self.random_state < 0:
            raise ValueError("random_state must be >=0")

    def make_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def model_path(self) -> Path:
        return self.output_dir / "churn_model.joblib"

    @property
    def metrics_path(self) -> Path:
        return self.output_dir / "metrics.json"

    @property
    def importances_path(self) -> Path:
        return self.output_dir / "feature_importances.json"



   
def load_data(path: Path) -> pd.DataFrame:
     return pd.read_csv(path)

#preprocessing

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates(subset=["customer_id"])
    cleaned = cleaned.dropna(subset=["churn"])

    cleaned["tenure"] = cleaned["tenure"].fillna(cleaned["tenure"].median())
    cleaned["monthly_charges"] = cleaned["monthly_charges"].fillna(cleaned["monthly_charges"].median())
    return cleaned

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df.copy()

    featured["chargres_per_ticket"] = featured["monthly_charges"] / (
        featured["support_tickets"] + 1
    )
    featured["is_senior"] = (featured["age"] >= 65).astype(int)
    featured["is_new_customer"] = (featured["tenure"]< 6).astype(int)

    return featured

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    return pd.get_dummies(
        df,
        columns=["contract_type", "internet_service", "payment_method"],
        drop_first=True
    )

def split_features_and_target(
        df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=["customer_id", "churn"])
    y = df["churn"]
    return X, y 


def split_data(
        X: pd.DataFrame,
        y: pd.Series,
        *,
        test_size: float,
        random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

def build_model(random_state: int) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=random_state,
    )

def train_model(
        model: RandomForestClassifier,
        X_train: pd.DataFrame,
        y_train: pd.Series, 
) -> None:
    model.fit(X_train, y_train)

def evaluate_model(
        model: RandomForestClassifier,
        X_test: pd.DataFrame,
        y_test: pd.Series,
) -> dict[str, object]:
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)

    return {
        "accuracy": accuracy,
        "classification_report": report,
    }

def compute_feature_importances(
        model: RandomForestClassifier,
        feature_names: list[str]
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

def save_artifacts(
        config: TrainingConfig,
        model: RandomForestClassifier,
        metrics: dict[str, object],
        importances: pd.DataFrame,
) -> None:
    config.make_output_dir()

    joblib.dump(model, config.model_path)

    with config.metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    importances.to_csv(config.importances_path, index=False)

    