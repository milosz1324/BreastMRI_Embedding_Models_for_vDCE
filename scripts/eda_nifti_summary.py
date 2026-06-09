from __future__ import annotations

import argparse
import csv
from pathlib import Path

import nibabel as nib
import numpy as np
from tqdm import tqdm


NIFTI_SUFFIXES = (".nii", ".nii.gz")


def is_nifti(path: Path) -> bool:
    return path.name.lower().endswith(NIFTI_SUFFIXES)


def classify_path(path: Path) -> str:
    text = str(path).lower()
    if "lesion_annotations" in text:
        return "lesion_annotation"
    if "labels" in text or "labelstr" in text:
        return "left_right_mask"
    if "images" in text or "imagestr" in text:
        return "image"
    return "nifti_unknown"


def summarize_nifti(path: Path, dataset_dir: Path) -> dict[str, object]:
    img = nib.load(str(path))
    dataobj = img.dataobj
    shape = tuple(int(v) for v in img.shape)
    zooms = tuple(float(v) for v in img.header.get_zooms()[: len(shape)])
    dtype = str(dataobj.dtype)

    # Use a small sample for intensity stats to avoid loading huge volumes unnecessarily.
    arr = np.asanyarray(dataobj)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        stats = {"min": "", "p01": "", "mean": "", "p99": "", "max": ""}
    else:
        stats = {
            "min": float(np.min(finite)),
            "p01": float(np.percentile(finite, 1)),
            "mean": float(np.mean(finite)),
            "p99": float(np.percentile(finite, 99)),
            "max": float(np.max(finite)),
        }

    return {
        "relative_path": str(path.relative_to(dataset_dir)).replace("\\", "/"),
        "kind": classify_path(path.relative_to(dataset_dir)),
        "shape": "x".join(map(str, shape)),
        "zooms": "x".join(f"{z:.6g}" for z in zooms),
        "dtype": dtype,
        **stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize NIfTI files in BreastDivider.")
    parser.add_argument("dataset_dir", type=Path, help="Path to local BreastDividerDataset directory.")
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of NIfTI files to inspect. Use 0 for all files.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("outputs/breastdivider_eda/nifti_summary.csv"),
        help="CSV output path.",
    )
    args = parser.parse_args()

    dataset_dir = args.dataset_dir.resolve()
    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory does not exist: {dataset_dir}")

    nifti_files = [p for p in dataset_dir.rglob("*") if p.is_file() and is_nifti(p)]
    if args.limit and args.limit > 0:
        nifti_files = nifti_files[: args.limit]

    rows = []
    for path in tqdm(nifti_files, desc="Inspecting NIfTI"):
        try:
            rows.append(summarize_nifti(path, dataset_dir))
        except Exception as exc:
            rows.append(
                {
                    "relative_path": str(path.relative_to(dataset_dir)).replace("\\", "/"),
                    "kind": classify_path(path.relative_to(dataset_dir)),
                    "shape": "",
                    "zooms": "",
                    "dtype": "",
                    "min": "",
                    "p01": "",
                    "mean": "",
                    "p99": "",
                    "max": "",
                    "error": repr(exc),
                }
            )

    fieldnames = [
        "relative_path",
        "kind",
        "shape",
        "zooms",
        "dtype",
        "min",
        "p01",
        "mean",
        "p99",
        "max",
        "error",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"NIfTI files inspected: {len(rows)}")
    print(f"Summary written to: {args.out}")


if __name__ == "__main__":
    main()
