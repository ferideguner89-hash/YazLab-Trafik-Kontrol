
import os
import traci
import sumolib

# SUMO dosyasinin konumu
sumo_home = os.environ["SUMO_HOME"]

config_path = os.path.join(
    sumo_home,
    "docs",
    "examples",
    "sumo",
    "simple_nets",
    "cross",
    "cross1ltl",
    "test.sumocfg"
)

sumo_binary = sumolib.checkBinary("sumo")

# Simülasyonu baslat
traci.start([sumo_binary, "-c", config_path])

print("Trafik veri analizi basladi!")

try:
    for step in range(100):

        traci.simulationStep()

        # Tum araclarin ID listesi
        vehicle_ids = traci.vehicle.getIDList()

        # Toplam arac sayisi
        vehicle_count = len(vehicle_ids)

        # Arac hizlarini ve bekleme surelerini topla
        total_speed = 0
        total_waiting = 0

        for vehicle_id in vehicle_ids:
            total_speed += traci.vehicle.getSpeed(vehicle_id)
            total_waiting += traci.vehicle.getWaitingTime(
                vehicle_id
            )

        if vehicle_count > 0:
            average_speed = total_speed / vehicle_count
            average_waiting = total_waiting / vehicle_count
        else:
            average_speed = 0
            average_waiting = 0

        # Trafik isiklarini bul
        traffic_lights = traci.trafficlight.getIDList()

        # Her 10 adimda bir bilgileri yazdir
        if (step + 1) % 10 == 0:

            print("\n------------------------")
            print(f"Simülasyon adimi: {step + 1}")
            print(f"Arac sayisi: {vehicle_count}")
            print(f"Ortalama hiz: {average_speed:.2f} m/s")
            print(
                f"Ortalama bekleme: "
                f"{average_waiting:.2f} saniye"
            )

            for light_id in traffic_lights:
                state = traci.trafficlight.getRedYellowGreenState(
                    light_id
                )
                print(
                    f"Trafik isigi {light_id}: {state}"
                )

finally:
    traci.close()

print("\nTrafik veri analizi tamamlandi!")
