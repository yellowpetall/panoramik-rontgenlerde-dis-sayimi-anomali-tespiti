# Deney 03: Görev 2 Pseudo-Labeling ile Healthy (Sağlıklı Diş) Sınıfı Ekleme

## Yapılan Değişiklikler
* **Hiyerarşik Etiket Üretimi (Pseudo-Labeling):** Görev 2 (`quadrant_enumeration` hemisection YOLOv8s) ağırlıkları kullanılarak 705 röntgendeki tüm dişler tespit edildi. Gerçek anomali kutularıyla çakışmayan (`IoU < 0.30`) **16.831** dişe `4: Healthy` sınıfı eklendi.
* **Eğitim Kurulumu:** CLAHE ön işleme + `imgsz=1024` + `yolov8s.pt` ile 5 sınıflı model eğitildi ve aynı 107 test görüntüsü üzerinde değerlendirildi.

## Test Seti Metrikleri (Aynı 107 Test Görüntüsü)

| Sınıf / Genel | Precision (P) | Recall (R) | AP50 | AP70 | AP50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **5 Sınıf Genel (Healthy Dahil)** | **0.579** | **0.631** | **0.567** | **0.508** | **0.388** |
| **4 Anomali Ortalaması (Adil Kıyas)** | **0.505** | **0.556** | **0.478** | **0.417** | **0.306** |
| **Impacted** | 0.779 | 0.942 | 0.871 | 0.779 | 0.550 |
| **Caries** | 0.329 | 0.541 | 0.364 | 0.354 | 0.259 |
| **Periapical Lesion** | 0.473 | 0.288 | 0.272 | 0.177 | 0.159 |
| **Deep Caries** | 0.439 | 0.453 | 0.403 | 0.357 | 0.254 |
| **Healthy (Pseudo-Label)** | 0.873 | 0.930 | 0.924 | 0.872 | 0.718 |

## Çıkarımlar ve Sonraki Adım
* `Healthy` sınıfının eklenmesiyle 4 anomali sınıfının `mAP70` skoru **+5.2 puan** (`0.365 → 0.417`), `Deep Caries` `AP50` skoru **+7.1 puan** (`0.332 → 0.403`) ve `Periapical Lesion` `AP50` skoru **+7.2 puan** (`0.200 → 0.272`) arttı.
* Ancak DENTEX veri setindeki kısmi çürük etiketlemeleri nedeniyle pseudo-label olarak atanan `Healthy` kutuları ile hafif `Caries` vakaları çakışmakta ve tek aşamalı tespit mimarisi ~0.48 `mAP50` sınırına dayanmaktadır.
* **Deney 04:** Tespit edilen diş kutularının yakın çekim kırpılıp (**Crop**) ayrı bir **CNN (ResNet50 / EfficientNet)** sınıflandırıcısı ile eğitildiği 2 aşamalı mimariye geçilecektir.