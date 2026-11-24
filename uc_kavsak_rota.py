
import sumolib

net = sumolib.net.readNet(
    "simulation/network/antalya.net.xml"
)

kavsaklar = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

k1 = net.getNode(kavsaklar["K1"])
k3 = net.getNode(kavsaklar["K3"])

# K1'e giren ve K3'ten cikan yollar
girisler = [
    edge for edge in k1.getIncoming()
    if edge.allows("passenger")
]

cikislar = [
    edge for edge in k3.getOutgoing()
    if edge.allows("passenger")
]

bulunan_rota = None

for giris in girisler:
    for cikis in cikislar:

        rota, mesafe = net.getShortestPath(
            giris, cikis, vClass="passenger"
        )

        if not rota:
            continue

        # Rotanin gectigi kavsak dugumleri
        dugumler = [rota[0].getFromNode().getID()]
        dugumler += [
            edge.getToNode().getID()
            for edge in rota
        ]

        # K1, K2 ve K3 sirasiyla geciliyor mu?
        hedefler = [
            kavsaklar["K1"],
            kavsaklar["K2"],
            kavsaklar["K3"]
        ]

        sonraki = 0

        for dugum in dugumler:
            if dugum == hedefler[sonraki]:
                sonraki += 1

                if sonraki == 3:
                    bulunan_rota = (rota, mesafe)
                    break

        if bulunan_rota:
            break

    if bulunan_rota:
        break

if bulunan_rota:
    rota, mesafe = bulunan_rota

    print("BASARILI!")
    print("K1 -> K2 -> K3 rotasi bulundu.")
    print(f"Mesafe: {mesafe:.1f} metre")

    print("\nRota yollari:")
    for edge in rota:
        print(edge.getID())

else:
    print("K1 -> K2 -> K3 sirasinda")
    print("uygun en kisa rota bulunamadi.")
    print("Farkli guzergahlar incelenebilir.")
