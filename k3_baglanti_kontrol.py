
from pathlib import Path
import traci
import sumolib

BASE_DIR = Path(__file__).resolve().parent
CONFIG = BASE_DIR / "simulation" / "antalya.sumocfg"

K3 = (
    "cluster_1354137368_14253375237_"
    "14269048484_2137707255_#2more"
)

GIRIS = "77488741#3_1"
CIKIS_YOLU = "120862425#2"

traci.start([
    sumolib.checkBinary("sumo"),
    "-c",
    str(CONFIG)
])

try:
    links = traci.trafficlight.getControlledLinks(K3)

    print("\n===== K3 HEDEF BAGLANTILAR =====")

    for indeks, group in enumerate(links):
        if not group:
            continue

        for connection in group:
            giris_seridi = connection[0]
            cikis_seridi = connection[1]

            if (
                giris_seridi == GIRIS
                and cikis_seridi.startswith(CIKIS_YOLU + "_")
            ):
                print("Sinyal indeksi:", indeks)
                print("Giris seridi:", giris_seridi)
                print("Cikis seridi:", cikis_seridi)
                print("-----------------------")

finally:
    traci.close()

print("\nKontrol tamamlandi!")
