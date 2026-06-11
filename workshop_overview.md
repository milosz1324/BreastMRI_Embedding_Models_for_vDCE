# Sprawozdanie z pracowni problemowej magisterskiej

## Dane podstawowe

**Autor:** Miłosz Andruczyk

**Temat pracy:** Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis

**Obszar tematyczny:** sztuczna inteligencja, wizja komputerowa, obrazowanie medyczne, MRI piersi

**Opiekun pracy:** prof. Tomasz Trzciński

**Konsultacja merytoryczna:** prof. Andrzej Liebert

**Repozytorium projektu:** [https://github.com/milosz1324/BreastMRI_Embedding_Models_for_vDCE](https://github.com/milosz1324/BreastMRI_Embedding_Models_for_vDCE)

## Cel pracowni

Celem pracowni problemowej było przygotowanie podstaw teoretycznych i praktycznych do realizacji pracy magisterskiej dotyczącej modeli embeddingowych dla obrazów MRI piersi oraz ich wykorzystania w zadaniu syntezy wirtualnych obrazów dynamicznego wzmocnienia kontrastowego, czyli virtual DCE.

Główna motywacja pracy wynika z faktu, że dynamiczne obrazowanie kontrastowe MRI piersi jest istotne w diagnostyce raka piersi, ale wymaga podania środka kontrastowego. Metody uczenia maszynowego mogą potencjalnie umożliwić rekonstrukcję informacji kontrastowej na podstawie sekwencji niekontrastowych lub ograniczonego zestawu danych wejściowych. W pracy zaplanowane są eksperymenty, które mają na celu sprawdzenie czy reprezentacje embeddingowe uczone na pojedynczych przekrojach 2D MRI piersi mogą poprawić jakość i stabilność syntezy obrazów post-contrast w porównaniu z bezpośrednim podejściem image-to-image.

## Zakres wykonanych prac

W ramach pracowni wykonano dwa główne zadania:

1. Przegląd i opracowanie literatury związanej z tematem pracy.
2. Wstępne rozpoznanie datasetu BreastDivider oraz przygotowanie narzędzi do jego  analizy.

## Przegląd literatury

Przygotowano przegląd wybranych publikacji obejmujących najważniejsze obszary potrzebne do realizacji pracy:

- kliniczne znaczenie DCE-MRI piersi,
- syntezę obrazów kontrastowych i virtual DCE,
- cross-contrast MRI image synthesis,
- modele embeddingowe i foundation models w obrazowaniu medycznym,
- dataset BreastDivider oraz segmentację lewej i prawej piersi,
- metryki oceny jakości syntezy obrazów medycznych.

Wybrane artykuły zostały przeanalizowane według wspólnego szablonu oceny literatury. Dla każdego artykułu opisano problem badawczy, dane, metodę, sposób ewaluacji, najważniejsze wyniki oraz znaczenie publikacji dla planowanej pracy magisterskiej.

Opracowania literatury znajdują się w repozytorium w katalogu:

[literature_review/](https://github.com/milosz1324/BreastMRI_Embedding_Models_for_vDCE/tree/main/literature_review)

Opracowane zostały między innymi następujące publikacje:

- **Foundation Models in Medical Imaging: A Review and Outlook** - artykuł wykorzystany do uporządkowania pojęć takich jak foundation model, embedding, self-supervised learning i downstream task.
- **Vascularity and Dynamic Contrast-Enhanced Breast Magnetic Resonance Imaging** - artykuł dostarczający kontekstu klinicznego dla DCE-MRI piersi.
- **Synthesizing Late-Stage Contrast Enhancement in Breast MRI** - publikacja bezpośrednio związana z syntezą obrazów DCE-MRI piersi i analizą dynamiki wzmocnienia kontrastowego.
- **Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation** - artykuł opisujący dataset BreastDivider i model segmentacji lewej/prawej piersi.
- **A review on cross-contrast MRI image synthesis through deep learning** - przegląd metod syntezy obrazów MRI pomiędzy różnymi kontrastami.

Najważniejszy wniosek z przeglądu literatury jest taki, że sama ocena globalnymi metrykami obrazu, takimi jak SSIM i PSNR, może być niewystarczająca w zadaniu virtual DCE. W dalszej pracy należy uwzględnić również ocenę w masce piersi oraz, jeśli dane na to pozwolą, ocenę w obszarach zmian chorobowych.

## Rozpoznanie datasetu BreastDivider

Drugim elementem pracowni było wstępne rozpoznanie datasetu BreastDivider. Zbiór ten jest publicznym datasetem MRI piersi zawierającym obrazy 3D oraz maski segmentacyjne lewej i prawej piersi. Ze względu na duży rozmiar pełnego datasetu, wynoszący około 440 GB, nie pobierano całości danych. Zamiast tego wykonano selektywne pobranie metadanych oraz małej próbki technicznej obrazów i masek.

Pobrano i przeanalizowano między innymi:

- `dataset.json`,
- `README.md`,
- `mapping_info.txt`,
- `breastdivider_id_mapping.csv`,
- plik z adnotacjami klasyfikacyjnymi zmian,
- próbkę obrazów MRI i odpowiadających im masek left/right w formacie `.nii.gz`.

Przygotowano skrypty pomocnicze do:

- inwentaryzacji struktury pobranego datasetu,
- podsumowania plików NIfTI,
- sprawdzenia rozmiarów wolumenów, spacingu, typów danych i zakresów intensywności,
- wizualizacji obrazów MRI z nałożonymi maskami lewej i prawej piersi,
- generowania kontrolowanych komend pobierania małych próbek danych z Hugging Face.

Wyniki analizy datasetu zostały zebrane w dedykowanym notebooku:

[notebooks/01_breastdivider_dataset_overview.ipynb](https://github.com/milosz1324/BreastMRI_Embedding_Models_for_vDCE/blob/main/notebooks/01_breastdivider_dataset_overview.ipynb)

Notebook zawiera opis datasetu, podsumowanie pobranych plików, tabele ze statystykami NIfTI, kontrolę zgodności obrazów i masek oraz wizualizacje overlay MRI + maska left/right.

## Wyniki analizy datasetu

Wstępna analiza potwierdziła, że BreastDivider może być użyteczny jako źródło masek anatomicznych dla pipeline'u slice-level. Dla pobranej próbki udało się otworzyć pliki NIfTI oraz sparować obrazy MRI z odpowiadającymi im maskami. Maski zawierają etykiety odpowiadające tłu oraz lewej i prawej piersi, dzięki czemu mogą zostać użyte do wyboru przekrojów zawierających tkankę piersi, cropowania, maskowania oraz odrzucania pustych slice'ów.

Zaobserwowano również istotną zmienność danych. Przypadki różnią się rozmiarem wolumenów, spacingiem, typem danych i zakresem intensywności. Oznacza to, że dalszy preprocessing musi uwzględniać normalizację intensywności oraz ujednolicenie rozmiaru przekrojów 2D. Jest to szczególnie ważne w kontekście uczenia modelu embeddingowego, aby model nie uczył się głównie różnic technicznych pomiędzy akwizycjami.

Na obecnym etapie BreastDivider został potwierdzony jako wartościowy dataset do przygotowania anatomicznego preprocessingu. Nie potwierdzono jeszcze, czy sam BreastDivider zawiera wystarczającą liczbę jednoznacznych par pre-contrast/post-contrast wymaganych do trenowania docelowego modelu virtual DCE. To pozostaje jednym z kluczowych zagadnień do sprawdzenia w kolejnym etapie.

## Rezultaty pracowni

W ramach pracowni przygotowano:

- zestaw opracowań literatury w formacie Markdown,
- szablon oceny artykułów naukowych,
- podsumowanie koncepcji pracy i aktualnego stanu realizacji,
- skrypty do pobierania i analizy próbek BreastDivider,
- notebook Jupyter prezentujący wstępne rozpoznanie datasetu,
- podstawowe wyniki EDA: inwentaryzację plików, statystyki NIfTI oraz wizualizacje masek na obrazach MRI.

Prace te stanowią podstawę do przejścia od rozpoznania literatury i danych do właściwej części eksperymentalnej pracy magisterskiej.

## Planowane następne kroki

W kolejnym etapie planowane jest:

1. Rozszerzenie analizy datasetu o większą, ale nadal kontrolowaną próbkę przypadków.
2. Sprawdzenie, które przypadki mogą zostać wykorzystane jako pary pre-contrast/post-contrast do zadania virtual DCE.
3. Przygotowanie pipeline'u slice-level:
   - wybór przekrojów zawierających tkankę piersi,
   - wykorzystanie masek left/right,
   - crop lub resize przekrojów,
   - normalizacja intensywności,
   - przygotowanie indeksu danych.
4. Przygotowanie prostego baseline'u direct image-to-image, np. modelu 2D U-Net.
5. Przygotowanie pierwszej wersji modelu embeddingowego dla przekrojów 2D MRI piersi.
6. Porównanie podejścia direct image-to-image z podejściem wykorzystującym embeddingi.
7. Ocena jakości rekonstrukcji przy użyciu SSIM, PSNR, MAE/MSE oraz metryk liczonych w masce piersi.

## Podsumowanie

W ramach pracowni problemowej wykonano przygotowanie teoretyczne i praktyczne do dalszej realizacji pracy magisterskiej. Przeanalizowano najważniejsze kierunki literatury, rozpoznano dataset BreastDivider oraz przygotowano narzędzia do jego dalszej analizy. Uzyskane wyniki wskazują, że BreastDivider może pełnić istotną rolę w preprocessingu i przygotowaniu danych slice-level, natomiast dalszej weryfikacji wymaga dostępność par pre-contrast/post-contrast dla właściwego zadania virtual DCE.
