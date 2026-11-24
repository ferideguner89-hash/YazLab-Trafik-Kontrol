
from pathlib import Path
import xml.etree.ElementTree as ET

import traci
import sumolib

BASE = Path(__file__).resolve().parent

CONFIG = BASE / "simulation" / "normal_karma.sumocfg"
OUTPUT = BASE / "simulation" / "results" / "aksama_tripinfo.xml"

SERIT = "77488741#3_1"

if not CONFIG.is_file():
    raise FileNotFoundError(f"Dosya bulunamadi: {CONFIG}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

traci.start([
    sumolib.checkBinary("sumo"),
    "-c", str(CONFIG),
    "--seed", "42",
    "--tripinfo-output", str(OUTPUT),
    "--no-step-log", "true"
])

try:
    eski_hiz = traci.lane.getMaxSpeed(SERIT)

    toplam_cikan = 0
    toplam_varan = 0

    while traci.simulation.getTime() < 1200:
        traci.simulationStep()

        zaman = int(traci.simulation.getTime())

        if zaman == 200:
            traci.lane.setMaxSpeed(SERIT, 3.0)
            print("200. saniye: Yol calismasi basladi.")

        if zaman == 800:
            traci.lane.setMaxSpeed(SERIT, eski_hiz)
            print("800. saniye: Yol calismasi bitti.")

        toplam_cikan += traci.simulation.getDepartedNumber()
        toplam_varan += traci.simulation.getArrivedNumber()

    aktif = traci.vehicle.getIDCount()

finally:
    traci.close()

araclar = list(
    ET.parse(OUTPUT).getroot().iter("tripinfo")
)

tamamlanan = [
    a for a in araclar
    if float(a.get("arrival", "-1")) >= 0
]

print("\n===== AKSAMA SENARYOSU =====")
print("Yola cikan arac:", toplam_cikan)
print("Tamamlanan arac:", toplam_varan)
print("Sonda hala yolda olan:", aktif)

if tamamlanan:
    ort_bekleme = sum(
        float(a.get("waitingTime", "0"))
        for a in tamamlanan
    ) / len(tamamlanan)

    print("Ortalama bekleme:", round(ort_bekleme, 2), "sn")

print("\nAksama senaryosu tamamlandi!")
