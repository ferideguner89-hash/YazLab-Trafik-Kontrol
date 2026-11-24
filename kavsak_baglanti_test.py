
import sumolib

# Gercek yol agimiz
network_path = "simulation/network/antalya.net.xml"

net = sumolib.net.readNet(network_path)

# Sectigimiz 3 trafik isigi kontroloru
kavsaklar = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

traffic_lights = {
    tls.getID(): tls
    for tls in net.getTrafficLights()
}

# Her kontrolorun yonettigi kavsak dugumlerini bul
def get_controlled_nodes(tls):
    nodes = {}

    for connection in tls.getConnections():
        from_lane = connection[0]
        node = from_lane.getEdge().getToNode()
        nodes[node.getID()] = node

    return list(nodes.values())


for name, tls_id in kavsaklar.items():

    tls = traffic_lights.get(tls_id)

    print(f"\n{name} KONTROLU")

    if tls is None:
        print("Kontrolor bulunamadi!")
        continue

    nodes = get_controlled_nodes(tls)

    print("Kontrolor ID:", tls_id)
    print("Kontrol edilen dugum sayisi:", len(nodes))

    for node in nodes:
        print("Kavsak dugumu:", node.getID())

print("\nKontrol tamamlandi!")
