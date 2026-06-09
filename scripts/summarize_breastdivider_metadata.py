from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def find_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized = {c.lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    for column in columns:
        low = column.lower()
        if any(candidate.lower() in low for candidate in candidates):
            return column
    return None


def write_counts(path: Path, title: str, counter: Counter[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([title, "count"])
        for key, value in counter.most_common():
            writer.writerow([key, value])


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize BreastDivider metadata CSV files.")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("data/BreastDividerDataset"),
        help="Local BreastDividerDataset directory.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/breastdivider_eda"),
        help="Output directory.",
    )
    args = parser.parse_args()

    dataset_dir = args.dataset_dir
    mapping_path = dataset_dir / "breastdivider_id_mapping.csv"
    classification_path = dataset_dir / "lesion_annotations" / "classification" / "classification.csv"

    args.out_dir.mkdir(parents=True, exist_ok=True)

    if not mapping_path.exists():
        raise SystemExit(f"Missing mapping CSV: {mapping_path}")

    mapping = read_csv(mapping_path)
    columns = list(mapping[0].keys()) if mapping else []
    print(f"Mapping rows: {len(mapping)}")
    print(f"Mapping columns: {columns}")

    source_col = find_column(columns, ["source_dataset", "dataset", "collection", "source"])
    modality_col = find_column(columns, ["modality", "sequence", "series", "contrast", "phase"])
    id_col = find_column(columns, ["breastdivider_id", "id", "case"])
    original_id_col = find_column(columns, ["original_id", "patient", "study", "subject"])

    if source_col:
        counts = Counter(row.get(source_col, "") or "<missing>" for row in mapping)
        write_counts(args.out_dir / "metadata_source_counts.csv", source_col, counts)
        print(f"Source counts written: {args.out_dir / 'metadata_source_counts.csv'}")
    else:
        print("Could not infer source dataset column.")

    if modality_col:
        counts = Counter(row.get(modality_col, "") or "<missing>" for row in mapping)
        write_counts(args.out_dir / "metadata_modality_counts.csv", modality_col, counts)
        print(f"Modality/phase counts written: {args.out_dir / 'metadata_modality_counts.csv'}")
    else:
        print("Could not infer modality/phase column.")

    summary_path = args.out_dir / "metadata_summary.txt"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write(f"Mapping rows: {len(mapping)}\n")
        f.write(f"Mapping columns: {columns}\n")
        f.write(f"Inferred ID column: {id_col}\n")
        f.write(f"Inferred original ID column: {original_id_col}\n")
        f.write(f"Inferred source column: {source_col}\n")
        f.write(f"Inferred modality/phase column: {modality_col}\n")
        f.write("\n")

        if classification_path.exists():
            classification = read_csv(classification_path)
            class_columns = list(classification[0].keys()) if classification else []
            f.write(f"Classification rows: {len(classification)}\n")
            f.write(f"Classification columns: {class_columns}\n")
            print(f"Classification rows: {len(classification)}")
            print(f"Classification columns: {class_columns}")
        else:
            f.write(f"Classification CSV not found: {classification_path}\n")
            print(f"Classification CSV not found: {classification_path}")

    print(f"Summary written: {summary_path}")


if __name__ == "__main__":
    main()
