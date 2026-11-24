
from pathlib import Path
import xml.etree.ElementTree as ET
import traci
import sumolib

BASE = Path(__file__).resolve().parent
CONFIG = BASE / "simulation" / "antalya.sumocfg"
RESULTS = BASE / "simulation" / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

K3 = (
    "cluster_1354137368_14253375237_"
    "14269048484_2137707255_#2more"
)

YOGUN_SERIT = "77488741#3_1"


def deney(ad, yesil_uzat=False):
    cikti = RESULTS / f"{ad}_tripinfo.xml"

    traci.start([
        sumolib.checkBinary("sumo"),
        "-c", str(CONFIG),
        "--seed", "42",
        "--tripinfo-output", str(cikti),
        "--no-step-log", "true"
    ])

    max_kuyruk = 0
    kuyruk_650 = None
    tamamlanan = 0
    onceki_faz = None

    try:
        while traci.simulation.getTime() < 1200:
            traci.simulationStep()

            faz = traci.trafficlight.getPhase(K3)

            # Mevcut faz sırasını değiştirmiyoruz.
            # Yalnızca faz 2'ye girildiğinde süreyi uzatıyoruz.
            if yesil_uzat and faz == 2 and onceki_faz != 2:
                traci.trafficlight.setPhaseDuration(K3, 17)

            onceki_faz = faz

            kuyruk = traci.lane.getLastStepHaltingNumber(
                YOGUN_SERIT
            )

            max_kuyruk = max(max_kuyruk, kuyruk)

            if traci.simulation.getTime() == 650:
                kuyruk_650 = kuyruk

            tamamlanan += traci.simulation.getArrivedNumber()

    finally:
        traci.close()

    agac = ET.parse(cikti)
    yolculuklar = [
        t for t in agac.getroot().iter("tripinfo")
        if float(t.get("arrival", "-1")) >= 0
    ]

    if yolculuklar:
        ort_bekleme = sum(
            float(t.get("waitingTime", "0"))
            for t in yolculuklar
        ) / len(yolculuklar)
    else:
        ort_bekleme = 0

    print(f"\n===== {ad.upper()} =====")
    print("Tamamlanan arac:", tamamlanan)
    print("K3 maksimum kuyruk:", max_kuyruk)
    print("650. saniyedeki kuyruk:", kuyruk_650)
    print("Ortalama bekleme:", round(ort_bekleme, 2), "sn")


if not CONFIG.is_file():
    raise FileNotFoundError(f"Dosya bulunamadi: {CONFIG}")

deney("sabit", yesil_uzat=False)
deney("uzatilmis_yesil", yesil_uzat=True)

print("\nKarsilastirma tamamlandi!")
