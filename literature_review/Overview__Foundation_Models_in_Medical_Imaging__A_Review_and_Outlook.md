## **1 Foundation Models in Medical Imaging: A Review and Outlook** 

## **1.1 Dane bibliograficzne** 

- **Tytul:** Foundation Models in Medical Imaging: A Review and Outlook 

- **Autorzy:** Vivien van Veldhuizen, Vanessa Botha, Chunyao Lu, Melis Erdal Cesur, Kevin Groot Lipman, Edwin D. de Jong, Hugo Horlings, Clarisa I. Sanchez, Cees G. M. Snoek, Lodewyk Wessels, Ritse Mann, Eric Marcus, Jonas Teuwen 

- **Rok:** 2025 

- **Typ publikacji:** arXiv preprint, arXiv:2506.09095, wersja v4 z 18.11.2025 

- **Link:** https://arxiv.org/abs/2506.09095 

## **1.2 Problem** 

Artykul porzadkuje aktualny stan badan nad modelami fundamentalnymi w obrazowaniu medycznym. Autorzy wyjasniaja, czym sa foundation models, jak wyglada typowy pipeline ich tworzenia oraz jak takie modele sa stosowane w trzech glownych obszarach: patologii cyfrowej, radiologii i okulistyce. 

Glowny problem omawiany w artykule polega na tym, ze w medycynie dostep do duzych, dobrze opisanych zbiorow danych jest ograniczony, a klasyczne modele nadzorowane wymagaja duzej liczby etykiet. Foundation models maja zmniejszyc zaleznosc od recznej anotacji dzieki uczeniu na duzych zbiorach danych, czesto bez etykiet, oraz pozniejszej adaptacji do konkretnych zadan klinicznych. 

Z punktu widzenia niniejszej pracy artykul jest zwiazany przede wszystkim z modelami fundamentalnymi, uczeniem reprezentacji oraz embeddingami. Tematyka MRI pojawia sie jako czesc szerszej dyskusji o radiologii, szczegolnie w kontekscie danych 3D i ograniczen obliczeniowych. Artykul nie dotyczy jednak bezposrednio breast MRI ani virtual DCE. 

## **1.3 Dane** 

Artykul ma charakter przegladowy, dlatego autorzy nie trenuja jednego wlasnego modelu na jednym zbiorze danych. Zamiast tego analizuja ponad 150 publikacji dotyczacych foundation models oraz self-supervised learning w obrazowaniu medycznym. 

Autorzy omawiaja wiele modalnosci obrazowania, m.in. obrazy histopatologiczne, RTG, CT, MRI, ultrasound, PET oraz obrazy okulistyczne, takie jak OCT i fundus photography. W sekcji radiologicznej MRI jest traktowane jako modalnosc przestrzenna, ktora dostarcza szczegolowych informacji o tkankach miekkich, ale jednoczesnie generuje istotne trudnosci obliczeniowe ze wzgledu na charakter danych 3D. 

1 

Poniewaz jest to artykul przegladowy, nie wystepuje jeden okreslony input, target ani podzial danych na zbiory treningowe i testowe. Autorzy podkreslaja jednak, ze ograniczona dostepnosc danych klinicznych oraz brak standaryzacji utrudniaja reprodukowalnosc i porownywanie modeli. Dla niniejszej pracy istotny jest wniosek metodologiczny, ze w eksperymentach na breast MRI podzial danych powinien byc wykonywany na poziomie pacjenta, a nie pojedynczych przekrojow, aby uniknac data leakage. 

## **1.4 Metoda** 

Artykul nie proponuje jednej konkretnej architektury, lecz porownuje najwazniejsze rodziny modeli wykorzystywanych jako foundation models w obrazowaniu medycznym. Omawiane sa m.in.: 

- konwolucyjne sieci neuronowe, np. ResNet i ConvNeXt; 

- Vision Transformers, np. ViT i Swin Transformer; 

- modele vision-language inspirowane CLIP; 

- modele 3D dla CT i MRI; 

- modele promptable, np. medyczne warianty Segment Anything; 

- metody adaptacji modeli, takie jak task-specific heads, adaptery, LoRA i fine-tuning. 

Centralnym pojeciem artykulu jest reprezentacja embeddingowa. Foundation model po etapie pretrainingu zamienia dane obrazowe na wysokowymiarowe reprezentacje, ktore moga byc pozniej wykorzystane w wielu zadaniach downstream, takich jak klasyfikacja, segmentacja, detekcja, retrieval, generowanie raportow albo synteza obrazow. 

Autorzy omawiaja wiele strategii uczenia reprezentacji, w tym contrastive learning, self-distillation, masked image modeling oraz vision-language contrastive learning. Dla niniejszej pracy szczegolnie istotne sa podejscia typu MAE, DINO/DINOv2 oraz ogolna idea encodera uczonego self-supervised, ktory nastepnie moze sluzyc jako zrodlo embeddingow dla modelu generatywnego. 

Waznym aspektem jest takze sposob wykorzystania informacji przestrzennej. Autorzy wskazuja, ze radiologia, a zwlaszcza CT i MRI, stawia dodatkowe wyzwania, poniewaz dane czesto maja charakter 3D. Pelne modele 3D sa kosztowne obliczeniowo, dlatego wiele prac wykorzystuje przekroje 2D lub podejscia posrednie. Jest to bezposrednio istotne dla niniejszej pracy, poniewaz planowany model embeddingowy ma dzialac na poziomie pojedynczych przekrojow 2D MRI piersi. 

2 

## **1.5 Ewaluacja** 

Poniewaz artykul jest przegladem literatury, nie zawiera jednej wspolnej tabeli wynikow eksperymentalnych. Omawiane prace stosuja rozne metryki w zaleznosci od zadania, np. accuracy i AUROC dla klasyfikacji, Dice i IoU dla segmentacji, a takze metryki zwiazane z retrieval, visual question answering lub generowaniem raportow. 

Metryki takie jak SSIM, PSNR, MAE i MSE nie sa glownym tematem artykulu. Sa one bardziej charakterystyczne dla zadan rekonstrukcji i syntezy obrazow, takich jak virtual DCE. W kontekscie niniejszej pracy artykul jest wiec wazniejszy jako zrodlo teoretyczne dla embeddingow i foundation models niz jako bezposrednie zrodlo metryk dla oceny jakosci syntezy obrazow. 

Autorzy omawiaja rowniez znaczenie oceny klinicznej, interpretowalnosci, odpornosci modeli, biasu, fairness oraz regulacji. Nie przeprowadzaja jednak wlasnej oceny klinicznej ani analizy lesion-focused. 

## **1.6 Najwazniejsze wnioski** 

Najwazniejszy wniosek z artykulu jest taki, ze foundation models sa obiecujacym kierunkiem w obrazowaniu medycznym, poniewaz pozwalaja uczyc sie ogolnych reprezentacji z duzych zbiorow danych i adaptowac je do wielu zadan przy ograniczonej liczbie etykiet. 

Autorzy podkreslaja jednak, ze wdrozenie takich modeli w medycynie nadal napotyka istotne bariery. Naleza do nich ograniczona dostepnosc otwartych danych klinicznych, wysokie koszty obliczeniowe, trudnosc pracy z danymi 3D, potrzeba interpretowalnosci oraz koniecznosc walidacji modeli w warunkach klinicznych. 

Dla niniejszej pracy szczegolnie istotne sa nastepujace obserwacje: 

- embeddingi moga stanowic uniwersalna reprezentacje obrazow medycznych; 

- self-supervised learning pozwala ograniczyc zaleznosc od recznych etykiet; 

- encodery typu CNN lub ViT moga byc adaptowane do zadan downstream; 

- praca na przekrojach 2D MRI jest praktycznym kompromisem wobec kosztow pelnych modeli 3D; 

- modele medyczne musza byc oceniane nie tylko metrykami technicznymi, ale takze pod katem odpornosci, generalizacji i potencjalnej przydatnosci klinicznej. 

## **1.7 Znaczenie dla pracy magisterskiej** 

Artykul stanowi dobre zrodlo do rozdzialu teoretycznego. Moze zostac wykorzystany do wyjasnienia, czym sa foundation models w obrazowaniu medycznym, dlaczego embeddingi sa istotne oraz jakie znaczenie ma self-supervised learning w sytuacji ograniczonej dostepnosci etykietowanych danych medycznych. 

3 

W kontekscie tematu _Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis_ artykul uzasadnia pierwsza faze pracy, czyli uczenie modelu reprezentacyjnego dla pojedynczych przekrojow 2D MRI piersi. Nie dostarcza jednak szczegolowej metodologii dla virtual DCE, dlatego powinien byc uzupelniony artykulami bezposrednio dotyczacymi syntezy obrazow po kontrascie w breast MRI. 

Elementy mozliwe do wykorzystania w pracy: 

- definicja foundation model jako modelu uczonego na szerokich danych i adaptowanego do wielu zadan; 

- opis embeddingow jako wysokowymiarowych reprezentacji obrazow; 

- opis self-supervised learning, MAE, DINO i contrastive learning; 

- uzasadnienie wyboru modelu slice-level 2D w MRI; 

- dyskusja ograniczen: dane, generalizacja, robustness, interpretowalnosc i walidacja kliniczna. 

## **1.8 Ocena przydatnosci** 

## **Ocena: 4/5** 

Artykul jest bardzo przydatny jako szerokie wprowadzenie do foundation models i reprezentacji embeddingowych w obrazowaniu medycznym. Dobrze nadaje sie do rozdzialu teoretycznego oraz do uzasadnienia, dlaczego warto uczyc reprezentacje obrazow MRI przed etapem syntezy vDCE. Jego ograniczeniem jest to, ze nie dotyczy bezposrednio breast MRI ani virtual DCE, dlatego nie powinien byc traktowany jako glowny artykul metodologiczny dla eksperymentow generatywnych. 

