
from pathlib import Path
import traci
import sumolib

# Python dosyasinin bulundugu proje klasoru
BASE_DIR = Path(__file__).resolve().parent

CONFIG = BASE_DIR / "simulation" / "antalya.sumocfg"

K3 = (
    "cluster_1354137368_14253375237_"
    "14269048484_2137707255_#2more"
)

YOGUN_SERIT = "77488741#3_1"

# Dosyalarin varligini kontrol et
if not CONFIG.is_file():
    raise FileNotFoundError(
        f"SUMO konfigurasyon dosyasi bulunamadi: {CONFIG}"
    )

sumo_binary = sumolib.checkBinary("sumo")

traci.start([
    sumo_binary,
    "-c",
    str(CONFIG)
])

try:
    links = traci.trafficlight.getControlledLinks(K3)

    print("\n===== K3 SINYAL BAGLANTILARI =====")

    sinyal_indeksleri = set()

    for indeks, group in enumerate(links):
        if not group:
            continue

        for connection in group:
            giris_seridi = connection[0]
            cikis_seridi = connection[1]

            if giris_seridi == YOGUN_SERIT:
                sinyal_indeksleri.add(indeks)

                print("Sinyal indeksi:", indeks)
                print("Giris seridi:", giris_seridi)
                print("Cikis seridi:", cikis_seridi)
                print("----------------------")

    print("\n===== K3 SINYAL FAZLARI =====")

    programlar = traci.trafficlight.getAllProgramLogics(K3)

    for program in programlar:
        print("Program ID:", program.programID)

        for faz_no, faz in enumerate(program.phases):
            renkler = []

            for indeks in sorted(sinyal_indeksleri):
                renkler.append(
                    f"{indeks}: {faz.state[indeks]}"
                )

            print(
                f"Faz {faz_no} | "
                f"Sure: {faz.duration} sn | "
                f"Sinyaller: {', '.join(renkler)}"
            )

    if not sinyal_indeksleri:
        print("UYARI: Yogun serit icin sinyal bulunamadi.")

finally:
    traci.close()

print("\nAnaliz tamamlandi!")
