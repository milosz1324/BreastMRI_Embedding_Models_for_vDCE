## **4 A review on cross-contrast MRI image synthesis through deep learning**

## **4.1 Dane bibliograficzne**

- **Tytul:** A review on cross-contrast MRI image synthesis through deep learning

- **Autorzy:** Richard Acs, Hanqi Zhuang

- **Rok:** 2025

- **Typ publikacji:** Review article, Discover Imaging, Volume 2, Article 9

- **DOI:** https://doi.org/10.1007/s44352-025-00012-3

- **Link:** https://link.springer.com/article/10.1007/s44352-025-00012-3

## **4.2 Problem**

Artykul porzadkuje literature dotyczaca syntezy obrazow MRI pomiedzy roznymi kontrastami, czyli cross-contrast MRI image synthesis. Problem polega na tym, ze pelne badanie MRI czesto wymaga wielu sekwencji, np. T1, T2, FLAIR, DWI lub obrazow po kontraście. Akwizycja wielu kontrastow jest czasochlonna, kosztowna i uciazliwa dla pacjenta. W niektorych sytuacjach okreslony kontrast moze byc niedostepny, zlej jakosci albo przeciwwskazany, np. gdy wymaga podania srodka kontrastowego.

Synteza cross-contrast ma pozwolic wygenerowac brakujacy kontrast MRI na podstawie innych dostepnych sekwencji. W praktyce jest to problem image-to-image translation: model dostaje jeden lub kilka obrazow wejściowych i generuje obraz docelowy o innym kontraście.

Artykul jest istotny dla mojej pracy, poniewaz virtual DCE mozna potraktowac jako szczegolny przypadek cross-contrast MRI synthesis. W moim przypadku interesuje mnie generowanie obrazu post-kontrastowego lub obrazu podobnego do DCE na podstawie obrazow niekontrastowych i/lub embeddingow slice-level.

Artykul jest zwiazany z:

- foundation models: posrednio, przez dyskusje reprezentacji latentnych i architektur deep learning;
- MRI: tak;
- breast MRI: czesciowo, poniewaz omawia rowniez badania breast MRI, ale wiekszosc literatury dotyczy brain MRI;
- virtual contrast / vDCE: tak, w szerszym znaczeniu syntezy obrazow contrast-enhanced;
- image synthesis: tak, bezposrednio;
- embeddings / representation learning: posrednio, zwlaszcza przez autoencodery, latent spaces, diffusion conditioning i multimodalne reprezentacje.

## **4.3 Dane**

Artykul jest przegladem 30 badan dotyczacych deep learning-based cross-contrast MRI synthesis. Autorzy nie trenuja wlasnego modelu, ale analizuja dane, architektury, metryki i zastosowania kliniczne opisane w wybranych publikacjach.

Proces wyszukiwania literatury obejmowal bazy PubMed, IEEE Xplore i DOAJ. Autorzy analizowali publikacje dotyczace syntezy MRI przy uzyciu deep learningu, a nastepnie odfiltrowali je do prac stricte dotyczacych translacji pomiedzy kontrastami MRI.

Najczesciej omawiane publiczne datasety to:

- BraTS;
- ISLES;
- IXI.

Autorzy podkreslaja jednak, ze publiczne datasety uzywane w tej dziedzinie sa zdominowane przez brain MRI. To ogranicza generalizacje na inne regiony anatomiczne, takie jak piers, serce czy uklad miesniowo-szkieletowy. W przegladzie wskazano, ze tylko czesc badan wykorzystywala prywatne dane kliniczne, a wsrod nich tylko dwa dotyczyly tkanki piersi.

Input i target zaleza od konkretnej pracy. Przyklady:

- T1 -> T2;
- T2 -> T1;
- T1/T2/DWI -> FLAIR;
- non-contrast T1 -> contrast-enhanced T1;
- jedna modalnosc -> wiele brakujacych kontrastow;
- wiele modalnosci -> jedna modalnosc docelowa.

Dla mojej pracy szczegolnie wazny jest wariant artificial contrast enhancement, czyli generowanie obrazu contrast-enhanced bez dodatkowej akwizycji lub bez podania kontrastu. Autorzy wskazuja, ze takie badania istnieja, ale czesto opieraja sie na prywatnych datasetach, co pokazuje potrzebe publicznych zbiorow dla zadan zwiazanych z kontrastem.

## **4.4 Metoda**

Artykul omawia glowne rodziny architektur wykorzystywanych w cross-contrast MRI synthesis.

Pierwsza grupa to klasyczne sieci neuronowe do translacji obrazu:

- fully convolutional neural networks;
- autoencodery;
- U-Net.

Modele te dobrze nadaja sie do bezposredniego uczenia odwzorowania input -> target, szczegolnie gdy dostepne sa sparowane dane. U-Net jest czesto stosowany jako model bazowy, poniewaz laczy encoder-decoder ze skip connections, co pomaga zachowac strukture anatomiczna.

Druga grupa to GAN-y:

- conditional GAN;
- pix2pix;
- CycleGAN;
- StarGAN;
- inne warianty adversarial image-to-image translation.

GAN-y sa przydatne, gdy celem jest realistyczna synteza obrazu, szczegolnie w przypadku danych niesparowanych lub mniej scisle kontrolowanych. Conditional GAN i pix2pix sa typowymi rozwiazaniami dla sparowanych danych, natomiast CycleGAN pozwala uczyc translacje bez pelnych par input-target.

Trzecia grupa to diffusion models, szczegolnie DDPM. Autorzy wskazuja, ze modele dyfuzyjne moga dawac bardzo wysoka jakosc i dobre zachowanie szczegolow strukturalnych, ale sa bardziej kosztowne obliczeniowo i wolniejsze ze wzgledu na iteracyjny proces generowania.

Czwarta grupa to transformery i modele hybrydowe. Vision Transformers oraz modele laczace CNN i attention sa obiecujace, poniewaz potrafia modelowac zaleznosci globalne. Jednoczesnie sa drozsze obliczeniowo i mniej powszechne w cross-contrast MRI synthesis niz U-Net lub GAN.

Z punktu widzenia mojej pracy bardzo wazne jest to, ze autorzy omawiaja latent space i reprezentacje multimodalne. W niektorych metodach dostepne kontrasty lub maski anatomiczne sa wprowadzane jako warunek generowania. To dobrze laczy sie z idea pracy magisterskiej, w ktorej model generatywny moze byc warunkowany embeddingiem slice'a MRI.

## **4.5 Ewaluacja**

Autorzy wskazuja, ze najczesciej stosowane metryki w MRI image synthesis to:

- MAE;
- MSE;
- RMSE;
- PSNR;
- SSIM;
- NMSE;
- NRMSE;
- PCC;
- NCC;
- FID.

Szczegolnie czesto pojawiaja sie SSIM, PSNR i NMSE. SSIM mierzy podobienstwo strukturalne, PSNR mierzy relacje sygnalu do bledu rekonstrukcji, a MAE/MSE mierza blad pikselowy. Autorzy podkreslaja jednak, ze takie metryki nie zawsze wystarczaja do oceny przydatnosci klinicznej obrazu syntetycznego.

Bardzo wazna czesc artykulu dotyczy oceny klinicznej. Autorzy wskazuja, ze kilka badan wykorzystywalo ocene radiologow, np. skale Likerta dotyczace artefaktow, jakosci fat suppression, pewnosci diagnostycznej, marginesow tkanek i definicji struktur anatomicznych. Tego typu ocena moze ujawnic problemy, ktorych nie widac w SSIM lub PSNR.

Artykul omawia rowniez metody statystyczne stosowane do porownywania modeli:

- Wilcoxon signed-rank test;
- ANOVA;
- mixed effects models.

Dla mojej pracy najwazniejszy wniosek ewaluacyjny jest taki, ze SSIM i PSNR sa potrzebne, ale nie powinny byc jedynymi metrykami. W przypadku vDCE szczegolnie wazna bedzie ocena w masce piersi, w ROI zmiany oraz potencjalnie ocena zachowania lokalnego wzmocnienia.

## **4.6 Najwazniejsze wnioski**

Najwazniejszy wniosek artykulu jest taki, ze deep learning skutecznie wspiera synteze cross-contrast MRI, ale dziedzina nadal ma ograniczenia zwiazane z danymi, kliniczna interpretowalnoscia i generalizacja.

Autorzy wskazuja, ze:

- U-Net i GAN-y sa dominujacymi architekturami w obecnej literaturze;
- GAN-y i DDPM-y osiagaja bardzo dobre wyniki jakosciowe;
- diffusion models sa obiecujace, ale kosztowne obliczeniowo;
- transformery sa kierunkiem rozwojowym, ale nadal mniej eksplorowanym;
- wiekszosc publicznych benchmarkow dotyczy brain MRI;
- brakuje duzych, publicznych i wieloosrodkowych datasetow dla innych anatomii, w tym breast MRI;
- ocena kliniczna przez ekspertow jest konieczna, poniewaz metryki techniczne moga ukrywac istotne bledy diagnostyczne.

Co wyglada przekonujaco:

- artykul systematycznie porzadkuje 30 prac;
- jasno rozdziela architektury: U-Net/CNN, GAN, diffusion, transformer;
- dobrze opisuje metryki i ograniczenia SSIM/PSNR;
- wskazuje problem dominacji brain MRI w publicznych danych;
- omawia artificial contrast enhancement jako wazny wariant cross-contrast synthesis.

Co jest slabe lub niejasne:

- artykul jest przegladem, wiec nie daje jednego eksperymentu do bezposredniego odtworzenia;
- nie skupia sie na breast MRI, tylko na calej dziedzinie MRI synthesis;
- wiele wnioskow ma charakter ogolny;
- nie rozwiazuje problemu wyboru konkretnej architektury dla vDCE w MRI piersi.

## **4.7 Znaczenie dla pracy magisterskiej**

Artykul jest bardzo przydatny jako szerokie zrodlo metodologiczne dla rozdzialu o syntezie MRI. Pomaga umiejscowic virtual DCE w szerszym obszarze cross-contrast MRI synthesis.

Dla tematu _Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis_ artykul moze posluzyc do uzasadnienia kilku decyzji:

- potraktowania vDCE jako zadania image-to-image translation;
- wyboru U-Net jako prostego baseline'u;
- rozpatrzenia GAN lub diffusion model jako mocniejszych modeli generatywnych;
- uzycia embeddingu jako warunku generowania;
- raportowania SSIM, PSNR i MAE;
- dodania oceny ROI lub lesion-focused;
- ostroznego traktowania globalnych metryk obrazu.

Artykul dobrze wspiera takze argument, ze publiczne datasety dla breast MRI sa mniej powszechne niz dla brain MRI. To uzasadnia uzycie BreastDivider oraz potrzebe wlasnej analizy datasetu pod katem par pre/post-contrast.

Elementy mozliwe do wykorzystania w pracy:

- definicja cross-contrast MRI synthesis;
- przeglad architektur U-Net, GAN, DDPM i transformer;
- lista typowych metryk: MAE, PSNR, SSIM, NMSE, FID;
- argument za ocena kliniczna lub ROI-based;
- wskazanie ograniczen publicznych datasetow;
- fragment do porownania direct image-to-image vs embedding-conditioned synthesis.

## **4.8 Ocena przydatnosci**

## **Ocena: 5/5**

Artykul jest bardzo przydatny, poniewaz porzadkuje metody syntezy MRI i metryki oceny, ktore bezposrednio dotycza drugiej fazy pracy magisterskiej. Nie jest skoncentrowany wylacznie na breast MRI ani vDCE, ale daje szeroki kontekst metodologiczny i pomaga uzasadnic wybor baseline'ow oraz sposob ewaluacji. Szczegolnie wazny jest wniosek, ze metryki globalne, takie jak SSIM i PSNR, powinny byc uzupelnione ocena kliniczna lub przynajmniej analiza ROI.
