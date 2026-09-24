#!/usr/bin/env python3
"""Reproducible hourly-load baselines for the next group meeting.

Expected input columns:
    timestamp,power_mw

If no input file is present, a clearly labelled synthetic dataset is generated
only to test the pipeline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def generate_demo_data(path: Path, hours: int = 24 * 60) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    timestamp = pd.date_range("2026-01-01", periods=hours, freq="h", tz="Europe/London")
    step = np.arange(hours)
    hour = timestamp.hour.to_numpy()
    weekday = timestamp.dayofweek.to_numpy()

    daily = 7.5 * np.sin(2 * np.pi * (hour - 8) / 24)
    workday = np.where(weekday < 5, 3.0, -2.0)
    weekly = 1.8 * np.sin(2 * np.pi * step / (24 * 7))
    trend = 0.004 * step
    noise = rng.normal(0, 1.1, hours)
    power_mw = 45 + daily + workday + weekly + trend + noise

    frame = pd.DataFrame({"timestamp": timestamp, "power_mw": power_mw})
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return frame


def load_data(path: Path) -> tuple[pd.DataFrame, bool]:
    synthetic = not path.exists()
    frame = generate_demo_data(path) if synthetic else pd.read_csv(path)

    required = {"timestamp", "power_mw"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Input is missing columns: {sorted(missing)}")

    frame = frame.loc[:, ["timestamp", "power_mw"]].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="raise")
    frame["power_mw"] = pd.to_numeric(frame["power_mw"], errors="raise")
    frame = frame.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    frame = frame.reset_index(drop=True)
    if len(frame) < 24 * 21:
        raise ValueError("At least 21 days of hourly data are required for this demo pipeline")
    return frame, synthetic


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["lag_24"] = result["power_mw"].shift(24)
    result["lag_168"] = result["power_mw"].shift(168)
    return result.dropna().reset_index(drop=True)


def linear_prediction(train: pd.DataFrame, test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    features = ["lag_24", "lag_168"]
    x_train = np.column_stack([np.ones(len(train)), train[features].to_numpy()])
    y_train = train["power_mw"].to_numpy()
    coefficients, *_ = np.linalg.lstsq(x_train, y_train, rcond=None)

    x_test = np.column_stack([np.ones(len(test)), test[features].to_numpy()])
    return x_test @ coefficients, coefficients


def score(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    error = actual - predicted
    safe_actual = np.where(np.abs(actual) > 1e-9, np.abs(actual), np.nan)
    return {
        "MAE_MW": float(np.mean(np.abs(error))),
        "RMSE_MW": float(np.sqrt(np.mean(error**2))),
        "MAPE_percent": float(np.nanmean(np.abs(error) / safe_actual) * 100),
    }


def run(input_path: Path, output_dir: Path, test_hours: int) -> None:
    frame, synthetic = load_data(input_path)
    featured = add_features(frame)
    if len(featured) <= test_hours + 24:
        raise ValueError("Not enough rows remain after lag creation for the requested test horizon")

    train = featured.iloc[:-test_hours].copy()
    test = featured.iloc[-test_hours:].copy()

    test["previous_day"] = test["lag_24"]
    test["previous_week"] = test["lag_168"]
    test["lag_mean"] = 0.5 * test["lag_24"] + 0.5 * test["lag_168"]
    test["linear_regression"], coefficients = linear_prediction(train, test)

    models = ["previous_day", "previous_week", "lag_mean", "linear_regression"]
    actual = test["power_mw"].to_numpy()
    metrics = []
    for model in models:
        metrics.append({"model": model, **score(actual, test[model].to_numpy())})

    output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(metrics).sort_values("RMSE_MW").to_csv(output_dir / "metrics.csv", index=False)
    test.rename(columns={"power_mw": "actual_power_mw"}).to_csv(
        output_dir / "predictions.csv", index=False
    )

    summary = {
        "input_file": str(input_path),
        "synthetic_demo_data": synthetic,
        "measurement_boundary": "PCC / grid-connection active power",
        "resolution": "hourly",
        "split": {
            "method": "chronological",
            "train_rows": len(train),
            "test_rows": len(test),
            "test_start": str(test["timestamp"].iloc[0]),
            "test_end": str(test["timestamp"].iloc[-1]),
        },
        "linear_coefficients": {
            "intercept": float(coefficients[0]),
            "lag_24": float(coefficients[1]),
            "lag_168": float(coefficients[2]),
        },
        "warning": "Synthetic results validate code only and are not research evidence." if synthetic else None,
    }
    (output_dir / "model_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(test["timestamp"], test["power_mw"], label="Actual", color="#111827", linewidth=2)
    ax.plot(
        test["timestamp"],
        test["linear_regression"],
        label="Linear regression",
        color="#2563eb",
        linewidth=1.5,
    )
    ax.plot(
        test["timestamp"],
        test["previous_day"],
        label="Previous day",
        color="#f59e0b",
        linewidth=1.1,
        alpha=0.8,
    )
    title_prefix = "SYNTHETIC DEMO — " if synthetic else ""
    ax.set_title(f"{title_prefix}Hourly PCC active-power forecast")
    ax.set_xlabel("Time")
    ax.set_ylabel("Active power (MW)")
    ax.grid(alpha=0.2)
    ax.legend(ncol=3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_dir / "forecast_plot.png", dpi=180)
    plt.close(fig)

    print(f"Input: {input_path}")
    print(f"Synthetic demo: {synthetic}")
    print(pd.DataFrame(metrics).sort_values("RMSE_MW").to_string(index=False))
    print(f"Outputs: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "hourly_load.csv",
        help="CSV with timestamp,power_mw columns",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "research" / "outputs",
        help="Directory for metrics, predictions, summary and plot",
    )
    parser.add_argument("--test-hours", type=int, default=168, help="Final chronological test window")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.input, args.output_dir, args.test_hours)
