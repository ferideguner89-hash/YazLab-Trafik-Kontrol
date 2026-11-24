
import traci
import sumolib

CONFIG = "simulation/antalya.sumocfg"

K3 = (
    "cluster_1354137368_14253375237_"
    "14269048484_2137707255_#2more"
)

sumo_binary = sumolib.checkBinary("sumo")

traci.start([sumo_binary, "-c", CONFIG])

try:
    # K3'un kontrol ettigi giris seritlerini bul
    seritler = set()

    links = traci.trafficlight.getControlledLinks(K3)

    for group in links:
        if not group:
            continue

        for connection in group:
            seritler.add(connection[0])

    print("K3 giris seridi sayisi:", len(seritler))

    # Simulasyonu 650. saniyeye ilerlet
    while traci.simulation.getTime() < 650:
        traci.simulationStep()

    print("\n===== K3 - 650. SANIYE =====")

    toplam_kuyruk = 0

    for serit in sorted(seritler):

        arac = traci.lane.getLastStepVehicleNumber(
            serit
        )

        kuyruk = traci.lane.getLastStepHaltingNumber(
            serit
        )

        if arac == 0:
            continue

        toplam_kuyruk += kuyruk

        print(
            f"Serit: {serit} | "
            f"Arac: {arac} | "
            f"Bekleyen: {kuyruk}"
        )

    print("\nToplam bekleyen:", toplam_kuyruk)

    print(
        "Aktif faz:",
        traci.trafficlight.getPhase(K3)
    )

    print(
        "Isik durumu:",
        traci.trafficlight.getRedYellowGreenState(K3)
    )

finally:
    traci.close()

print("\nAnaliz tamamlandi!")
