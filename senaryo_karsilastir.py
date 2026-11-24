
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
SONUCLAR = BASE / "simulation" / "results"

dosyalar = {
    "NORMAL TRAFIK": "normal_karma_tripinfo.xml",
    "YOGUN TRAFIK": "yogun_karma_tripinfo.xml"
}

for senaryo, dosya_adi in dosyalar.items():

    dosya = SONUCLAR / dosya_adi

    if not dosya.is_file():
        print("Dosya bulunamadi:", dosya)
        continue

    agac = ET.parse(dosya)
    araclar = list(agac.getroot().iter("tripinfo"))

    tamamlanan = [
        a for a in araclar
        if float(a.get("arrival", "-1")) >= 0
    ]

    tamamlanmayan = len(araclar) - len(tamamlanan)

    print(f"\n===== {senaryo} =====")
    print("Kaydedilen arac:", len(araclar))
    print("Tamamlanan arac:", len(tamamlanan))
    print("Tamamlanmayan arac:", tamamlanmayan)

    if tamamlanan:
        for baslik, alan in [
            ("Ortalama bekleme", "waitingTime"),
            ("Ortalama yolculuk", "duration"),
            ("Ortalama zaman kaybi", "timeLoss")
        ]:
            ortalama = sum(
                float(a.get(alan, "0"))
                for a in tamamlanan
            ) / len(tamamlanan)

            print(f"{baslik}: {ortalama:.2f} sn")

print("\nKarsilastirma tamamlandi!")

