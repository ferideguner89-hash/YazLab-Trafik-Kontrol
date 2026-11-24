
from pathlib import Path
import traci
import sumolib

BASE_DIR = Path(__file__).resolve().parent
CONFIG = BASE_DIR / "simulation" / "antalya.sumocfg"

K3 = (
    "cluster_1354137368_14253375237_"
    "14269048484_2137707255_#2more"
)

YOGUN_SERIT = "77488741#3_1"

if not CONFIG.is_file():
    raise FileNotFoundError(f"Dosya bulunamadi: {CONFIG}")

traci.start([
    sumolib.checkBinary("sumo"),
    "-c",
    str(CONFIG)
])

try:
    while traci.simulation.getTime() < 650:
        traci.simulationStep()

    araclar = traci.lane.getLastStepVehicleIDs(YOGUN_SERIT)

    print("\n===== K3 ARAC YONLERI =====")
    print("Serit:", YOGUN_SERIT)
    print("Arac sayisi:", len(araclar))

    for arac_id in araclar[:5]:
        rota = traci.vehicle.getRoute(arac_id)
        rota_indeksi = traci.vehicle.getRouteIndex(arac_id)

        print("\nArac:", arac_id)
        print("Mevcut yol:", traci.vehicle.getRoadID(arac_id))
        print("Rota indeksi:", rota_indeksi)

        if rota_indeksi + 1 < len(rota):
            print("Sonraki yol:", rota[rota_indeksi + 1])
        else:
            print("Sonraki yol: Rota sonu")

finally:
    traci.close()

print("\nKontrol tamamlandi!")
