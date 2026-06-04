import pandas as pd
from pathlib import Path


def export_data(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(output_path)
    print(f"Saved: {output_path}  |  Shape: {df.shape}")