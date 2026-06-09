from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ID_PATTERN = re.compile(r"(\d{5})")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def infer_breastdivider_id(row: dict[str, str]) -> str | None:
    for key, value in row.items():
        text = f"{key} {value}"
        if "BreastDivider_" in text:
            match = re.search(r"BreastDivider_(\d{5})", text)
            if match:
                return match.group(1)
    for value in row.values():
        if not value:
            continue
        match = ID_PATTERN.search(value)
        if match:
            return match.group(1)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a small Hugging Face download command for BreastDivider image/mask samples."
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=Path("data/BreastDividerDataset/breastdivider_id_mapping.csv"),
        help="Path to breastdivider_id_mapping.csv.",
    )
    parser.add_argument("--n", type=int, default=10, help="Number of cases to include.")
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        help="Batch number used in Hugging Face paths, e.g. 1 or 2.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("outputs/breastdivider_eda/sample_download_command.sh"),
        help="Output shell script path.",
    )
    args = parser.parse_args()

    if not args.mapping.exists():
        raise SystemExit(f"Missing mapping CSV: {args.mapping}")

    rows = read_csv(args.mapping)
    ids: list[str] = []
    seen = set()
    for row in rows:
        bid = infer_breastdivider_id(row)
        if bid and bid not in seen:
            seen.add(bid)
            ids.append(bid)
        if len(ids) >= args.n:
            break

    if not ids:
        ids = [f"{i:05d}" for i in range(1, args.n + 1)]

    includes = []
    for bid in ids:
        includes.append(f'"imagesTr_batch{args.batch}/BreastDivider_{bid}_0000.nii.gz"')
        includes.append(f'"labelsTr_batch{args.batch}/BreastDivider_{bid}.nii.gz"')

    command = [
        "hf download Bubenpo/BreastDividerDataset",
        "  --repo-type dataset",
        "  --local-dir data/BreastDividerDataset",
        "  --dry-run",
        "  --include \\",
    ]
    for idx, item in enumerate(includes):
        suffix = " \\" if idx < len(includes) - 1 else ""
        command.append(f"  {item}{suffix}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(command) + "\n", encoding="utf-8")

    print(f"Selected IDs: {', '.join(ids)}")
    print(f"Download command written to: {args.out}")
    print("Run it first with --dry-run. Remove --dry-run only after checking the size.")


if __name__ == "__main__":
    main()
