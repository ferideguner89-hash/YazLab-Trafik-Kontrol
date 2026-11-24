
import sumolib

net = sumolib.net.readNet(
    "simulation/network/antalya.net.xml"
)

kavsaklar = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

def kavsaga_giren_yollar(kavsak_id):
    node = net.getNode(kavsak_id)
    return [
        edge for edge in node.getIncoming()
        if edge.allows("passenger")
    ]


def kavsaktan_cikan_yollar(kavsak_id):
    node = net.getNode(kavsak_id)
    return [
        edge for edge in node.getOutgoing()
        if edge.allows("passenger")
    ]


def rota_kontrol(baslangic, bitis):
    print(f"\n{baslangic} -> {bitis} kontrol ediliyor")

    giris_yollari = kavsaga_giren_yollar(
        kavsaklar[baslangic]
    )

    cikis_yollari = kavsaktan_cikan_yollar(
        kavsaklar[bitis]
    )

    en_iyi_rota = None
    en_kisa_mesafe = float("inf")

    for giris in giris_yollari:
        for cikis in cikis_yollari:

            rota, mesafe = net.getShortestPath(
                giris,
                cikis,
                vClass="passenger"
            )

            if rota and mesafe < en_kisa_mesafe:
                en_iyi_rota = rota
                en_kisa_mesafe = mesafe

    if en_iyi_rota:
        print("SONUC: Rota bulundu!")
        print(f"Rota uzunlugu: {en_kisa_mesafe:.1f} metre")
        print("Gecilen yollar:")

        for edge in en_iyi_rota:
            print(" -", edge.getID())
    else:
        print("SONUC: Uygun rota bulunamadi!")


rota_kontrol("K1", "K2")
rota_kontrol("K2", "K3")

print("\nRota kontrolu tamamlandi!")
