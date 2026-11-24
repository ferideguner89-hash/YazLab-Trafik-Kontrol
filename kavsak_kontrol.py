
import os
import sumolib

# Olusturdugumuz gercek SUMO yol agi
network_path = os.path.join(
    "simulation",
    "network",
    "antalya.net.xml"
)

# Yol agini oku
network = sumolib.net.readNet(
    network_path,
    withPrograms=True
)

# Trafik isigi kontrolorlerini bul
traffic_lights = network.getTrafficLights()

print("Gercek Antalya yol agi analizi")
print("-------------------------------")

print(f"Trafik isigi kontroloru sayisi: {len(traffic_lights)}")

for light in traffic_lights:
    print(f"Trafik isigi ID: {light.getID()}")

print("-------------------------------")
print("Kontrol tamamlandi!")
