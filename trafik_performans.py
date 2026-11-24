
import os
import xml.etree.ElementTree as ET

dosya_yolu = os.path.join(
    "simulation",
    "tripinfo.xml"
)

tree = ET.parse(dosya_yolu)
root = tree.getroot()

tamamlanan = []
tamamlanmayan = []

for trip in root.findall("tripinfo"):

    arrival = float(trip.get("arrival", "-1"))

    bilgiler = {
        "id": trip.get("id"),
        "duration": float(trip.get("duration", "0")),
        "waiting": float(trip.get("waitingTime", "0")),
        "time_loss": float(trip.get("timeLoss", "0"))
    }

    # -1: Arac henuz hedefine ulasmamis
    if arrival >= 0:
        tamamlanan.append(bilgiler)
    else:
        tamamlanmayan.append(bilgiler)


print("===== TRAFIK PERFORMANS RAPORU =====")

print("Toplam kayit:",
      len(tamamlanan) + len(tamamlanmayan))

print("Tamamlanan yolculuk:", len(tamamlanan))
print("Tamamlanmayan yolculuk:", len(tamamlanmayan))

if tamamlanan:

    ort_sure = sum(
        a["duration"] for a in tamamlanan
    ) / len(tamamlanan)

    ort_bekleme = sum(
        a["waiting"] for a in tamamlanan
    ) / len(tamamlanan)

    ort_kayip = sum(
        a["time_loss"] for a in tamamlanan
    ) / len(tamamlanan)

    print(f"Ortalama seyahat suresi: {ort_sure:.2f} sn")
    print(f"Ortalama bekleme suresi: {ort_bekleme:.2f} sn")
    print(f"Ortalama zaman kaybi: {ort_kayip:.2f} sn")

else:
    print("Tamamlanan yolculuk bulunamadi.")

print("===================================")
