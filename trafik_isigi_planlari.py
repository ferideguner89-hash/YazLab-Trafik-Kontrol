
import sumolib

network_path = "simulation/network/antalya.net.xml"

net = sumolib.net.readNet(
    network_path,
    withPrograms=True
)

kavsaklar = {
    "K1": "cluster_10230587551_10230587557_10230587562_10230587564_#11more",
    "K2": "1061515522",
    "K3": "cluster_1354137368_14253375237_14269048484_2137707255_#2more"
}

tls_dict = {
    tls.getID(): tls
    for tls in net.getTrafficLights()
}

for name, tls_id in kavsaklar.items():

    print(f"\n===== {name} TRAFIK ISIGI =====")

    tls = tls_dict.get(tls_id)

    if tls is None:
        print("Kontrolor bulunamadi!")
        continue

    print("Kontrolor:", tls_id)

    programs = tls.getPrograms()

    if not programs:
        print("Sinyal plani bulunamadi!")
        continue

    for program_id, program in programs.items():

        print("Program ID:", program_id)

        phases = program.getPhases()

        for i, phase in enumerate(phases):

            print(
                f"Faz {i}: "
                f"Sure = {phase.duration} sn | "
                f"Durum = {phase.state}"
            )

print("\nKontrol tamamlandi!")
