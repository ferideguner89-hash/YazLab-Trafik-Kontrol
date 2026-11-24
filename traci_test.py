
import os
import traci
import sumolib

# SUMO ornek simülasyonunun dosya yolu
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


# SUMO programini bul
sumo_binary = sumolib.checkBinary("sumo")

# Simülasyonu baslat
traci.start([sumo_binary, "-c", config_path])

print("SUMO simülasyonu basladi!")

try:
    # Simülasyonu 100 adim ilerlet
    for step in range(100):
        traci.simulationStep()

        # Simülasyondaki arac sayisi
        vehicle_count = traci.vehicle.getIDCount()

        print(
            f"Adim {step + 1}: "
            f"{vehicle_count} arac var"
        )

finally:
    # SUMO baglantisini kapat
    traci.close()

print("Simülasyon tamamlandi!")
