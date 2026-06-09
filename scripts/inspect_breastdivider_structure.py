from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


NIFTI_SUFFIXES = (".nii", ".nii.gz")


def is_nifti(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(NIFTI_SUFFIXES)


def classify_path(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()

    if "lesion_annotations" in parts:
        return "lesion_annotation"
    if "labelstr" in "".join(parts) or "labels" in "".join(parts):
        return "left_right_mask"
    if "imagestr" in "".join(parts) or "images" in "".join(parts):
        return "image"
    if is_nifti(path):
        return "nifti_unknown"
    if name.endswith(".csv"):
        return "csv"
    if name.endswith(".json"):
        return "json"
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect local BreastDivider folder structure without heavy dependencies."
    )
    parser.add_argument(
        "dataset_dir",
        type=Path,
        help="Path to local BreastDividerDataset directory.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("outputs/breastdivider_eda/file_inventory.csv"),
        help="CSV inventory output path.",
    )
    args = parser.parse_args()

    dataset_dir = args.dataset_dir.resolve()
    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory does not exist: {dataset_dir}")

    files = [p for p in dataset_dir.rglob("*") if p.is_file()]
    by_kind = Counter()
    by_suffix = Counter()
    top_dirs = Counter()

    rows = []
    for path in files:
        rel = path.relative_to(dataset_dir)
        kind = classify_path(rel)
        by_kind[kind] += 1
        by_suffix[".nii.gz" if path.name.lower().endswith(".nii.gz") else path.suffix.lower()] += 1
        top_dirs[rel.parts[0] if rel.parts else "."] += 1
        rows.append(
            {
                "relative_path": str(rel).replace("\\", "/"),
                "kind": kind,
                "size_bytes": path.stat().st_size,
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["relative_path", "kind", "size_bytes"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset dir: {dataset_dir}")
    print(f"Files total: {len(files)}")
    print("")
    print("By kind:")
    for key, value in by_kind.most_common():
        print(f"  {key}: {value}")
    print("")
    print("By suffix:")
    for key, value in by_suffix.most_common():
        print(f"  {key or '<none>'}: {value}")
    print("")
    print("Top-level dirs/files:")
    for key, value in top_dirs.most_common(20):
        print(f"  {key}: {value}")
    print("")
    print(f"Inventory written to: {args.out}")


if __name__ == "__main__":
    main()
