## **2 Synthesizing Late-Stage Contrast Enhancement in Breast MRI: A Comprehensive Pipeline Leveraging Temporal Contrast Enhancement Dynamics**

## **2.1 Dane bibliograficzne**

- **Tytul:** Synthesizing Late-Stage Contrast Enhancement in Breast MRI: A Comprehensive Pipeline Leveraging Temporal Contrast Enhancement Dynamics

- **Alternatywny tytul w wersji HTML arXiv:** A Time-Intensity Aware Pipeline for Generating Late-Stage Breast DCE-MRI using Generative Adversarial Models

- **Autorzy:** Ruben D. Fonnegra, Maria Liliana Hernandez, Juan C. Caicedo, Gloria M. Diaz

- **Rok:** 2024; wersja v2 opublikowana 24.01.2025

- **Typ publikacji:** arXiv preprint, arXiv:2409.01596

- **Link:** https://arxiv.org/abs/2409.01596

## **2.2 Problem**

Artykul dotyczy syntezy poznej fazy obrazow DCE-MRI piersi na podstawie wczesnej fazy po podaniu kontrastu. Autorzy wychodza z zalozenia, ze pelne badanie DCE-MRI jest klinicznie wartosciowe, ale czasochlonne, kosztowne i obciazajace dla pacjentek. Standardowe protokoly moga obejmowac kilka akwizycji po podaniu kontrastu, co wydluza badanie, zwieksza ryzyko artefaktow ruchowych oraz wymaga wiekszych zasobow do przechowywania i analizy danych.

Problem polega na tym, ze skrocone protokoly MRI zwykle zachowuja tylko wczesna faze po kontraście. To pozwala wykrywac podejrzane obszary, ale ogranicza mozliwosc oceny dynamiki wzmocnienia kontrastowego. Pozna faza jest wazna, poniewaz pozwala analizowac krzywa time-intensity, ktora moze miec charakter persistent, plateau lub washout. Taki wzorzec moze pomagac w roznicowaniu zmian lagodnych i zlosliwych.

Z punktu widzenia niniejszej pracy artykul jest bardzo blisko tematu virtual DCE. Nie generuje obrazu post-kontrastowego bez zadnego kontrastu, lecz syntetyzuje pozna faze kontrastowa z fazy wczesnej. Mimo tego jest istotny, bo pokazuje, ze sama wizualna podobnosc obrazu nie wystarcza. Model powinien zachowywac klinicznie istotna dynamike wzmocnienia.

Artykul jest zwiazany z:

- foundation models: nie bezposrednio;
- MRI: tak;
- breast MRI: tak, bezposrednio;
- virtual contrast / vDCE: tak, w wariancie early-to-late DCE synthesis;
- image synthesis: tak;
- embeddings / representation learning: posrednio, poniewaz model uczy reprezentacje potrzebne do syntezy, ale nie jest to osobny embedding model.

## **2.3 Dane**

Autorzy wykorzystuja publiczny dataset Duke-Breast-Cancer-MRI. Zbior zawiera 922 przedoperacyjne badania MRI pacjentek z inwazyjnym rakiem piersi. Dane obejmuja sekwencje pre-contrast oraz 3 lub 4 sekwencje post-contrast. Pacjentki byly badane na skanerach 1.5T i 3T, z uzyciem roznych producentow skanerow i roznych srodkow kontrastowych, co zwieksza heterogenicznosc danych.

W eksperymentach wykorzystano:

- obraz pre-contrast jako punkt odniesienia dla normalizacji i krzywej time-intensity;
- najwczesniejszy obraz post-contrast, okolo 2 minuty po podaniu kontrastu;
- najpozniejszy obraz post-contrast, okolo 6 minut po podaniu kontrastu.

Input modelu:

- early post-contrast DCE-MRI.

Target modelu:

- late post-contrast DCE-MRI.

Autorzy trenowali modele oddzielnie dla obrazow 1.5T i 3T, poniewaz obrazy z tych dwoch typow skanerow roznia sie wizualnie i kontrastowo. W pracy podano, ze wykorzystane podzbiory obejmowaly 393 pacjentow dla 1.5T oraz 389 pacjentow dla 3T.

Pelne wolumeny DICOM nie byly wykorzystane bezposrednio. Autorzy wykonali selekcje obrazow/ramek na podstawie dostepnych anotacji ROI, uwzgledniajac takze obrazy poprzedzajace i nastepujace. To oznacza, ze podejscie jest bardziej slice/frame-level niz pelne 3D volume-level.

W artykule nie jest najwazniejszy klasyczny split pacjentow, lecz ocena generowanych obrazow dla wybranych przypadkow i ROI. Dla niniejszej pracy trzeba jednak pamietac, ze przy budowie wlasnego pipeline'u vDCE podzial train/validation/test powinien byc wykonany na poziomie pacjenta, aby uniknac data leakage miedzy podobnymi przekrojami tego samego badania.

## **2.4 Metoda**

Artykul proponuje caly pipeline, a nie tylko pojedyncza architekture. Pipeline sklada sie z trzech glownych elementow:

- normalizacji TI-norm;
- modelu generatywnego TI-PAN;
- ewaluacji opartej o klasyczne metryki obrazu i metryki krzywej time-intensity.

Podstawowa architektura to Pixel Attention Network (PAN). Jest to model z blokami attention, ktore maja wydobywac cechy przestrzenne i rekonstruowac obraz wyjsciowy. Autorzy rozszerzaja model o podejscie adversarialne, dodajac dyskryminator podobny do rozwiazan GAN. Model generuje pozna faze kontrastowa na podstawie obrazu wczesnej fazy.

Najwazniejsza innowacja metodyczna to Time-Intensity Loss (TI-loss). Funkcja straty nie optymalizuje wylacznie pikselowej zgodnosci miedzy obrazem syntetycznym i rzeczywistym. Zamiast tego uwzglednia roznice w zachowaniu wzmocnienia kontrastowego, czyli zmiane intensywnosci miedzy faza wczesna i pozna. Autorzy argumentuja, ze dla DCE-MRI kluczowe jest nie tylko wygenerowanie realistycznego obrazu, ale zachowanie klinicznie interpretowalnej krzywej time-intensity.

Drugim waznym elementem jest TI-norm, czyli normalizacja oparta na informacji czasowej. Autorzy zwracaja uwage, ze klasyczne min-max lub z-score liczone osobno dla kazdego obrazu moga zniszczyc relacje intensywnosci pomiedzy pre-contrast, early post-contrast i late post-contrast. TI-norm wykorzystuje statystyki obrazu pre-contrast jako wspolny punkt odniesienia, dzieki czemu obrazy post-contrast zachowuja informacje o wzorcu wzmocnienia.

Metoda jest:

- supervised, bo uczy sie z par early post-contrast -> late post-contrast;
- generatywna, bo syntetyzuje brakujaca faze obrazowania;
- GAN-like, bo wykorzystuje dyskryminator;
- 2D/frame-level, poniewaz pelne wolumeny nie byly uzyte bezposrednio;
- nie jest self-supervised ani foundation model.

## **2.5 Ewaluacja**

Autorzy oceniaja synteze na dwoch poziomach: klasyczna jakosc obrazu oraz zachowanie klinicznie istotnej dynamiki kontrastu.

Klasyczne metryki obrazu:

- MAE;
- SSIM;
- PSNR.

Te metryki sa liczone dla calego obrazu oraz dla ROI. Wyniki pokazuja, ze modele moga byc podobne pod wzgledem metryk pikselowych, a mimo to roznic sie pod wzgledem zachowania krzywej time-intensity. To jest jeden z najwazniejszych wnioskow dla mojej pracy.

Metryki specyficzne dla DCE-MRI:

- CA Pattern Score, czyli metryka sprawdzajaca, czy syntetyczny obraz zachowuje ten sam typ krzywej wzmocnienia co obraz rzeczywisty: persistent, plateau lub washout;
- Average Difference in Enhancement, czyli srednia roznica we wzmocnieniu miedzy obrazem rzeczywistym i wygenerowanym.

Ewaluacja obejmuje:

- caly obraz;
- anotowane ROI;
- nieanotowane regiony tkanki.

Autorzy stosuja takze test Wilcoxona, aby sprawdzic, czy istnieje istotna roznica miedzy rzeczywistym i wygenerowanym wzmocnieniem kontrastowym. To jest interesujace, bo wychodzi poza samo raportowanie SSIM/PSNR i wprowadza bardziej klinicznie zorientowana ocene.

## **2.6 Najwazniejsze wyniki**

Wyniki pikselowe byly podobne dla porownywanych modeli PAN, CE-PAN i TI-PAN. W tabeli dla pelnych obrazow 1.5T raportowano m.in. PSNR okolo 27.0 i SSIM okolo 0.69, natomiast dla 3T PSNR okolo 25.5-25.7 i SSIM okolo 0.69. Rownice w klasycznych metrykach byly niewielkie.

Dla ROI wartosci SSIM byly nizsze niz dla calego obrazu, co jest spodziewane, poniewaz obszary zmian i lokalnego wzmocnienia sa trudniejsze do wygenerowania niz duze fragmenty tla lub stabilnej tkanki. Dla ROI raportowano SSIM okolo 0.51 dla 1.5T i okolo 0.58 dla 3T.

Najwazniejsze wyniki dotycza jednak metryk time-intensity. TI-PAN osiagal lepsze wyniki niz klasyczny PAN i CE-PAN w metrykach opisujacych zachowanie wzmocnienia kontrastowego. W tabeli widac szczegolnie duza poprawe CA Pattern Score: TI-PAN uzyskuje okolo 0.827 dla 1.5T i 0.818 dla 3T, podczas gdy pozostale warianty sa blizej 0.61-0.63.

Autorzy pokazuja rowniez, ze klasyczna normalizacja min-max i z-score moze wizualnie dawac podobne obrazy, ale jednoczesnie znieksztalcac krzywa time-intensity. TI-norm zachowuje relacje intensywnosci miedzy fazami badania i dzieki temu lepiej wspiera klinicznie interpretowalna synteze.

Najwazniejszy wniosek autorow:

Same metryki obrazu, takie jak PSNR, SSIM i MAE, nie wystarczaja do oceny syntezy DCE-MRI. Model moze wygladac dobrze globalnie, ale nie zachowywac poprawnie wzorca wzmocnienia kontrastowego w obszarach klinicznie istotnych. Dlatego w zadaniach virtual DCE konieczne jest laczenie metryk pikselowych z metrykami zaleznymi od dynamiki kontrastu i ROI.

Co wyglada przekonujaco:

- temat jest bezposrednio zwiazany z breast DCE-MRI;
- metoda uwzglednia kliniczny sens obrazow, a nie tylko ich podobienstwo pikselowe;
- autorzy testuja oddzielnie 1.5T i 3T;
- wykorzystany jest publiczny dataset Duke;
- praca dobrze uzasadnia, dlaczego SSIM/PSNR nie wystarczaja;
- TI-norm jest praktyczna wskazowka dla preprocessingu sekwencji DCE.

Co jest slabe lub niejasne:

- metoda nie usuwa potrzeby podania kontrastu, bo generuje pozna faze z wczesnej fazy post-contrast;
- nie jest to dokladnie to samo zadanie co synteza vDCE z obrazow niekontrastowych;
- podejscie opiera sie na wybranych ROI i ramkach, a nie na pelnych wolumenach;
- potrzebna bylaby niezalezna ocena kliniczna przez radiologow;
- autorzy sami wskazuja, ze nalezy zbadac odpornosc na rozne srodki kontrastowe, dawki i zmiennosc akwizycji.

## **2.7 Znaczenie dla pracy magisterskiej**

Artykul jest bardzo przydatny jako zrodlo metodologiczne dla czesci virtual DCE. Chociaz nie generuje obrazu post-kontrastowego z sekwencji calkowicie niekontrastowych, pokazuje wazna idee: w DCE-MRI nalezy zachowac dynamike wzmocnienia, a nie tylko podobienstwo obrazu.

Dla tematu _Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis_ najwazniejsze sa trzy inspiracje.

Po pierwsze, preprocessing. TI-norm pokazuje, ze normalizacja obrazow DCE-MRI musi uwzgledniac relacje pomiedzy fazami czasowymi. W mojej pracy warto uwazac na klasyczne min-max lub z-score liczone osobno dla kazdego slice'a, poniewaz moga usuwac informacje o rzeczywistych roznicach intensywnosci.

Po drugie, funkcja straty. TI-loss jest dobrym przykladem tego, ze funkcja celu moze byc dopasowana do sensu klinicznego zadania. W mojej pracy mozna rozważyć podobna idee: poza L1/L2/SSIM loss dodac skladnik, ktory wzmacnia zgodnosc w obszarze piersi lub lesion ROI.

Po trzecie, ewaluacja. Artykul bardzo dobrze uzasadnia, ze SSIM i PSNR powinny byc tylko czescia oceny. Dla vDCE warto raportowac wyniki osobno dla calego obrazu, maski piersi oraz potencjalnie lesion ROI. Jesli w danych dostepne sa fazy czasowe, mozna rozwazyc rowniez metryki podobne do CA Pattern Score lub Average Difference in Enhancement.

Elementy mozliwe do wykorzystania w pracy:

- opis klinicznego znaczenia early i late DCE-MRI;
- argument, ze pozna faza pomaga w interpretacji zmian przez krzywa time-intensity;
- inspiracja do normalizacji intensywnosci;
- inspiracja do funkcji straty uwzgledniajacej kontrast enhancement;
- metryki SSIM, PSNR, MAE jako baseline;
- dodatkowe metryki ROI/time-intensity jako bardziej klinicznie sensowna ocena;
- uzasadnienie lesion-focused analysis.

## **2.8 Ocena przydatnosci**

## **Ocena: 5/5**

Artykul jest bardzo przydatny dla pracy magisterskiej, poniewaz bezposrednio dotyczy breast DCE-MRI i syntezy obrazow kontrastowych. Jego najwieksza wartosc polega na pokazaniu, ze w zadaniach virtual DCE nie wystarczy wygenerowac obraz podobny wizualnie. Trzeba takze zachowac klinicznie istotny wzorzec wzmocnienia kontrastowego.

Ograniczeniem jest to, ze praca syntetyzuje late post-contrast z early post-contrast, a nie pelny obraz post-kontrastowy z sekwencji niekontrastowych. Mimo to artykul jest jednym z najlepszych zrodel do rozdzialu o metodach syntezy DCE-MRI, preprocessingu, funkcjach straty i ewaluacji zorientowanej klinicznie.
