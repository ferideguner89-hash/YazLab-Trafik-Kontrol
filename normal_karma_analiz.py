
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent

DOSYA = (
    BASE
    / "simulation"
    / "results"
    / "normal_karma_tripinfo.xml"
)

if not DOSYA.is_file():
    raise FileNotFoundError(
        f"Sonuc dosyasi bulunamadi: {DOSYA}"
    )

agac = ET.parse(DOSYA)
araclar = list(agac.getroot().iter("tripinfo"))

tamamlanan = [
    arac for arac in araclar
    if float(arac.get("arrival", "-1")) >= 0
]

tamamlanmayan = len(araclar) - len(tamamlanan)

print("\n===== NORMAL TRAFIK ANALIZI =====")
print("Kaydedilen toplam arac:", len(araclar))
print("Tamamlanan arac:", len(tamamlanan))
print("Tamamlanmayan arac:", tamamlanmayan)

if tamamlanan:
    ort_bekleme = sum(
        float(a.get("waitingTime", "0"))
        for a in tamamlanan
    ) / len(tamamlanan)

    ort_yolculuk = sum(
        float(a.get("duration", "0"))
        for a in tamamlanan
    ) / len(tamamlanan)

    ort_zaman_kaybi = sum(
        float(a.get("timeLoss", "0"))
        for a in tamamlanan
    ) / len(tamamlanan)

    print("Ortalama bekleme:", round(ort_bekleme, 2), "sn")
    print("Ortalama yolculuk:", round(ort_yolculuk, 2), "sn")
    print("Ortalama zaman kaybi:", round(ort_zaman_kaybi, 2), "sn")

print("\nAnaliz tamamlandi!")
