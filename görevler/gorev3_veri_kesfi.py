import numpy as np
import json
import cv2
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from pathlib import Path

# 1. Dosya yollarını tanımla
disease_dir = Path(__file__).resolve().parents[1] / "training_data" / "quadrant-enumeration-disease"
json_path = disease_dir / "train_quadrant_enumeration_disease.json"
xrays_dir = disease_dir / "xrays"

with open(json_path, "r") as f:
    data = json.load(f)

# 2. Kategori sözlüklerini oluştur
cat1_map = {c["id"]: c["name"] for c in data["categories_1"]} # Kadranlar (1-4)
cat2_map = {c["id"]: c["name"] for c in data["categories_2"]} # Diş sırası (1-8)
cat3_map = {c["id"]: c["name"] for c in data["categories_3"]} # Hastalıklar (4 sınıf)

print("=== KATEGORİ TANIMLARI ===")
print("Kadranlar (cat_1):", cat1_map)
print("Diş Sırası (cat_2):", cat2_map)
print("Hastalıklar (cat_3):", cat3_map)

# 3. Görüntü ve etiket istatistikleri
all_images = {img["id"]: img for img in data["images"]}
anns_by_img = defaultdict(list)
for ann in data["annotations"]:
    anns_by_img[ann["image_id"]].append(ann)

images_with_disease = len(anns_by_img)
images_without_disease = len(all_images) - images_with_disease

print("\n=== GÖRÜNTÜ DAĞILIMI ===")
print(f"JSON'daki toplam röntgen sayısı: {len(all_images)}")
print(f"En az 1 anomalisi olan röntgen:  {images_with_disease}")
print(f"Hiç anomalisi olmayan röntgen:   {images_without_disease}")
print(f"Toplam anomali kutusu sayısı:    {len(data['annotations'])}")

# 4. Hastalık türlerine göre dağılım (Sınıf dengesizliği var mı?)
disease_counts = Counter(cat3_map[ann["category_id_3"]] for ann in data["annotations"])
print("\n=== HASTALIK TÜRLERİNE GÖRE KUTU SAYISI ===")
for name, count in disease_counts.most_common():
    oran = (count / len(data["annotations"])) * 100
    print(f"  - {name:<20}: {count:>4} adet (%{oran:.1f})")

# 5. Aynı diş kutusunda birden fazla hastalık var mı kontrolü
bbox_counter = Counter((ann["image_id"], tuple(ann["bbox"])) for ann in data["annotations"])
multi_label_teeth = sum(1 for c in bbox_counter.values() if c > 1)
print(f"\nAynı dişte birden fazla anomali etiketi olan durum sayısı: {multi_label_teeth}")

# 6. Örnek 2 Röntgeni Etiketleriyle Çizdir
sample_img_ids = list(anns_by_img.keys())[:2]
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

colors = {
    "Caries": (0, 255, 255),             # Sarı
    "Deep Caries": (0, 140, 255),        # Turuncu
    "Periapical Lesion": (0, 0, 255),    # Kırmızı
    "Impacted": (255, 0, 255)            # Mor
}

for idx, img_id in enumerate(sample_img_ids):
    img_info = all_images[img_id]
    img_path = xrays_dir / img_info["file_name"]
    img_bytes = np.fromfile(str(xrays_dir / img_info["file_name"]), dtype=np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    for ann in anns_by_img[img_id]:
        x, y, w, h = map(int, ann["bbox"])
        q = cat1_map[ann["category_id_1"]]
        t = cat2_map[ann["category_id_2"]]
        d = cat3_map[ann["category_id_3"]]
        color = colors.get(d, (0, 255, 0))

        cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
        label = f"FDI:{q}{t} | {d}"
        cv2.putText(img, label, (x, max(y - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

    axes[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[idx].set_title(f"Dosya: {img_info['file_name']} (Toplam {len(anns_by_img[img_id])} anomali)")
    axes[idx].axis("off")

plt.tight_layout()
plt.show()