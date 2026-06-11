# Pracownia problemowa magisterska

## Temat pracy

**Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis**

Wersja polska robocza:
**Modele embeddingowe dla MRI piersi w zadaniu syntezy wirtualnych obrazów dynamicznego wzmocnienia kontrastowego**

## Cel pracy

Celem pracy jest opracowanie modelu reprezentacji obrazów MRI piersi na poziomie pojedynczych przekrojów 2D, a następnie sprawdzenie, czy tak wyuczone embeddingi poprawiają jakość generowania obrazów post-kontrastowych w porównaniu z bezpośrednimi metodami image-to-image. Model ma być rozwijany z wykorzystaniem publicznie dostępnego zbioru BreastDivider, który zawiera obrazy MRI piersi oraz segmentacje lewej i prawej piersi.

Główna motywacja kliniczna wynika z faktu, że dynamiczne obrazowanie kontrastowe DCE-MRI jest ważne w diagnostyce raka piersi, ale wymaga podania środka kontrastowego. Metody sztucznej inteligencji mogą umożliwić generowanie obrazów typu virtual DCE na podstawie sekwencji bez kontrastu, co potencjalnie ogranicza obciążenie pacjentki, skraca badanie i zmniejsza zależność od gadolinowych środków kontrastowych.

## Proponowana struktura pierwszego rozdziału

### 1.1. Obrazowanie MRI piersi i znaczenie DCE-MRI

MRI piersi jest jedną z najbardziej czułych metod obrazowania stosowanych w diagnostyce, monitorowaniu leczenia i ocenie zmian nowotworowych. Szczególne znaczenie ma dynamiczne obrazowanie po podaniu kontrastu, ponieważ pozwala obserwować wzorce wzmocnienia tkanek w czasie. Obszary patologiczne, w tym zmiany nowotworowe, często charakteryzują się odmienną dynamiką perfuzji i przepuszczalności naczyń, co przekłada się na widoczne różnice intensywności w obrazach post-kontrastowych.

Jednocześnie DCE-MRI wymaga użycia środków kontrastowych na bazie gadolinu. Chociaż są one powszechnie stosowane, ich podanie wiąże się z dodatkowymi kosztami, dłuższym czasem badania, przeciwwskazaniami oraz pytaniami dotyczącymi bezpieczeństwa u wybranych grup pacjentek. Z tego powodu rośnie zainteresowanie metodami pozwalającymi ograniczyć dawkę kontrastu lub syntetyzować informację kontrastową na podstawie sekwencji niekontrastowych.

### 1.2. Synteza obrazów kontrastowych i virtual DCE

Synteza obrazów medycznych może być traktowana jako zadanie translacji obrazu do obrazu. W kontekście MRI oznacza to uczenie modelu odwzorowania pomiędzy jedną lub kilkoma sekwencjami wejściowymi a obrazem docelowym, na przykład pomiędzy obrazem pre-kontrastowym a obrazem post-kontrastowym. W literaturze stosowano do tego m.in. architektury U-Net, modele GAN, transformatory oraz modele dyfuzyjne.

Dla tej pracy szczególnie istotne są podejścia do virtual DCE, w których model generuje obraz przypominający rzeczywisty obraz po kontraście. Przykładem bezpośrednio związanym z MRI piersi jest praca prezentowana na ISMRM 2022, w której wykorzystano U-Net do generowania virtual dynamic contrast-enhanced MRI of the breast. Nowsze prace z innych narządów, np. DCE-diff, pokazują natomiast przydatność modeli dyfuzyjnych oraz wejść multimodalnych, takich jak T1 pre-contrast, T2, PD i ADC, do syntezy obrazów early/late DCE.

Ważnym problemem w tych metodach jest nie tylko średnia jakość rekonstrukcji, lecz także zachowanie informacji klinicznie istotnej. Model może osiągać dobre wyniki globalne, a jednocześnie rozmywać subtelne zmiany ogniskowe. Z tego powodu poza klasycznymi metrykami jakości obrazu warto rozważyć analizę ograniczoną do obszarów piersi lub zmian chorobowych.

### 1.3. Modele embeddingowe i foundation models w obrazowaniu medycznym

Modele embeddingowe uczą się zwartej reprezentacji danych wejściowych. W obrazowaniu medycznym taka reprezentacja może kodować informacje anatomiczne, teksturalne, modalnościowe i patologiczne, które następnie mogą być wykorzystane w zadaniach klasyfikacji, segmentacji, detekcji lub rekonstrukcji obrazu.

Foundation models w obrazowaniu medycznym rozwijają tę ideę w większej skali. Są trenowane na dużych i zróżnicowanych zbiorach danych, często z użyciem uczenia samonadzorowanego, kontrastywnego lub multimodalnego. Ich zaletą jest możliwość adaptacji do wielu zadań bez trenowania całego modelu od początku. W tej pracy interesujące jest pytanie, czy embeddingi uczone na przekrojach MRI piersi mogą stanowić lepsze wejście lub warunek dla modelu generatywnego niż surowy obraz wejściowy.

W praktyce etap embeddingowy można rozważyć w kilku wariantach:

- autoencoder lub variational autoencoder trenowany do rekonstrukcji slice'ów MRI,
- kontrastywne uczenie reprezentacji dla par przekrojów lub augmentacji,
- model typu masked autoencoder,
- wykorzystanie gotowego modelu medycznego i dostrojenie go do MRI piersi,
- uczenie embeddingu specyficznego dla modalności i anatomicznego regionu piersi.

### 1.4. Zbiór BreastDivider

BreastDivider jest publicznym zbiorem MRI piersi z etykietami segmentacji lewej i prawej piersi. Zgodnie z opisem artykułu "Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation" zbiór obejmuje ponad 13 000 anotowanych przypadków i został udostępniony razem z modelem segmentacyjnym. Wersja BreastDividerDataset na Hugging Face jest oznaczona jako zbiór 3D do segmentacji i klasyfikacji, z licencją CC BY-NC-SA 4.0.

Z punktu widzenia tej pracy BreastDivider jest istotny z kilku powodów:

- pozwala wyciąć lub zamaskować obszar lewej i prawej piersi,
- umożliwia uczenie reprezentacji na dużej liczbie przekrojów 2D,
- może zawierać różne sekwencje MRI, w tym obrazy przed i po kontraście,
- pozwala badać odporność modelu na różnice między źródłami danych i protokołami akwizycji.

Pierwszym krokiem praktycznym powinno być sprawdzenie, które przypadki zawierają pary potrzebne do zadania syntezy: obraz niekontrastowy jako wejście oraz odpowiadający mu obraz post-kontrastowy jako target. Sam fakt istnienia segmentacji lewa/prawa pierś nie wystarcza do trenowania vDCE; potrzebne są jeszcze spójne pary modalności lub faz czasowych.

### 1.5. Metryki oceny jakości syntezy

Do oceny jakości obrazów syntetycznych można wykorzystać metryki pikselowe i strukturalne:

- **PSNR** - mierzy stosunek sygnału do błędu rekonstrukcji; jest prosty, ale słabo oddaje jakość kliniczną.
- **SSIM** - porównuje podobieństwo strukturalne obrazów, uwzględniając luminancję, kontrast i strukturę.
- **MAE/MSE** - mierzą średni błąd intensywności, przydatne jako uzupełnienie PSNR.
- **MS-SSIM** - wieloskalowa wersja SSIM, często lepiej odpowiadająca percepcji struktury.
- **Analiza ROI** - ocena tylko w masce piersi lub w masce zmiany chorobowej, jeśli takie etykiety są dostępne.

W pracy warto raportować metryki zarówno dla całego przekroju, jak i dla obszaru piersi. Jeżeli dostępne będą maski zmian, można dodać analizę lesion-focused, ponieważ właśnie tam błędy syntezy mogą mieć największe znaczenie kliniczne.

## Plan przeglądu literatury

Na potrzeby pracowni problemowej warto opracować 4-6 artykułów, po jednym lub dwa z każdego obszaru. Każdy artykuł można ocenić według template'u z pliku `LITERATURE_REVIEW_TEMPLATE.pdf`.

| Obszar | Proponowany artykuł | Po co go czytać |
| --- | --- | --- |
| Foundation models w obrazowaniu medycznym | `Overview__Foundation_Models_in_Medical_Imaging__A_Review_and_Outlook.pdf` | Ustala słownictwo: foundation model, embedding, transfer, self-supervised learning, downstream task. |
| Dataset i segmentacja MRI piersi | Rokuss et al., "Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation" | Bezpośrednio opisuje BreastDivider i jego ograniczenia. |
| Virtual DCE MRI piersi | "Virtual Dynamic Contrast Enhanced MRI of the Breast using a U-Net" | Najbliższy tematowi pracy przykład generowania DCE dla MRI piersi. |
| Generatywne modele DCE | "DCE-diff: Diffusion Model for Synthesis of Early and Late Dynamic Contrast-Enhanced MR Images from Non-Contrast Multimodal Inputs" | Pokazuje nowocześniejszy model generatywny i metryki PSNR/SSIM/MAE/FID. |
| Image-to-image translation w medycynie | Wybrany przegląd lub klasyczna praca o U-Net/GAN/pix2pix/medical synthesis | Tło metodologiczne dla porównania embedding-based vs direct image-to-image. |
| Ewaluacja syntetycznych obrazów medycznych | Artykuł o ograniczeniach SSIM/PSNR lub ocenie klinicznej syntezy | Uzasadnia, dlaczego same metryki globalne nie wystarczą. |

## Karta oceny artykułu

Do każdego artykułu warto przygotować osobną notatkę według stałego schematu:

1. Pełny tytuł i dane bibliograficzne.
2. Problem badawczy.
3. Dane użyte w eksperymencie.
4. Metoda/architektura.
5. Zadanie wejście -> wyjście.
6. Metryki oceny.
7. Najważniejsze wyniki.
8. Mocne strony.
9. Ograniczenia.
10. Przydatność dla tej pracy magisterskiej.
11. Cytat lub idea do wykorzystania we wstępie/przeglądzie literatury.

## Plan analizy datasetu

Analiza BreastDivider powinna odpowiedzieć najpierw na pytania organizacyjne, a dopiero potem modelowe.

### Etap 1: pobranie i rozpoznanie struktury

Cele:

- sprawdzić rozmiar datasetu i sposób pobierania,
- ustalić strukturę katalogów,
- znaleźć format danych, prawdopodobnie NIfTI `.nii.gz`,
- sprawdzić nazewnictwo modalności i faz kontrastowych,
- zweryfikować licencję oraz wymagania cytowania.

Wynik etapu:

- krótki opis źródła danych,
- tabela z liczbą przypadków, plików i modalności,
- lista problemów technicznych, np. brakujące pary, różne rozdzielczości, różne orientacje.

### Etap 2: exploratory data analysis

Proponowany notebook: `notebooks/01_breastdivider_eda.ipynb`.

Notebook powinien zawierać:

- ładowanie przykładowych wolumenów,
- odczyt shape, spacing, orientation i typów danych,
- histogramy intensywności,
- wizualizację kilku slice'ów,
- nałożenie masek lewej/prawej piersi,
- porównanie pre-contrast i post-contrast, jeśli pary są dostępne,
- wykrywanie pustych lub mało informacyjnych slice'ów,
- wybranie strategii normalizacji intensywności.

### Etap 3: przygotowanie danych slice-level

Docelowy model embeddingowy ma działać na pojedynczych przekrojach 2D, więc trzeba przygotować pipeline:

- wybór osi przekrojów,
- odrzucanie slice'ów bez piersi lub z małą liczbą pikseli w masce,
- crop albo maskowanie obszaru piersi,
- resize do stałego rozmiaru, np. 256 x 256,
- normalizacja intensywności per volume albo per breast mask,
- zapis indeksu danych w formacie CSV/Parquet.

Przykładowy rekord indeksu:

| patient_id | study_id | source_dataset | modality | phase | volume_path | mask_path | slice_idx | breast_side | has_lesion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Duke_Breast_MRI_001 | ... | Duke | T1 | pre | ... | ... | 72 | left | unknown |

### Etap 4: minimalny baseline

Przed modelem embeddingowym warto zbudować prosty baseline:

- wejście: slice pre-contrast lub wybrane sekwencje niekontrastowe,
- target: odpowiadający slice post-contrast,
- model: U-Net 2D,
- metryki: SSIM, PSNR, MAE,
- ewaluacja: cały obraz, maska piersi, opcjonalnie lesion ROI.

Ten baseline będzie punktem odniesienia dla drugiego wariantu:

- encoder generuje embedding slice'a,
- model generatywny dostaje embedding jako warunek,
- porównanie: direct image-to-image vs embedding-conditioned reconstruction.

## Proponowany zakres pierwszej części pracowni

Na najbliższy etap warto przygotować:

1. Wstępny rozdział teoretyczny na 5-8 stron.
2. 4 karty oceny artykułów według template'u.
3. Krótki opis BreastDivider: źródło, rozmiar, modalności, licencja, zastosowanie.
4. Notebook EDA z wizualizacją przykładowych przypadków.
5. Decyzję, czy dataset zawiera wystarczająco dużo par pre/post-contrast do trenowania vDCE.
6. Projekt pipeline'u slice-level i opis pierwszego baseline'u.

## Otwarte pytania badawcze

- Czy embeddingi uczone na slice'ach MRI piersi poprawiają jakość rekonstrukcji obrazów post-kontrastowych?
- Czy embeddingi poprawiają stabilność modelu między różnymi źródłami danych i protokołami MRI?
- Czy model embeddingowy lepiej zachowuje lokalne struktury w obszarach zmian chorobowych?
- Czy segmentacja lewej i prawej piersi pomaga w trenowaniu przez ograniczenie tła i nieistotnych struktur?
- Czy lepsze wyniki globalne SSIM/PSNR przekładają się na lepszą jakość w regionach klinicznie istotnych?

## Bibliografia robocza

1. Rokuss, M., Hamm, B., Kirchhoff, Y., Maier-Hein, K. "Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation." arXiv:2507.13830, 2025. https://arxiv.org/abs/2507.13830
2. BreastDividerDataset, Hugging Face dataset card. https://huggingface.co/datasets/Bubenpo/BreastDividerDataset
3. "Virtual Dynamic Contrast Enhanced MRI of the Breast using a U-Net." ISMRM 2022 abstract. https://archive.ismrm.org/2022/1522.html
4. M., K. K. et al. "DCE-diff: Diffusion Model for Synthesis of Early and Late Dynamic Contrast-Enhanced MR Images from Non-Contrast Multimodal Inputs." CVPR Workshop, 2024. https://openaccess.thecvf.com/content/CVPR2024W/DEF-AI-MIA/papers/M_DCE-diff_Diffusion_Model_for_Synthesis_of_Early_and_Late_Dynamic_CVPRW_2024_paper.pdf
5. "Foundation Models in Medical Imaging -- A Review and Outlook." arXiv:2506.09095. https://arxiv.org/abs/2506.09095

## Następne kroki

1. Otworzyć `START_HERE.pdf` i sprawdzić formalne wymagania prowadzącego.
2. Przepisać pola z `LITERATURE_REVIEW_TEMPLATE.pdf` do osobnego szablonu markdown dla kart artykułów.
3. Opracować pierwszy artykuł: `Overview__Foundation_Models_in_Medical_Imaging__A_Review_and_Outlook.pdf`.
4. Sprawdzić technicznie możliwość pobrania BreastDivider i jego rozmiar.
5. Utworzyć notebook EDA po potwierdzeniu sposobu pobrania datasetu.
