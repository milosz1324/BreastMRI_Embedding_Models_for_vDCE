## **Pracownia problemowa magisterska**

Temat: **Breast MRI Embedding Models for Virtual Dynamic Contrast-Enhanced Image Synthesis**

Specjalnosc: Sztuczna Inteligencja / Wizja komputerowa

Ten dokument nie jest elementem pracy magisterskiej, tylko nieformalnym krótkim podsumowaniem koncepcji, aktualnego rozpoznania literatury oraz planu pierwszego etapu pracy nad realizacją pracy magisterskiej.

## **1. Cel pracy**

Celem pracy jest sprawdzenie, czy reprezentacje embeddingowe wyuczone na pojedynczych przekrojach 2D MRI piersi moga poprawic synteze obrazow po kontraście, czyli virtual DCE, w porownaniu z bezposrednim podejsciem image-to-image.

Praca jest planowana w dwoch glownych etapach:

1. Wytrenowanie lub adaptacja modelu embeddingowego dla pojedynczych przekrojow 2D MRI piersi.
2. Uzycie embeddingow jako warunku lub reprezentacji pomocniczej w modelu generatywnym rekonstruujacym obrazy post-contrast.

Glowna hipoteza robocza jest taka, ze model generatywny korzystajacy z reprezentacji embeddingowej moze uzyskac lepsza jakosc rekonstrukcji, wieksza stabilnosc oraz lepsze zachowanie struktur klinicznie istotnych niz prosty model direct image-to-image.

## **2. Rozszerzony kontekst kliniczny**

Dynamic contrast-enhanced breast MRI jest jedna z najczulszych metod obrazowania stosowanych w diagnostyce raka piersi, screeningu pacjentek wysokiego ryzyka, ocenie rozleglosci choroby, planowaniu leczenia oraz monitorowaniu odpowiedzi na terapie. Obrazy DCE-MRI powstaja po podaniu gadolinowego srodka kontrastowego i pozwalaja obserwowac, jak tkanki wzmacniaja sie w czasie.

Znaczenie DCE-MRI wynika z biologii nowotworu. Zmiany zlosliwe czesto charakteryzuja sie nasilona angiogeneza, zwiekszona przepuszczalnoscia naczyn i odmienna dynamika perfuzji. W praktyce radiologicznej istotne sa nie tylko cechy morfologiczne zmiany, ale takze dynamika kontrastu: szybkie wzmocnienie, plateau albo washout. Informacja ta moze pomagac w roznicowaniu zmian lagodnych i zlosliwych oraz w ocenie agresywnosci biologicznej.

Jednoczesnie klasyczne DCE-MRI ma istotne ograniczenia. Wymaga podania srodka kontrastowego, wydluza badanie, zwieksza koszt procedury i moze byc problematyczne u wybranych pacjentek. Dodatkowo protokoly DCE-MRI roznia sie miedzy osrodkami, skanerami, dawkami i rodzajami kontrastu, co utrudnia generalizacje modeli AI. Z tego powodu rozwijane sa metody virtual contrast / virtual DCE, ktore maja odtwarzac informacje kontrastowa z obrazow niekontrastowych lub z ograniczonej liczby faz czasowych.

W tej pracy szczegolnie wazne jest to, ze syntetyczny obraz post-contrast nie powinien byc oceniany wylacznie jako obraz podobny pikselowo do obrazu referencyjnego. W zastosowaniu klinicznym wazne jest zachowanie lokalnych struktur, obszarow wzmocnienia oraz potencjalnie regionow zmian chorobowych. Dlatego poza metrykami globalnymi, takimi jak SSIM i PSNR, warto rozwazyc ocene w masce piersi oraz, jesli bedzie to mozliwe, w lesion ROI.

## **3. Glowne pytania badawcze**

1. Czy embeddingi slice-level ucza sie reprezentacji przydatnych do rekonstrukcji obrazow DCE?
2. Czy model generatywny wspierany embeddingami osiaga lepsze SSIM i PSNR niz bezposredni model image-to-image?
3. Czy embeddingi poprawiaja stabilnosc wynikow pomiedzy pacjentami, przekrojami i wariantami akwizycji?
4. Czy poprawa jest widoczna w obszarach klinicznie istotnych, np. w masce piersi lub w okolicy zmian chorobowych?
5. Czy segmentacja lewej i prawej piersi z BreastDivider moze poprawic preprocessing i ograniczyc wplyw tla na uczenie modelu?

## **4. Planowany zakres pracy**

Minimalny zakres pracy:

1. Przeglad literatury: DCE-MRI piersi, virtual contrast / vDCE, cross-contrast MRI synthesis, foundation models i embeddingi w obrazowaniu medycznym.
2. Analiza BreastDivider dataset: format danych, sekwencje MRI, liczba przypadkow, liczba przekrojow, maski left/right, potencjalne pary pre/post-contrast.
3. Przygotowanie pipeline'u slice-level: wybor osi przekrojow, odrzucanie pustych slice'ow, crop/maskowanie piersi, normalizacja intensywnosci.
4. Baseline direct image-to-image, np. 2D U-Net rekonstruujacy post-contrast z non-contrast input.
5. Model embeddingowy, np. encoder CNN/ViT trenowany self-supervised albo na proxy task.
6. Model vDCE z embeddingami, w ktorym rekonstrukcja obrazu jest warunkowana reprezentacja embeddingowa.
7. Ewaluacja: SSIM, PSNR, MAE/MSE, analiza wizualna, metryki w masce piersi, opcjonalnie lesion-focused analysis.

Mozliwe rozszerzenia:

1. Porownanie kilku typow embeddingow: CNN, ViT, DINO/MAE-style self-supervised.
2. Analiza generalizacji na danych klinicznych z Erlangen.
3. Analiza odpornosci na roznice akwizycji.
4. Ablacje: rozmiar embeddingu, sposob laczenia embeddingu z generatorem, liczba slice'ow.
5. Lesion-focused metrics, jesli beda dostepne maski lub bounding boxy zmian.

## **5. Etap 1 pracowni problemowej**

Na potrzeby pierwszego etapu pracowni problemowej przygowane zostały następujące elementy:

1. **Opracowanie literatury.** Wybrane artykuly zostaly lub zostana przeanalizowane wedlug wspolnego template'u oceny artykulu. Wybralem przede wszystkim publikacje, ktore moim zdaniem najlepiej wspieraja realizacje pracy: kontekst kliniczny DCE-MRI, synteze obrazow kontrastowych, foundation models/embeddingi, dataset BreastDivider oraz metryki oceny.
2. **Rozpoznanie BreastDivider dataset.** Celem jest sprawdzenie, czy dataset zawiera przypadki przydatne do zadania vDCE, szczegolnie pary pre-contrast i post-contrast, oraz jak mozna wykorzystac maski lewej i prawej piersi.

Planowane wyniki Etapu 1:

- tabela literatury z podzialem tematycznym;
- kilka kart oceny artykulow przygotowanych wedlug `LITERATURE_REVIEW_TEMPLATE.md`;
- wstepny opis BreastDivider i powiazanych datasetow;
- notebook/skrypt eksploracyjny datasetu;
- decyzja, czy dane sa wystarczajace do trenowania modelu vDCE;

## **6. Aktualnie opracowane artykuly**

Do tej pory przygotowano kilka kart oceny artykulow, wybranych jako najbardziej przydatne dla realizacji pracy:

| Obszar | Artykul | Plik |
| --- | --- | --- |
| Foundation models / embeddingi | Foundation Models in Medical Imaging: A Review and Outlook | `Overview__Foundation_Models_in_Medical_Imaging__A_Review_and_Outlook.md` |
| Kontekst kliniczny DCE-MRI | Vascularity and Dynamic Contrast-Enhanced Breast Magnetic Resonance Imaging | `Vascularity_and_DCE_Breast_MRI_Literature_Review.md` |
| Synteza DCE-MRI piersi | Synthesizing Late-Stage Contrast Enhancement in Breast MRI | `Synthesizing_Late_Stage_Contrast_Enhancement_Breast_MRI_Literature_Review.md` |
| Dataset BreastDivider | Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation | `Divide_and_Conquer_BreastDivider_Literature_Review.md` |
| Cross-contrast MRI synthesis | A review on cross-contrast MRI image synthesis through deep learning | `Cross_Contrast_MRI_Synthesis_Deep_Learning_Review.md` |

## **7. Tabela literatury roboczej**

| Obszar | Artykul / zrodlo | Link | Znaczenie dla pracy |
| --- | --- | --- | --- |
| MRI piersi i DCE-MRI | Vascularity and Dynamic Contrast-Enhanced Breast Magnetic Resonance Imaging | https://pmc.ncbi.nlm.nih.gov/articles/PMC10364989/ | Kontekst kliniczny: rola kontrastu, unaczynienie, ograniczenia DCE-MRI. |
| MRI piersi i DCE-MRI | Diffusion Breast MRI: Current Standard and Emerging Techniques | https://pmc.ncbi.nlm.nih.gov/articles/PMC9307963/ | Tlo dla sekwencji niekontrastowych, szczegolnie DWI. |
| MRI piersi i DCE-MRI | Abbreviated Breast MRI: State of the Art | https://pubs.rsna.org/doi/abs/10.1148/radiol.221822 | Uzasadnienie skracania protokolow MRI i znaczenia alternatyw dla pelnego DCE. |
| Virtual DCE / breast MRI synthesis | Virtual Dynamic Contrast Enhanced MRI of the Breast using a U-Net | https://archive.ismrm.org/2022/1522.html | Bezposredni przyklad vDCE breast MRI z uzyciem U-Net. |
| Virtual DCE / breast MRI synthesis | Tumor-Attentive Segmentation-Guided GAN for Synthesizing Breast Contrast-Enhanced MRI Without Contrast Agents | https://pmc.ncbi.nlm.nih.gov/articles/PMC9721354/ | Synteza contrast-enhanced breast MRI z pre-contrast T1; analiza tumor ROI. |
| Virtual DCE / breast MRI synthesis | Simulating Dynamic Tumor Contrast Enhancement in Breast MRI using Conditional Generative Adversarial Networks | https://arxiv.org/abs/2409.18872 | Generowanie dynamicznego zachowania kontrastu w breast MRI. |
| Virtual DCE / breast MRI synthesis | Synthesizing Late-Stage Contrast Enhancement in Breast MRI | https://arxiv.org/abs/2409.01596 | Synteza late DCE z early DCE; wazne dla dynamiki time-intensity. |
| Generative DCE-MRI | DCE-diff: Diffusion Model for Synthesis of Early and Late Dynamic Contrast-Enhanced MR Images | https://openaccess.thecvf.com/content/CVPR2024W/DEF-AI-MIA/html/M_DCE-diff_Diffusion_Model_for_Synthesis_of_Early_and_Late_Dynamic_CVPRW_2024_paper.html | Inspiracja metodologiczna: diffusion, multimodal input, SSIM/PSNR/MAE/FID. |
| Generative DCE-MRI | DCE-FORMER | https://arxiv.org/abs/2402.02125 | Przyklad transformerowego podejscia do predykcji early/late DCE. |
| Generative DCE-MRI | AAD-DCE | https://arxiv.org/abs/2502.02555 | Inspiracja do multimodalnego wejscia i attention. |
| Embeddingi / foundation models | Foundation Models in Medical Imaging -- A Review and Outlook | https://arxiv.org/abs/2506.09095 | Podstawowe pojecia: foundation model, embedding, pretraining, downstream task. |
| Embeddingi / self-supervised learning | Models Genesis | https://pmc.ncbi.nlm.nih.gov/articles/PMC7405596/ | Klasyczny przyklad self-supervised representation learning w medical imaging. |
| Embeddingi / self-supervised learning | Self-supervised learning for medical image analysis using image context restoration | https://pmc.ncbi.nlm.nih.gov/articles/PMC7613987/ | Uzasadnienie uczenia reprezentacji bez pelnych etykiet. |
| Embeddingi / transfer learning | Med3D | https://arxiv.org/abs/1904.00625 | Transfer learning dla 3D medical image analysis. |
| Embeddingi / masked modeling | Masked Image Modeling Advances 3D Medical Image Analysis | https://openaccess.thecvf.com/content/WACV2023/papers/Chen_Masked_Image_Modeling_Advances_3D_Medical_Image_Analysis_WACV_2023_paper.pdf | Inspiracja do masked autoencoder / masked image modeling. |
| Dataset BreastDivider | Divide and Conquer: A Large-Scale Dataset and Model for Left-Right Breast MRI Segmentation | https://arxiv.org/abs/2507.13830 | Glowny artykul o BreastDivider. |
| Dataset BreastDivider | BreastDividerDataset - Hugging Face dataset card | https://huggingface.co/datasets/Bubenpo/BreastDividerDataset | Praktyczne zrodlo: licencja, struktura, zawartosc datasetu. |
| Powiazane datasety | Duke-Breast-Cancer-MRI - TCIA | https://www.cancerimagingarchive.net/collection/duke-breast-cancer-mri/ | Zrodlo danych DCE-MRI wykorzystywane w wielu pracach i datasetach. |
| Powiazane datasety | MAMA-MIA | https://arxiv.org/abs/2406.13844 | Multi-center breast DCE-MRI benchmark z segmentacjami ekspertow. |
| Powiazane datasety | BreastDCEDL | https://pmc.ncbi.nlm.nih.gov/articles/PMC12917191/ | Deep learning-ready dataset DCE-MRI oparty m.in. na Duke/I-SPY. |
| Metryki | Image Quality Assessment: From Error Visibility to Structural Similarity | https://live.ece.utexas.edu/publications/2004/zwang_ssim_ieeeip2004.pdf | Klasyczny artykul wprowadzajacy SSIM. |
| Metryki | On the proper use of structural similarity for robust evaluation of medical image synthesis models | https://pubmed.ncbi.nlm.nih.gov/35106778/ | Ograniczenia i dobre praktyki raportowania SSIM w medical image synthesis. |
| Metody syntezy MRI | A review on cross-contrast MRI image synthesis through deep learning | https://link.springer.com/article/10.1007/s44352-025-00012-3 | Przeglad metod, architektur i metryk dla MRI image synthesis. |

## **8. Najblizsze kroki**

1. Dopracowanie kart oceny artykulow i wybor 5-6 najwazniejszych publikacji do bezposredniego cytowania w pierwszej czesci pracy.
2. Pobranie i rozpoznanie struktury BreastDivider.
3. Przygotowanie notebooka EDA dla datasetu: formaty plikow, liczba przypadkow, modalnosci, pary pre/post-contrast, maski left/right.
4. Zaprojektowanie pipeline'u slice-level i podstawowego baseline'u direct image-to-image.
