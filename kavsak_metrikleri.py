
import traci
import sumolib

CONFIG = "simulation/antalya.sumocfg"

KAVSAKLAR = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

sumo_binary = sumolib.checkBinary("sumo")

traci.start([sumo_binary, "-c", CONFIG])

try:
    kavsak_seritleri = {}

    for ad, tls_id in KAVSAKLAR.items():

        links = traci.trafficlight.getControlledLinks(tls_id)

        seritler = set()

        for group in links:
            if not group:
                continue

            for connection in group:
                seritler.add(connection[0])

        kavsak_seritleri[ad] = sorted(seritler)

    while traci.simulation.getTime() < 1200:

        traci.simulationStep()

        zaman = traci.simulation.getTime()

        if int(zaman) % 100 != 0:
            continue

        print(f"\n===== ZAMAN: {zaman:.0f} sn =====")

        for ad, seritler in kavsak_seritleri.items():

            arac_idleri = set()

            kuyruk = 0

            for serit in seritler:
                arac_idleri.update(
                    traci.lane.getLastStepVehicleIDs(serit)
                )

                kuyruk += (
                    traci.lane.getLastStepHaltingNumber(serit)
                )

            arac_sayisi = len(arac_idleri)

            if arac_sayisi > 0:

                ort_hiz = sum(
                    traci.vehicle.getSpeed(arac)
                    for arac in arac_idleri
                ) / arac_sayisi

                ort_bekleme = sum(
                    traci.vehicle.getWaitingTime(arac)
                    for arac in arac_idleri
                ) / arac_sayisi

            else:
                ort_hiz = 0
                ort_bekleme = 0

            faz = traci.trafficlight.getPhase(
                KAVSAKLAR[ad]
            )

            print(
                f"{ad} | "
                f"Arac: {arac_sayisi} | "
                f"Kuyruk: {kuyruk} | "
                f"Hiz: {ort_hiz:.2f} m/s | "
                f"Bekleme: {ort_bekleme:.2f} sn | "
                f"Faz: {faz}"
            )

finally:
    traci.close()

print("\nKavsak metrikleri tamamlandi!")
