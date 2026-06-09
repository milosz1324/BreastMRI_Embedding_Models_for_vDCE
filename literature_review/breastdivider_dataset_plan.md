## BreastDivider dataset - plan rozpoznania

Ten dokument opisuje praktyczny plan Etapu 1: pobranie i rozpoznanie BreastDivider dataset.

## 1. Czy pobierac dataset lokalnie?

Tak, ale najlepiej etapowo.

BreastDivider jest duzym zbiorem 3D MRI, wiec nie warto zaczynac od pelnego pobrania wszystkiego bez sprawdzenia struktury, rozmiaru i potrzebnych plikow. Najpierw nalezy pobrac lub podejrzec strukture repozytorium/datasetu, a dopiero potem zdecydowac, czy pobieramy calosc, czy tylko wybrany batch/przykladowe przypadki.

Najlepszy workflow:

1. Utworzyc katalog `data/`, najlepiej nieuwzgledniany w git.
2. Pobrac najpierw metadane i/lub mala probe datasetu.
3. Sprawdzic strukture katalogow i nazewnictwo plikow.
4. Zweryfikowac, czy pliki zawieraja pary potrzebne do zadania vDCE: pre-contrast oraz post-contrast.
5. Dopiero potem pobrac wieksza czesc danych.

## 2. Proponowana struktura lokalna

```text
mgr/
├── data/
│   └── BreastDividerDataset/
├── scripts/
│   ├── inspect_breastdivider_structure.py
│   └── eda_nifti_summary.py
├── outputs/
│   └── breastdivider_eda/
└── requirements_eda.txt
```

Katalog `data/` powinien sluzyc tylko do lokalnych danych i nie powinien byc wysylany jako czesc pracy.

## 3. Pobieranie z Hugging Face

Dataset:

https://huggingface.co/datasets/Bubenpo/BreastDividerDataset

Po przygotowaniu srodowiska Python mozna uzyc:

```powershell
pip install -r requirements_eda.txt
huggingface-cli login
huggingface-cli download Bubenpo/BreastDividerDataset --repo-type dataset --local-dir data/BreastDividerDataset
```

Jesli dataset jest bardzo duzy, lepiej najpierw pobrac wybrane pliki lub katalogi, np. metadane, `dataset.json`, `lesion_annotations`, albo jeden batch obrazow/masek. Konkretne wzorce `--include` najlepiej dobrac po podejrzeniu zakladki "Files and versions" na Hugging Face.

Przyklad selektywnego pobierania:

```powershell
huggingface-cli download Bubenpo/BreastDividerDataset --repo-type dataset --local-dir data/BreastDividerDataset --include "dataset.json" "lesion_annotations/*"
```

Jesli pobieranie przez `huggingface-cli` nie zadziala, alternatywa to Git LFS:

```powershell
git lfs install
git clone https://huggingface.co/datasets/Bubenpo/BreastDividerDataset data/BreastDividerDataset
```

## 4. Co analizujemy w pierwszej kolejnosci?

Pierwsze pytania do datasetu:

1. Ile jest plikow obrazow `.nii` / `.nii.gz`?
2. Ile jest masek segmentacyjnych left/right?
3. Czy nazwy plikow pozwalaja rozpoznac pacjenta, dataset zrodlowy, modalnosc i faze kontrastowa?
4. Czy sa pary pre-contrast -> post-contrast?
5. Czy maski maja takie same rozmiary jak odpowiadajace obrazy?
6. Jakie sa rozmiary wolumenow, spacing i typ danych?
7. Ile slice'ow zawiera realna tkanke piersi, a ile jest pustych lub malo informacyjnych?
8. Czy sa lesion masks lub lesion labels dla przypadkow, ktore maja pary pre/post?

## 5. Minimalne EDA

Minimalny raport EDA powinien zawierac:

- liczbe przypadkow i plikow;
- strukture katalogow;
- liczbe obrazow i masek;
- liste zrodlowych kolekcji, np. Duke, MAMA-MIA, ISPY;
- statystyki shape i spacing;
- przykladowe slice'y z obrazem i maska;
- histogramy intensywnosci;
- wstepna liste kandydatow do par pre/post-contrast.

## 6. Decyzja po EDA

Po pierwszej analizie trzeba zdecydowac:

1. Czy BreastDivider zawiera wystarczajaco duzo par pre/post-contrast do trenowania vDCE?
2. Czy uzywamy calego BreastDivider, czy tylko podzbiorow takich jak Duke/MAMA-MIA?
3. Czy maski left/right sa bezposrednio uzyteczne do cropowania i wyboru slice'ow?
4. Czy lesion annotations sa wystarczajace do lesion-focused evaluation?
5. Czy pierwszym baseline'em powinien byc prosty 2D U-Net, czy najpierw autoencoder/embedding model?
