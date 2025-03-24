from collections import defaultdict, deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Dict, List, Tuple, Optional
import pyttsx3  # Metni sese dönüştürmek için kullandım.
import time  # Seslendirme araları için kullandım.


class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def __lt__(self, other: 'Istasyon'):
        return self.idx < other.idx


class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Konuşma hızını ayarladım.
        self.engine.setProperty('volume', 0.9)  # Ses seviyesini ayarladım.

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if not idx or not ad or not hat:
            raise ValueError("İstasyon ID, ad ve hat bilgileri zorunludur.")
        if idx in self.istasyonlar:
            raise ValueError(f"{idx} ID'li istasyon zaten mevcut.")
        istasyon = Istasyon(idx, ad, hat)
        self.istasyonlar[idx] = istasyon
        self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            raise ValueError("Geçersiz istasyon ID'si.")
        if not isinstance(sure, int) or sure <= 0:
            raise ValueError("Bağlantı süresi pozitif olmalıdır.")
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        kuyruk = deque([(self.istasyonlar[baslangic_id], [self.istasyonlar[baslangic_id]])])
        ziyaret_edilen = set()

        while kuyruk:
            mevcut, yol = kuyruk.popleft()
            if mevcut.idx == hedef_id:
                return yol

            if mevcut.idx not in ziyaret_edilen:
                ziyaret_edilen.add(mevcut.idx)
                for komsu, _ in mevcut.komsular:
                    kuyruk.append((komsu, yol + [komsu]))

        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        pq = [(0, self.istasyonlar[baslangic_id], [self.istasyonlar[baslangic_id]])]
        ziyaret_edilen = set()

        while pq:
            toplam_sure, mevcut, yol = heapq.heappop(pq)
            if mevcut.idx == hedef_id:
                return yol, toplam_sure

            if mevcut.idx not in ziyaret_edilen:
                ziyaret_edilen.add(mevcut.idx)
                for komsu, sure in mevcut.komsular:
                    heapq.heappush(pq, (toplam_sure + sure, komsu, yol + [komsu]))

        return None

    def metro_agini_ciz(self):
        G = nx.Graph()

        renkler = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Yeşil Hat": "green",
            "Turuncu Hat": "orange",
            "Mor Hat": "purple",
            "Sarı Hat": "yellow",
            "Pembe Hat": "pink",
            "Gri Hat": "grey",
            "Turkuaz Hat": "turquoise"
        }

        for istasyon in self.istasyonlar.values():
            G.add_node(istasyon.ad, color=renkler.get(istasyon.hat, "black"))
            for komsu, _ in istasyon.komsular:
                G.add_edge(istasyon.ad, komsu.ad, color=renkler.get(istasyon.hat, "black"))

        pos = nx.kamada_kawai_layout(G)
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        node_colors = [G.nodes[n]['color'] for n in G.nodes()]

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors,
                edge_color=edge_colors, font_size=10, font_weight="bold")
        plt.title("Hatay Metro Ağı")
        plt.show()

    def animasyonlu_rota_goster(self, rota: List[Istasyon]):
        G = nx.Graph()
        renkler = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Yeşil Hat": "green",
            "Turuncu Hat": "orange",
            "Mor Hat": "purple",
            "Sarı Hat": "yellow",
            "Pembe Hat": "pink",
            "Gri Hat": "grey",
            "Turkuaz Hat": "turquoise"
        }

        # Grafiği oluştur
        for istasyon in self.istasyonlar.values():
            G.add_node(istasyon.ad, color=renkler.get(istasyon.hat, "black"))
            for komsu, _ in istasyon.komsular:
                G.add_edge(istasyon.ad, komsu.ad, color=renkler.get(istasyon.hat, "black"))

        pos = nx.kamada_kawai_layout(G)
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        node_colors = [G.nodes[n]['color'] for n in G.nodes()]

        fig, ax = plt.subplots(figsize=(12, 8))
        plt.title("Metro Rotası: Tren Animasyonu")

        # Rota kenarlarını belirlendi.
        rota_kenarlari = []
        for i in range(len(rota) - 1):
            rota_kenarlari.append((rota[i].ad, rota[i + 1].ad))

        # Başlangıçta tüm grafiği çizdirdim.
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors,
                edge_color=edge_colors, font_size=10, font_weight="bold", ax=ax)

        # Tren görseli için hazırlık (sonradan kullanmadım)
        tren, = ax.plot([], [], 'o', markersize=20, color='black')
        tren_arka, = ax.plot([], [], 'o', markersize=24, color='white', alpha=0.7)
        tren_arka2, = ax.plot([], [], 'o', markersize=28, color='white', alpha=0.4)

        # Sesli anons için fonksiyon oluşturdum.
        def sesli_anons(istasyon_ad: str, sira: int, toplam: int):
            metin = f"{sira}. istasyon: {istasyon_ad}"
            print(metin)  # Konsola da yazdıralım
            self.engine.say(metin)
            self.engine.runAndWait()
            time.sleep(0.5)  # Anonslar arası bekleme

        # İlk istasyonu seslendirdim.
        sesli_anons(rota[0].ad, 1, len(rota))

        # Animasyon güncelleme fonksiyonu
        def update(frame):
            ax.clear()

            # Tüm grafiği çizdirdim.
            nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors,
                    edge_color=edge_colors, font_size=10, font_weight="bold", ax=ax)

            # Rota kenarlarını vurgulandı.
            nx.draw_networkx_edges(G, pos, edgelist=rota_kenarlari[:frame + 1],
                                   edge_color='black', width=3, ax=ax)

            # Mevcut istasyonu vurgulandı.
            if frame < len(rota):
                current_pos = pos[rota[frame].ad]
                tren.set_data([current_pos[0]], [current_pos[1]])
                tren_arka.set_data([current_pos[0]], [current_pos[1]])
                tren_arka2.set_data([current_pos[0]], [current_pos[1]])

                # İstasyon adını gösterildi.
                ax.text(current_pos[0], current_pos[1] + 0.05, rota[frame].ad,
                        fontsize=12, ha='center', color='black', weight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

                # Yeni istasyona gelindiğinde sesli anons yapıldı.
                if frame > 0:
                    sesli_anons(rota[frame].ad, frame + 1, len(rota))

            # Başlık güncellendi.
            ax.set_title(f"Metro Rotası: {rota[0].ad} → {rota[-1].ad}\n"
                         f"Adım: {frame + 1}/{len(rota)} - İstasyon: {rota[frame].ad}")

        # Animasyonu oluşturdum.
        ani = animation.FuncAnimation(fig, update, frames=len(rota),
                                      interval=1000, repeat=False)
        plt.tight_layout()
        plt.show()

        # Rota tamamlandığında son anons yapıldı.
        self.engine.say(f"Rota tamamlandı. Toplam {len(rota)} istasyon geçildi.")
        self.engine.runAndWait()


if __name__ == "__main__":
    metro = MetroAgi()

    # İstasyonları ekledim.
    istasyonlar = [
        ("KR1", "Antakya", "Kırmızı Hat"),
        ("KR2", "Defne", "Kırmızı Hat"),
        ("KR3", "Samandağ", "Kırmızı Hat"),
        ("KR4", "Yayladağı", "Kırmızı Hat"),
        ("KR5", "Arsuz", "Kırmızı Hat"),
        ("M1", "Antakya", "Mavi Hat"),
        ("M2", "Kırıkhan", "Mavi Hat"),
        ("M3", "Hassa", "Mavi Hat"),
        ("M4", "Osmaniye", "Mavi Hat"),
        ("M5", "Reyhanlı", "Mavi Hat"),
        ("Y1", "İskenderun", "Sarı Hat"),
        ("Y2", "Payas", "Sarı Hat"),
        ("Y3", "Erzin", "Sarı Hat"),
        ("Y4", "Ceyhan", "Sarı Hat"),
        ("P1", "Dörtyol", "Pembe Hat"),
        ("P2", "Hacıpaşa", "Pembe Hat"),
        ("P3", "Toprakkale", "Pembe Hat"),
        ("GR1", "Belen", "Gri Hat"),
        ("GR2", "Kumlu", "Gri Hat"),
        ("GR3", "Payas", "Gri Hat"),
        ("GR4", "Yakacık", "Gri Hat"),
        ("TR1", "Altınözü", "Turkuaz Hat"),
        ("TR2", "Yayladağı", "Turkuaz Hat"),
        ("TR3", "Narlıca", "Turkuaz Hat"),
        ("TR4", "Şenköy", "Turkuaz Hat"),
        ("TR5", "Büyükdalyan", "Turkuaz Hat"),
        ("TR6", "Harbiye", "Turkuaz Hat")
    ]

    for idx, ad, hat in istasyonlar:
        metro.istasyon_ekle(idx, ad, hat)

    # Bağlantıları oluşturdum.
    baglantilar = [
        ("KR1", "KR2", 5), ("KR2", "KR3", 10), ("KR3", "KR4", 10), ("KR4", "KR5", 15),
        ("M1", "M2", 8), ("M2", "M3", 12), ("M3", "M4", 15), ("M4", "M5", 18),
        ("Y1", "Y2", 7), ("Y2", "Y3", 9), ("Y3", "Y4", 11),
        ("P1", "P2", 6), ("P2", "P3", 8),
        ("KR1", "M1", 2), ("KR4", "Y1", 4), ("M4", "P1", 3), ("KR2", "M2", 6), ("Y2", "P2", 5),
        ("GR1", "GR2", 7), ("TR1", "TR2", 9), ("KR5", "GR1", 12), ("M5", "TR1", 14),
        ("GR2", "GR3", 5), ("GR3", "GR4", 6), ("TR2", "TR3", 7), ("TR3", "TR4", 8),
        ("TR4", "TR5", 9), ("TR5", "TR6", 10), ("KR1", "KR4", 20), ("GR1", "GR4", 15)
    ]

    for ist1, ist2, sure in baglantilar:
        metro.baglanti_ekle(ist1, ist2, sure)

    # Kullanıcı etkileşimi sağlandı.
    print("\n" + "=" * 50)
    print("HATAY METRO ROTA PLANLAYICI".center(50))
    print("=" * 50 + "\n")

    while True:
        print("\nMevcut istasyonlar:")
        istasyon_listesi = list(metro.istasyonlar.values())
        for i in range(0, len(istasyon_listesi), 3):
            satir = []
            for j in range(3):
                if i + j < len(istasyon_listesi):
                    ist = istasyon_listesi[i + j]
                    satir.append(f"{i + j + 1:2}. {ist.ad.ljust(15)} ({ist.hat})")
            print("   ".join(satir))

        print("\n" + "-" * 50)
        baslangic_giris = input("\nBaşlangıç istasyonu numarasını veya adını girin: ").strip()
        if baslangic_giris.lower() == 'q':
            break

        if baslangic_giris.isdigit():
            baslangic_idx = int(baslangic_giris) - 1
            if 0 <= baslangic_idx < len(istasyon_listesi):
                baslangic_ad = istasyon_listesi[baslangic_idx].ad
            else:
                print("\nGeçersiz numara! Lütfen listedeki bir numara girin.")
                continue
        else:
            baslangic_ad = baslangic_giris

        hedef_giris = input("Hedef istasyonu numarasını veya adını girin: ").strip()
        if hedef_giris.isdigit():
            hedef_idx = int(hedef_giris) - 1
            if 0 <= hedef_idx < len(istasyon_listesi):
                hedef_ad = istasyon_listesi[hedef_idx].ad
            else:
                print("\nGeçersiz numara! Lütfen listedeki bir numara girin.")
                continue
        else:
            hedef_ad = hedef_giris

        # İstasyon adlarını ID'lere çevirme işlemi
        baslangic_id = next((id for id, ist in metro.istasyonlar.items() if ist.ad.lower() == baslangic_ad.lower()),
                            None)
        hedef_id = next((id for id, ist in metro.istasyonlar.items() if ist.ad.lower() == hedef_ad.lower()), None)

        if not baslangic_id or not hedef_id:
            print("\nHatalı istasyon girişi! Lütfen doğru isimleri girin.")
            continue

        print("\n" + "-" * 50)
        print("1. En hızlı rota (en kısa süre)")
        print("2. En az aktarmalı rota")
        print("3. Metro ağını görüntüle")
        secim = input("Seçiminiz (1-3): ").strip()

        if secim == "1":
            sonuc = metro.en_hizli_rota_bul(baslangic_id, hedef_id)
            if sonuc:
                rota, sure = sonuc
                print("\n" + "=" * 50)
                print("EN HIZLI ROTA".center(50))
                print("=" * 50)
                print("\nRota:")
                print(" → ".join(istasyon.ad for istasyon in rota))
                print(f"\nToplam süre: {sure} dakika")
                print("\nRotanız animasyonla gösteriliyor...")
                metro.animasyonlu_rota_goster(rota)
            else:
                print("\nBelirtilen istasyonlar arasında rota bulunamadı.")

        elif secim == "2":
            sonuc = metro.en_az_aktarma_bul(baslangic_id, hedef_id)
            if sonuc:
                rota = sonuc
                print("\n" + "=" * 50)
                print("EN AZ AKTARMALI ROTA".center(50))
                print("=" * 50)
                print("\nRota:")
                print(" → ".join(istasyon.ad for istasyon in rota))
                print("\nRotanız animasyonla gösteriliyor...")
                metro.animasyonlu_rota_goster(rota)
            else:
                print("\nBelirtilen istasyonlar arasında rota bulunamadı.")

        elif secim == "3":
            print("\nMetro ağı haritası gösteriliyor...")
            metro.metro_agini_ciz()

        else:
            print("\nGeçersiz seçim! Lütfen 1, 2 veya 3 girin.")

    print("\nProgram sonlandırıldı. İyi günler!")


    