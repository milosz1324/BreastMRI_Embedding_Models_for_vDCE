from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from tqdm import tqdm


IMAGE_RE = re.compile(r"BreastDivider_(\d{5})_0000\.nii\.gz$")


def find_pairs(dataset_dir: Path) -> list[tuple[str, Path, Path]]:
    pairs: list[tuple[str, Path, Path]] = []

    for image_path in sorted(dataset_dir.glob("imagesTr_batch*/BreastDivider_*_0000.nii.gz")):
        match = IMAGE_RE.search(image_path.name)
        if not match:
            continue

        case_id = match.group(1)
        batch_name = image_path.parent.name.replace("imagesTr", "labelsTr")
        label_path = dataset_dir / batch_name / f"BreastDivider_{case_id}.nii.gz"
        if label_path.exists():
            pairs.append((case_id, image_path, label_path))

    return pairs


def robust_normalize(slice_2d: np.ndarray) -> np.ndarray:
    finite = slice_2d[np.isfinite(slice_2d)]
    if finite.size == 0:
        return np.zeros_like(slice_2d, dtype=np.float32)

    lo, hi = np.percentile(finite, [1, 99])
    if hi <= lo:
        hi = float(np.max(finite))
        lo = float(np.min(finite))
    if hi <= lo:
        return np.zeros_like(slice_2d, dtype=np.float32)

    out = (slice_2d.astype(np.float32) - lo) / (hi - lo)
    return np.clip(out, 0.0, 1.0)


def best_slice(mask: np.ndarray) -> tuple[int, int]:
    """Return axis and slice index with the largest left/right breast mask area."""
    binary = mask > 0
    best_axis = 0
    best_idx = 0
    best_area = -1

    for axis in range(3):
        areas = np.sum(binary, axis=tuple(i for i in range(3) if i != axis))
        idx = int(np.argmax(areas))
        area = int(areas[idx])
        if area > best_area:
            best_axis = axis
            best_idx = idx
            best_area = area

    return best_axis, best_idx


def take_slice(volume: np.ndarray, axis: int, idx: int) -> np.ndarray:
    if axis == 0:
        return volume[idx, :, :]
    if axis == 1:
        return volume[:, idx, :]
    return volume[:, :, idx]


def foreground_slice_counts(mask: np.ndarray) -> tuple[int, int, int]:
    binary = mask > 0
    counts = []
    for axis in range(3):
        areas = np.sum(binary, axis=tuple(i for i in range(3) if i != axis))
        counts.append(int(np.sum(areas > 0)))
    return tuple(counts)


def plot_case(
    case_id: str,
    image: np.ndarray,
    mask: np.ndarray,
    axis: int,
    idx: int,
    out_path: Path,
) -> None:
    image_slice = np.rot90(take_slice(image, axis, idx))
    mask_slice = np.rot90(take_slice(mask, axis, idx))
    image_norm = robust_normalize(image_slice)

    left_mask = mask_slice == 1
    right_mask = mask_slice == 2

    overlay = np.dstack([image_norm, image_norm, image_norm])
    overlay[left_mask, 0] = 1.0
    overlay[left_mask, 1] *= 0.25
    overlay[left_mask, 2] *= 0.25
    overlay[right_mask, 0] *= 0.25
    overlay[right_mask, 1] *= 0.45
    overlay[right_mask, 2] = 1.0

    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)

    axes[0].imshow(image_norm, cmap="gray")
    axes[0].set_title("MRI slice")
    axes[0].axis("off")

    axes[1].imshow(overlay)
    axes[1].set_title("MRI + left/right mask")
    axes[1].axis("off")

    axes[2].imshow(mask_slice, cmap="tab10", vmin=0, vmax=9)
    axes[2].set_title("Mask labels")
    axes[2].axis("off")

    fig.suptitle(f"BreastDivider_{case_id}, axis={axis}, slice={idx}", fontsize=11)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize local BreastDivider sample pairs.")
    parser.add_argument(
        "dataset_dir",
        type=Path,
        default=Path("data/BreastDividerDataset"),
        nargs="?",
        help="Path to local BreastDividerDataset directory.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of cases to visualize.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/breastdivider_eda/visualizations"),
        help="Output directory for PNG visualizations.",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("outputs/breastdivider_eda/sample_visual_summary.csv"),
        help="CSV summary output path.",
    )
    args = parser.parse_args()

    dataset_dir = args.dataset_dir.resolve()
    pairs = find_pairs(dataset_dir)
    if not pairs:
        raise SystemExit(
            "No image/mask pairs found. Expected paths like "
            "imagesTr_batch1/BreastDivider_00001_0000.nii.gz and "
            "labelsTr_batch1/BreastDivider_00001.nii.gz"
        )

    rows = []
    for case_id, image_path, label_path in tqdm(pairs[: args.limit], desc="Visualizing cases"):
        image = np.asanyarray(nib.load(str(image_path)).dataobj)
        mask = np.asanyarray(nib.load(str(label_path)).dataobj)

        if image.shape != mask.shape:
            print(f"WARNING: shape mismatch for {case_id}: image={image.shape}, mask={mask.shape}")

        axis, idx = best_slice(mask)
        output_path = args.out_dir / f"BreastDivider_{case_id}_overlay.png"
        plot_case(case_id, image, mask, axis, idx, output_path)

        labels, counts = np.unique(mask, return_counts=True)
        label_counts = ";".join(f"{int(label)}:{int(count)}" for label, count in zip(labels, counts))
        fg_counts = foreground_slice_counts(mask)

        rows.append(
            {
                "case_id": case_id,
                "image_path": str(image_path.relative_to(dataset_dir)).replace("\\", "/"),
                "label_path": str(label_path.relative_to(dataset_dir)).replace("\\", "/"),
                "image_shape": "x".join(map(str, image.shape)),
                "mask_shape": "x".join(map(str, mask.shape)),
                "selected_axis": axis,
                "selected_slice": idx,
                "foreground_slices_axis0": fg_counts[0],
                "foreground_slices_axis1": fg_counts[1],
                "foreground_slices_axis2": fg_counts[2],
                "label_counts": label_counts,
                "visualization": str(output_path).replace("\\", "/"),
            }
        )

    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Pairs found: {len(pairs)}")
    print(f"Cases visualized: {len(rows)}")
    print(f"Visualizations written to: {args.out_dir}")
    print(f"Summary written to: {args.summary}")


if __name__ == "__main__":
    main()
