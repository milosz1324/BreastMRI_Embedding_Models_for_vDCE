## **3 Vascularity and Dynamic Contrast-Enhanced Breast Magnetic Resonance Imaging**

## **3.1 Dane bibliograficzne**

- **Tytul:** Vascularity and Dynamic Contrast-Enhanced Breast Magnetic Resonance Imaging

- **Autorzy:** David E. Frankhouser, Eric Dietze, Ashish Mahabal, Victoria L. Seewaldt

- **Rok:** 2021

- **Typ publikacji:** Review article, Frontiers in Radiology, sekcja Artificial Intelligence in Radiology

- **DOI:** https://doi.org/10.3389/fradi.2021.735567

- **Link:** https://www.frontiersin.org/journals/radiology/articles/10.3389/fradi.2021.735567/full

## **3.2 Problem**

Artykul omawia znaczenie unaczynienia i angiogenezy w raku piersi oraz mozliwosci oceny tych zjawisk za pomoca dynamicznego obrazowania kontrastowego MRI. Autorzy podkreslaja, ze angiogeneza jest waznym etapem rozwoju i progresji inwazyjnego raka piersi. Klasyczna ocena mikrogestosci naczyn w materiale biopsyjnym ma wartosc prognostyczna, ale jest ograniczona przez zmiennosc oceny miedzy specjalistami oraz przez fakt, ze pojedynczy przekroj tkanki nie oddaje calej heterogenicznosci guza.

Glowny problem artykulu polega na tym, jak wykorzystac DCE-MRI do oceny unaczynienia piersi i guzow, mimo ze MRI nie obrazuje biologii naczyn bezposrednio. DCE-MRI pokazuje raczej zmiany sygnalu po podaniu gadolinowego srodka kontrastowego. W praktyce naczynia i obszary patologiczne sa wykrywane posrednio przez szybkie wzmocnienie kontrastowe oraz charakterystyczna morfologie.

Autorzy wskazuja trzy duze ograniczenia DCE-MRI w analizie naczyn:

- DCE-MRI mierzy zachowanie kontrastu gadolinowego, a nie bezposrednio proces biologiczny;
- rozdzielczosc klinicznego MRI 1.5T i 3T jest niewystarczajaca do obrazowania malych mikronaczyn;
- obrazy DCE-MRI sa trudne do wspolrejestrowania ze wzgledu na ruch i deformacje piersi.

Z punktu widzenia mojej pracy artykul jest wazny jako kliniczne i biologiczne uzasadnienie dla virtual DCE. Pokazuje, dlaczego dynamika kontrastu jest istotna diagnostycznie i dlaczego sama rekonstrukcja ladnego obrazu moze nie wystarczyc.

Artykul jest zwiazany z:

- foundation models: nie bezposrednio;
- MRI: tak;
- breast MRI: tak, bezposrednio;
- virtual contrast / vDCE: posrednio, przez opis znaczenia DCE-MRI i gadolinowego kontrastu;
- image synthesis: nie bezposrednio;
- embeddings / representation learning: posrednio, jako kontekst kliniczny dla cech, ktore embedding powinien zachowywac.

## **3.3 Dane**

Artykul ma charakter przegladowy, wiec autorzy nie trenuja jednego modelu na jednym zbiorze danych. Omawiaja literature dotyczaca DCE-MRI piersi, detekcji naczyn, analizy radiomicznej, modelowania farmakokinetycznego oraz metod uczenia maszynowego w analizie obrazow MRI piersi.

Opisywana modalnosc to dynamic contrast-enhanced breast MRI, czyli sekwencje MRI obejmujace obraz przed podaniem kontrastu oraz obrazy po podaniu kontrastu. Autorzy podkreslaja, ze w praktyce klinicznej DCE-MRI jest stosowane do:

- screeningu kobiet o wysokim ryzyku raka piersi;
- oceny lokalnego zaawansowania raka;
- planowania leczenia neoadjuwantowego i adjuwantowego;
- oceny odpowiedzi na leczenie;
- planowania zabiegow chirurgicznych i radioterapii.

W artykule nie ma jednego okreslonego inputu i targetu, poniewaz nie jest to praca eksperymentalna z jednym pipeline'em uczenia. W omawianych metodach inputem sa zwykle obrazy DCE-MRI, czesto obrazy subtraction lub maximum intensity projection, a targetem moze byc detekcja guza, klasyfikacja zmiany, parametry farmakokinetyczne lub detekcja naczyn.

W kontekscie mojej pracy wazne jest to, ze DCE-MRI wykorzystuje informacje czasowa: poczatkowe wzmocnienie, opozniona faze oraz washout. Jesli model vDCE ma byc klinicznie uzyteczny, powinien zachowywac przynajmniej czesc tych wzorcow, a nie tylko odtwarzac globalna intensywnosc obrazu.

## **3.4 Metoda**

Artykul nie proponuje jednej nowej architektury, lecz porzadkuje metody obliczeniowe stosowane w analizie breast DCE-MRI.

Autorzy omawiaja kilka grup metod:

- analiza krzywych kinetycznych, czyli ocena zmian intensywnosci sygnalu w czasie;
- modele farmakokinetyczne, szczegolnie warianty modelu Toftsa;
- klasyczne metody uczenia maszynowego, takie jak logistic regression, linear discriminant analysis, random forests i support vector machines;
- metody nienadzorowane, np. fuzzy C-means;
- sieci neuronowe i deep learning, szczegolnie CNN;
- radiomics, czyli ekstrakcje cech morfologicznych, histogramowych, teksturalnych i transformacyjnych;
- metody detekcji naczyn w 2D i 3D, m.in. Hessian morphology filters oraz seed growth.

W czesci dotyczacej DCE-MRI autorzy wyjasniaja, ze klasyczna analiza diagnostyczna wykorzystuje zarowno cechy morfologiczne, jak i dynamike kontrastu. Zmiany zlosliwe czesto charakteryzuja sie szybkim uptake i washout, co jest zwiazane ze zwiekszona waskularyzacja guza.

W czesci dotyczacej deep learningu autorzy wskazuja, ze CNN-y sa dobrze dopasowane do analizy obrazow, poniewaz zachowuja relacje przestrzenne miedzy cechami. Jednoczesnie podkreslaja, ze deep learning wymaga duzych, dobrze anotowanych zbiorow danych. Transfer learning moze zmniejszyc te wymagania, co jest wazne rowniez dla mojej pracy z embeddingami.

Metoda omawiana w artykule nie jest:

- generatywna;
- diffusion/GAN;
- self-supervised;
- bezposrednio embedding-based.

Jest to przede wszystkim przeglad metod analizy i interpretacji DCE-MRI piersi.

## **3.5 Ewaluacja**

Poniewaz artykul jest przegladem literatury, nie ma jednej wspolnej ewaluacji modelu. Autorzy omawiaja rozne typy metryk w zaleznosci od zadania.

Dla metod detekcji i klasyfikacji guzow pojawiaja sie klasyczne miary diagnostyczne:

- sensitivity;
- specificity;
- false positive rate;
- false negative rate;
- agreement z ocena ekspertow.

Dla segmentacji lub detekcji naczyn opisywane sa m.in. skutecznosc detekcji, czulosc, swoistosc i zgodnosc z ocena ekspercka. W tabeli dotyczacej badan nad detekcja naczyn autorzy przytaczaja m.in. prace, w ktorych algorytmy osiagaly wysoka czulosc w 3D vessel detection albo zmniejszaly liczbe falszywie dodatnich detekcji po usunieciu struktur naczyniowych.

Metryki takie jak SSIM, PSNR, MAE i MSE nie sa omawiane jako glowne metryki, poniewaz artykul nie dotyczy syntezy obrazow. Dla mojej pracy to wazna roznica: ten artykul pomaga uzasadnic kliniczny sens DCE-MRI, ale metryki rekonstrukcji nalezy czerpac z artykulow o image synthesis.

Artykul bardzo mocno podkresla problem generalizacji: protokoly DCE-MRI roznia sie miedzy osrodkami, rodzajem kontrastu, dawka, sila pola magnetycznego i strategia akwizycji. To oznacza, ze model oceniony tylko na jednym zbiorze moze nie dzialac dobrze w innych warunkach klinicznych.

## **3.6 Najwazniejsze wnioski**

Najwazniejszy wniosek jest taki, ze DCE-MRI jest bardzo czula i klinicznie wazna metoda obrazowania piersi, ale jej analiza obliczeniowa jest trudna. Obrazy DCE-MRI sa dynamiczne, trójwymiarowe, podatne na ruch i zalezne od protokolu akwizycji. Dodatkowo sygnal kontrastowy jest tylko posrednim odzwierciedleniem biologii guza i unaczynienia.

Autorzy podkreslaja, ze analiza naczyn w breast DCE-MRI jest trudniejsza niz w wielu innych typach obrazow, poniewaz piers jest tkanka heterogeniczna, odksztalcalna i rozni sie znacznie miedzy pacjentkami. Fibroglandular tissue, adipose tissue i tlo moga utrudniac automatyczna detekcje struktur o liniowej morfologii.

Dla pracy magisterskiej szczegolnie wazne sa nastepujace wnioski:

- DCE-MRI jest standardowa i bardzo czula metoda diagnostyki raka piersi;
- informacja czasowa i kinetyczna jest klinicznie istotna;
- protokoly DCE-MRI roznia sie miedzy osrodkami i skanerami;
- analiza obrazow powinna uwzgledniac heterogenicznosc piersi;
- klasyczne modele i deep learning moga wspierac analize, ale wymagaja duzych i dobrze przygotowanych danych;
- generalizacja kliniczna jest duzym wyzwaniem.

Co wyglada przekonujaco:

- artykul dobrze uzasadnia, dlaczego DCE-MRI jest wazne klinicznie;
- pokazuje zwiazek miedzy kontrastem, unaczynieniem i agresywnoscia biologiczna;
- szeroko opisuje ograniczenia techniczne DCE-MRI;
- dobrze tlumaczy, dlaczego analiza piersi jest trudna obliczeniowo.

Co jest slabe lub niejasne:

- artykul nie proponuje konkretnego modelu do syntezy obrazow;
- nie daje gotowego pipeline'u do vDCE;
- jest bardziej kliniczno-przegladowy niz eksperymentalny;
- wiele omawianych metod dotyczy vessel detection, a nie bezposrednio image-to-image synthesis.

## **3.7 Znaczenie dla pracy magisterskiej**

Artykul jest przydatny przede wszystkim do rozdzialu wprowadzajacego i motywacyjnego. Wyjasnia, dlaczego DCE-MRI jest istotne w diagnostyce raka piersi oraz dlaczego obrazy po podaniu kontrastu zawieraja informacje kliniczna zwiazana z waskularyzacja, perfuzja i dynamika uptake/washout.

W kontekscie tematu _Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis_ artykul pomaga uzasadnic, dlaczego celem nie powinno byc tylko wygenerowanie obrazu o wysokim SSIM lub PSNR. Model powinien zachowywac cechy zwiazane z tkanka piersi, dynamika kontrastu i potencjalnie regionami podejrzanymi klinicznie.

Elementy mozliwe do wykorzystania w pracy:

- opis roli DCE-MRI w screeningu i diagnostyce raka piersi;
- uzasadnienie znaczenia kontrastu gadolinowego;
- opis ograniczen DCE-MRI: koszt, protokoly, ruch, rozdzielczosc, heterogenicznosc;
- argument, ze analiza kliniczna wymaga uwzglednienia dynamiki wzmocnienia;
- motywacja dla lesion-focused lub breast-mask-focused evaluation;
- uzasadnienie potrzeby odpornosci modelu na zmiennosc akwizycji.

Artykul nie dostarcza bezposrednio architektury modelu do wykorzystania, ale pomaga zdefiniowac, jakie informacje powinien zachowywac model embeddingowy i generatywny.

## **3.8 Ocena przydatnosci**

## **Ocena: 4/5**

Artykul jest bardzo przydatny jako tlo kliniczne i biologiczne. Dobrze nadaje sie do wstepu oraz czesci opisujacej znaczenie DCE-MRI piersi. Jego ograniczeniem jest to, ze nie dotyczy bezposrednio virtual DCE ani syntezy obrazow. Dlatego powinien byc traktowany jako artykul motywacyjny i kliniczny, a nie jako glowne zrodlo metodologii modelu generatywnego.
