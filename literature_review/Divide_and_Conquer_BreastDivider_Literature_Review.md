## **5 Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation**

## **5.1 Dane bibliograficzne**

- **Tytul:** Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation

- **Autorzy:** Maximilian Rokuss, Benjamin Hamm, Yannick Kirchhoff, Klaus Maier-Hein

- **Rok:** 2025

- **Typ publikacji:** arXiv preprint; artykul zaakceptowany na MICCAI 2025 WOMEN workshop

- **Link:** https://arxiv.org/abs/2507.13830

- **Repozytorium:** https://github.com/MIC-DKFZ/BreastDivider

- **Dataset:** https://huggingface.co/datasets/Bubenpo/BreastDividerDataset

## **5.2 Problem**

Artykul rozwiazuje problem braku duzego, publicznie dostepnego zbioru MRI piersi z osobnymi maskami lewej i prawej piersi. W wielu publicznych datasetach i modelach segmentacyjnych piers traktowana jest jako jeden obszar anatomiczny, bez rozroznienia strony lewej i prawej. Jest to istotne ograniczenie, poniewaz wiele analiz klinicznych w breast MRI ma charakter jednostronny, np. ocena guza w jednej piersi, monitorowanie odpowiedzi na leczenie, analiza po mastektomii lub klasyfikacja zmian po jednej stronie.

Autorzy proponuja BreastDivider, czyli duzy dataset oraz model segmentacyjny do rozdzielania lewej i prawej piersi w obrazach MRI. Celem jest stworzenie zasobu, ktory moze wspierac bardziej anatomicznie swiadome modele AI dla breast MRI.

Z punktu widzenia niniejszej pracy artykul jest zwiazany przede wszystkim z datasetem i preprocessingiem. Nie dotyczy bezposrednio virtual DCE ani syntezy obrazow, ale jest kluczowy dla przygotowania danych slice-level. Maski lewej i prawej piersi moga pomoc ograniczyc uczenie modelu do istotnego obszaru anatomicznego, zamiast trenowac go na duzej ilosci tla i struktur spoza piersi.

Artykul jest zwiazany z:

- foundation models: posrednio, poniewaz dataset moze sluzyc do pretrainingu lub uczenia reprezentacji dla zadan downstream;
- MRI: tak;
- breast MRI: tak, bezposrednio;
- virtual contrast / vDCE: nie bezposrednio;
- image synthesis: nie bezposrednio;
- embeddings / representation learning: posrednio, przez mozliwosc przygotowania danych do uczenia embeddingow slice-level.

## **5.3 Dane**

Autorzy wprowadzaja BreastDivider, czyli publiczny dataset MRI piersi z jawnymi etykietami lewej i prawej piersi. Wedlug abstraktu artykulu zbior obejmuje ponad 13 000 anotowanych przypadkow. Aktualna wersja opisana w repozytorium zawiera 17 956 skanow 3D MRI piersi z maskami left/right.

Dataset zostal zbudowany z siedmiu publicznych kolekcji:

- Duke-Breast-Cancer-MRI;
- MAMA-MIA;
- Advanced-MRI-Breast-Lesions;
- EA1141;
- ODELIA;
- ISPY1;
- ISPY2.

Dane sa publiczne i udostepnione na Hugging Face. Kod oraz wrapper modelu znajduja sie w repozytorium GitHub MIC-DKFZ/BreastDivider. Dataset ma licencje CC BY-NC-SA 4.0, czyli pozwala na uzycie niekomercyjne z podaniem autorstwa i zachowaniem tej samej licencji.

Dane dotycza 3D MRI piersi i sa zapisane w formacie `.nii.gz`. Poniewaz zbior jest skompilowany z wielu publicznych kolekcji, moze zawierac rozne sekwencje, protokoly i fazy obrazowania. Z punktu widzenia mojej pracy szczegolnie wazne bedzie sprawdzenie, ktore przypadki zawieraja pary pre-contrast i post-contrast potrzebne do trenowania modeli virtual DCE.

Input modelu segmentacyjnego:

- obraz MRI piersi w formacie `.nii.gz`.

Target modelu segmentacyjnego:

- maska segmentacyjna w formacie `.nii.gz` z etykietami background, left breast i right breast.

W aktualnej wersji datasetu dostepne sa takze dodatkowe anotacje zmian chorobowych: ponad 3000 lesion classification targets oraz 467 masek segmentacji zmian. Moze to byc przydatne w przyszlej analizie lesion-focused, chociaz najpierw trzeba sprawdzic, czy te maski sa zgodne z przypadkami wybranymi do zadania vDCE.

Artykul i repozytorium informuja o ewaluacji w schemacie 5-fold cross-validation. Szczegoly splitu nalezy jeszcze zweryfikowac w pelnym PDF-ie lub dokumentacji datasetu. Dla dalszej pracy nad vDCE bardzo wazne bedzie, aby podzial train/validation/test byl wykonany na poziomie pacjenta, a nie pojedynczych slice'ow.

## **5.4 Metoda**

Autorzy udostepniaja model segmentacyjny oparty o nnU-Net / nnU-Net v2. Jest to popularna architektura i framework dla segmentacji obrazow medycznych, ktory automatycznie dobiera wiele elementow pipeline'u do konkretnego datasetu.

Metoda jest supervised segmentation. Wejsciem jest obraz MRI piersi, a wyjsciem maska segmentacyjna lewej i prawej piersi. Nie jest to metoda generatywna, diffusion ani GAN. Architektura nalezy do rodziny U-Net, ale artykul nie proponuje modelu syntezy obrazow.

Model nie uczy embeddingow w sensie planowanym w mojej pracy. Oczywiscie siec segmentacyjna tworzy wewnetrzne reprezentacje potrzebne do predykcji masek, ale nie jest to osobny encoder przeznaczony do transferu lub warunkowania modelu generatywnego.

Model pracuje na danych 3D MRI. Jest to istotne, poniewaz segmentacja calego wolumenu pozwala uzyskac spojne maski lewej i prawej piersi. W mojej pracy te maski moga zostac pozniej wykorzystane do przygotowania danych 2D slice-level:

- wyboru slice'ow zawierajacych tkanke piersi;
- cropowania lub maskowania obszaru piersi;
- odrzucania pustych przekrojow;
- osobnej analizy lewej i prawej piersi;
- ograniczenia metryk rekonstrukcji do obszaru piersi.

## **5.5 Ewaluacja**

Glowna metryka raportowana dla modelu segmentacyjnego to Dice score. Repozytorium podaje, ze pretrained nnU-Net osiaga okolo 0.99 Dice w 5-fold cross-validation.

Artykul nie raportuje metryk typowych dla syntezy obrazow, takich jak SSIM, PSNR, MAE lub MSE, poniewaz jego zadaniem jest segmentacja lewej i prawej piersi. Te metryki beda potrzebne dopiero w drugiej fazie mojej pracy, przy ocenie jakosci generowanych obrazow post-kontrastowych.

Glowny cel artykulu nie obejmuje oceny lesion-focused. Jednak aktualna wersja datasetu zawiera dodatkowe anotacje lesion, w tym ponad 3000 targetow klasyfikacyjnych i 467 masek segmentacyjnych zmian. To moze byc wazne w przyszlosci, jesli analiza vDCE zostanie rozszerzona o ocene jakosci rekonstrukcji w obszarach zmian chorobowych.

Na podstawie dostepnego opisu najwazniejszym wynikiem jest udostepnienie datasetu oraz modelu nnU-Net z bardzo wysokim Dice. Szczegolowe porownania z baseline'ami nalezy sprawdzic w pelnym PDF-ie artykulu.

## **5.6 Najwazniejsze wyniki**

Najwazniejsze wyniki i zasoby opisane w artykule oraz repozytorium:

- ponad 13 000 anotowanych przypadkow w wersji opisanej w abstrakcie artykulu;
- 17 956 skanow 3D MRI piersi w aktualnej wersji datasetu;
- maski left/right breast dla obrazow MRI;
- 3021 lesion classification targets;
- 467 lesion segmentation masks;
- pretrained nnU-Net do segmentacji lewej i prawej piersi;
- okolo 0.99 Dice w 5-fold cross-validation;
- publiczne repozytorium, dataset Hugging Face i gotowy wrapper inference.

Najwazniejszy wniosek autorow jest taki, ze rozroznienie lewej i prawej piersi jest waznym, ale dotad slabo wspieranym elementem analizy MRI piersi. BreastDivider ma wypelnic te luke poprzez udostepnienie duzego publicznego datasetu i gotowego modelu segmentacyjnego. Zasob ten moze wspierac zadania takie jak jednostronna klasyfikacja, analiza odpowiedzi na leczenie, follow-up po mastektomii oraz pretraining dla dalszych modeli AI w breast MRI.

Co wyglada przekonujaco:

- duza skala datasetu;
- publiczna dostepnosc danych i modelu;
- zebranie danych z wielu publicznych kolekcji;
- praktyczne repozytorium z gotowym narzedziem inference;
- bardzo wysoki Dice dla segmentacji lewej i prawej piersi;
- mozliwosc wykorzystania masek w dalszych zadaniach AI dla breast MRI.

Co jest slabe lub niejasne:

- artykul nie dotyczy bezposrednio syntezy vDCE ani rekonstrukcji obrazow post-kontrastowych;
- nie wiadomo od razu, ile przypadkow ma kompletne pary pre-contrast i post-contrast;
- trzeba samodzielnie sprawdzic strukture plikow, modalnosci i fazy obrazowania;
- nalezy zweryfikowac zgodnosc przestrzenna obrazow, masek piersi i ewentualnych masek zmian;
- dataset wymaga dodatkowej analizy technicznej przed trenowaniem modelu generatywnego.

## **5.7 Znaczenie dla pracy magisterskiej**

Artykul jest bardzo wazny, poniewaz opisuje dataset wskazany w temacie pracy jako baza do trenowania modelu embeddingowego. Chociaz BreastDivider nie jest datasetem zaprojektowanym specjalnie do virtual DCE, dostarcza duza liczbe obrazow MRI piersi oraz maski lewej i prawej piersi. Maski te moga byc wykorzystane do przygotowania danych na poziomie pojedynczych przekrojow 2D.

W kontekscie tematu _Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis_ artykul pomaga przede wszystkim w czesci datasetowej i preprocessingowej. Pozwala uzasadnic, dlaczego warto ograniczyc analize do obszaru piersi i dlaczego segmentacja lewej/prawej piersi moze poprawic przygotowanie danych.

Elementy mozliwe do wykorzystania w pracy:

- opis BreastDivider jako glownego publicznego datasetu;
- informacje o zrodlowych kolekcjach MRI piersi;
- wykorzystanie masek left/right do cropowania i maskowania;
- wybor slice'ow zawierajacych tkanke piersi;
- odrzucanie pustych lub malo informacyjnych przekrojow;
- przygotowanie indeksu danych slice-level;
- osobna analiza lewej i prawej piersi;
- potencjalna analiza lesion-focused, jesli dostepne maski zmian beda zgodne z wybranymi przypadkami;
- BreastDivider jako etap preprocessingu przed baseline'em image-to-image.

Artykul nie dostarcza bezposrednio architektury modelu vDCE ani metryk rekonstrukcji. Jego znaczenie polega raczej na tym, ze organizuje przestrzen danych i pozwala przygotowac bardziej anatomicznie sensowny pipeline przed uczeniem embeddingow i modelu generatywnego.

## **5.8 Ocena przydatnosci**

## **Ocena: 5/5**

Artykul jest kluczowy dla mojej pracy, poniewaz opisuje BreastDivider, czyli dataset wskazany w temacie jako baza do trenowania modelu embeddingowego. Nie odpowiada bezposrednio na pytanie o virtual DCE, ale jest bardzo wazny dla czesci praktycznej: pobrania danych, zrozumienia ich struktury, przygotowania masek piersi, wyboru slice'ow 2D i budowy pipeline'u preprocessingowego.

Bez tej analizy trudno bedzie poprawnie przygotowac dane do pozniejszego trenowania modelu generatywnego. Szczegolnie istotne bedzie sprawdzenie, ktore przypadki z BreastDivider zawieraja pary pre-contrast i post-contrast oraz czy maski left/right mozna bezproblemowo wykorzystac do analizy slice-level.
