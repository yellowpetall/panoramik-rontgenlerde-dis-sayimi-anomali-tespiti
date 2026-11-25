# Deney 01: Görev 3 Brute-Force Baseline (YOLOv8n)

## Deney Kurulumu
* **Veri Seti:** DENTEX `quadrant-enumeration-disease` (705 panoramik röntgen: 493 Train / 105 Val / 107 Test)
* **Sınıflar:** `0: Impacted`, `1: Caries`, `2: Periapical Lesion`, `3: Deep Caries` (Sağlıklı diş etiketi henüz eklenmedi)
* **Model & Parametreler:** `yolov8n.pt`, 50 epoch, `imgsz=640`, `batch=16`, `fliplr=0.0` (hiçbir ön işleme uygulanmadı)

## Test Seti Metrikleri (107 Görüntü / 517 Anomali)

| Sınıf / Genel | Test Örnek | Precision (P) | Recall (R) | AP50 | AP70 | AP50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Genel (All)** | **517** | **0.422** | **0.557** | **0.439** | **0.365** | **0.275** |
| **Impacted (Gömülü Diş)** | 90 | 0.789 | 0.956 | 0.882 | 0.728 | 0.529 |
| **Caries (Çürük)** | 296 | 0.273 | 0.659 | 0.343 | 0.326 | 0.239 |
| **Deep Caries (Derin Çürük)** | 106 | 0.389 | 0.415 | 0.332 | 0.233 | 0.195 |
| **Periapical Lesion (Kök Ucu Lezyonu)** | 25 | 0.238 | 0.200 | 0.200 | 0.174 | 0.136 |

## Hata Analizi Bulguları
1. **Gömülü Diş (`Impacted`):** Gerçek örneklerin %96'sı doğru tespit edildi (`AP50: 0.882`). Tek kayıp, komşu azı dişleriyle çakışan yatay 20'lik dişlerde kutu sınırının `IoU > 0.70` eşiğinde kaymasıdır (`AP70: 0.728`).
2. **`Deep Caries` → `Caries` Karışıklığı:** Gerçek derin çürüklerin yalnızca %5'i kaçırılırken **%53'ü** çoğunluk sınıfı olan `Caries` olarak tahmin edildi (`640px` çözünürlükte pulpa yakınlığı detayları kayboluyor).
3. **Kök Ucu Lezyonu (`Periapical Lesion`):** Veri setindeki düşük payı (%4.5) ve kök ucundaki küçük gölge yapısı nedeniyle vakaların %52'si çürük sınıflarıyla karıştırıldı.
4. **Sağlıklı Dişlerin Yanlış Alarm Üretmesi (`background`):** Model sağlıklı dişleri tanımadığı için arka plandaki yanlış pozitiflerin %44'ü `Caries`, %28'i `Deep Caries` olarak işaretlendi.

## Sonraki İyileştirme Adımları
* **Deney 02:** OpenCV CLAHE kontrast iyileştirme + yüksek çözünürlük (`imgsz=1024`) ile ince çürük ve kök ucu detaylarını netleştirme.
* **Deney 03:** Görev 2 diş tespit modeli ile çakışmayan dişlere `Healthy` (Sağlıklı Diş) etiketi üreterek yanlış pozitifleri düşürme.