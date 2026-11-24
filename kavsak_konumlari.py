
import sumolib

network_path = "simulation/network/antalya.net.xml"

net = sumolib.net.readNet(network_path)

print("TRAFIK ISIKLARININ KONUMLARI")
print("----------------------------")

for tls in net.getTrafficLights():

    tls_id = tls.getID()

    # Kontrol edilen baglantilardan kavsak dugumlerini bul
    nodes = []

    for connection in tls.getConnections():
        from_lane = connection[0]
        to_lane = connection[1]

        node = from_lane.getEdge().getToNode()
        nodes.append(node)

    # Tekrarlanan dugumleri kaldir
    unique_nodes = {node.getID(): node for node in nodes}

    for node in unique_nodes.values():
        x, y = node.getCoord()

        lon, lat = net.convertXY2LonLat(x, y)

        print(
            f"Kontrolor: {tls_id} | "
            f"Kavsak: {node.getID()} | "
            f"Enlem: {lat:.6f} | "
            f"Boylam: {lon:.6f}"
        )

print("----------------------------")
print("Konum kontrolu tamamlandi!")
