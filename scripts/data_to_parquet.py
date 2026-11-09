
import re
import argparse
import polars as pl
from pathlib import Path

FEATURES = [
    "lp", "v", "GTT", "GTn", "GGn",
    "Ts", "Tp", "T48", "T1", "T2",
    "P48", "P1", "P2", "Pexh", "TIC",
    "mf", "GT_compressor_decay", "GT_turbine_decay",
]

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_path",
        type=str,
        nargs="?",
        default="data/data.txt",
    )

    parser.add_argument(
        "output_path",
        type=str,
        nargs="?",
        default="data/data.parquet",
    )

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()

    with open(args.input_path, "r") as f:
        content = f.read()
    
    content = re.sub(r"[   ]+", ",", content.strip())
    content = re.sub(r"\n,", "\n", content)

    df = pl.read_csv(
        content.encode(),
        has_header=False,
        new_columns=FEATURES,
        schema_overrides={col: pl.Float64 for col in FEATURES},
    )

    df.write_parquet(args.output_path, compression="zstd")
    print(f"Saved {df.height} rows to {args.output_path}")
