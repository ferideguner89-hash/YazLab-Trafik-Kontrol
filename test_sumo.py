
import os
import traci
import sumolib

print("Python ve SUMO kutuphaneleri hazir!")

sumo_home = os.environ.get("SUMO_HOME")
print("SUMO_HOME:", sumo_home)

sumo_binary = sumolib.checkBinary("sumo")
print("SUMO programi:", sumo_binary)
