
from pathlib import Path
import traci
import sumolib

BASE = Path(__file__).resolve().parent

NET = BASE / "simulation/network/antalya.net.xml"

ROUTES = ",".join([
    str(BASE / "simulation/routes/normal.rou.xml"),
    str(BASE / "simulation/routes/coklu_deneme.rou.xml")
])


KAVSAKLAR = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

traci.start([
    sumolib.checkBinary("sumo"),
    "-n", str(NET),
    "-r", str(ROUTES),
    "--end", "1200",
    "--no-step-log", "true"
])

try:
    kavsak_seritleri = {}
    gorulen_araclar = {}

    for ad, tls_id in KAVSAKLAR.items():
        kavsak_seritleri[ad] = set(
            traci.trafficlight.getControlledLanes(tls_id)
        )
        gorulen_araclar[ad] = set()

    toplam_arac = 0

    while (
        traci.simulation.getMinExpectedNumber() > 0
        and traci.simulation.getTime() < 1200
    ):
        traci.simulationStep()

        toplam_arac += traci.simulation.getDepartedNumber()

        for ad, seritler in kavsak_seritleri.items():
            for serit in seritler:
                gorulen_araclar[ad].update(
                    traci.lane.getLastStepVehicleIDs(serit)
                )

    print("\n===== UC KAVSAK TRAFIK KONTROLU =====")
    print("Toplam yola cikan arac:", toplam_arac)

    for ad, araclar in gorulen_araclar.items():
        print(
            f"{ad} kavsagina yaklasan "
            f"farkli arac sayisi: {len(araclar)}"
        )

    ortak = set.intersection(*gorulen_araclar.values())

    print(
        "Uc kavsagin da giris seritlerinde "
        "gorulen arac sayisi:", len(ortak)
    )

finally:
    traci.close()

print("\nKontrol tamamlandi!")
