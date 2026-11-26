# Deney 02: CLAHE Kontrast İyileştirme + 1024px + YOLOv8s

## Yapılan Değişiklikler
* **Ön İşleme:** Tüm röntgenlere LAB renk uzayında `CLAHE (clipLimit=2.0, tileGridSize=(8,8))` uygulandı.
* **Çözünürlük ve Mimari:** `imgsz=640` → `1024`, `yolov8n.pt` → `yolov8s.pt`, `cos_lr=True`, gri tonlamaya zarar veren HSV renk artırımları (`hsv_h`, `hsv_s`) kapatıldı.

## Test Seti Metrikleri (Aynı 107 Test Görüntüsü)

| Sınıf / Genel | Precision (P) | Recall (R) | AP50 | AP70 | AP50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Genel (All)** | **0.503** | 0.465 | **0.448** | **0.376** | **0.283** |
| **Impacted** | 0.742 | 0.978 | 0.884 | 0.712 | 0.521 |
| **Caries** | 0.405 | 0.378 | 0.350 | 0.335 | 0.251 |
| **Periapical Lesion** | 0.373 | 0.200 | 0.239 | 0.204 | 0.160 |
| **Deep Caries** | 0.491 | 0.302 | 0.320 | 0.251 | 0.200 |

## Çıkarımlar
* Genel `Precision` değeri **+8.1 puan** (`0.422 → 0.503`), `mAP70` ise **+1.0 puan** (`0.365 → 0.376`) arttı.
* Ancak sağlıklı dişler hâlâ etiketli olmadığı için model sınır vakalarda çekimser kalarak `Recall` kaybetti (`0.557 → 0.465`). Tek aşamalı tespit mimarisinin sınırına yaklaşıldığı görüldü.