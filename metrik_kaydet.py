
import csv
import os
import traci
import sumolib

CONFIG = "simulation/antalya.sumocfg"

KAVSAKLAR = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

os.makedirs("simulation/results", exist_ok=True)

output_path = "simulation/results/traffic_metrics.csv"

sumo_binary = sumolib.checkBinary("sumo")

traci.start([sumo_binary, "-c", CONFIG])

try:
    kavsak_seritleri = {}

    for ad, tls_id in KAVSAKLAR.items():
        seritler = set()

        for group in traci.trafficlight.getControlledLinks(tls_id):
            if not group:
                continue

            for connection in group:
                seritler.add(connection[0])

        kavsak_seritleri[ad] = sorted(seritler)

    with open(output_path, "w", newline="", encoding="utf-8") as dosya:

        writer = csv.writer(dosya)

        writer.writerow([
            "timestamp",
            "intersection_id",
            "vehicle_count",
            "queue_length",
            "average_speed",
            "average_waiting_time",
            "signal_phase"
        ])

        while traci.simulation.getTime() < 1200:

            traci.simulationStep()
            zaman = traci.simulation.getTime()

            if int(zaman) % 10 != 0:
                continue

            for ad, seritler in kavsak_seritleri.items():

                araclar = set()
                kuyruk = 0

                for serit in seritler:
                    araclar.update(
                        traci.lane.getLastStepVehicleIDs(serit)
                    )

                    kuyruk += (
                        traci.lane.getLastStepHaltingNumber(serit)
                    )

                arac_sayisi = len(araclar)

                if arac_sayisi > 0:
                    ort_hiz = sum(
                        traci.vehicle.getSpeed(a)
                        for a in araclar
                    ) / arac_sayisi

                    ort_bekleme = sum(
                        traci.vehicle.getWaitingTime(a)
                        for a in araclar
                    ) / arac_sayisi
                else:
                    ort_hiz = 0
                    ort_bekleme = 0

                faz = traci.trafficlight.getPhase(
                    KAVSAKLAR[ad]
                )

                writer.writerow([
                    zaman,
                    ad,
                    arac_sayisi,
                    kuyruk,
                    round(ort_hiz, 2),
                    round(ort_bekleme, 2),
                    faz
                ])

finally:
    traci.close()

print("Metrikler kaydedildi!")
print("Dosya:", output_path)
