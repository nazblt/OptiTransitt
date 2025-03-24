# OptiTransit

### Projenin Açıklaması:
Bu proje, Hatay metro ağını modelleyen bir rota planlama sistemidir.
Kullanıcıların belirli iki istasyon arasındaki en kısa veya en az aktarmalı rotayı bulmalarına yardımcı olur. 
Proje, metro istasyonlarını ve hatlarını bir grafik veri yapısı kullanarak temsil eder ve farklı rotaları hesaplamak için algoritmalar içerir. 
Ayrıca, kullanıcıya sesli anons ve görsel animasyon ile yönlendirme sağlayarak interaktif bir deneyim sunar.


### Projenin Amacı: 
1. Graf veri yapısını kullanarak metro ağını modelleme
2. BFS (Breadth-First Search) algoritması ile en az aktarmalı rotayı bulma
3. A* algoritması ile en hızlı rotayı bulma
4. Gerçek dünya problemlerini algoritmik düşünce ile çözme

### Kullanılan Teknolojiler ve Kütüphaneler:

1.Python

2.Heapq:
Python'un standart kütüphanelerinden biri olan heapq, öncelikli kuyruk (priority queue) işlemleri için kullanılır.

3.Collections:

Python'un collections modülü, gelişmiş veri yapılarını içerir.
Genellikle deque, defaultdict ve Counter gibi yapıları barındırır.

4.Pyttsx3: 

Metni sese dönüştürmek için kullanılır.

5.Time:
Bu modül sayesinde zamanı ölçme, bekleme, tarih ve saat bilgilerini alma gibi işlemleri gerçekleştirilir.

6.Typing:
Bu modül, değişkenlerin ve fonksiyonların tiplerini belirtmek için kullanılır.

7. Matplotlib:
   
Matplotlib, Python'da veri görselleştirmeleri (grafikler, diyagramlar, çizimler vb.) yapmak için

kullanılan en popüler kütüphanelerden biridir.

8. Matplotlib.animation:

Animasyonları oluşturmak için kullanılan bir modüldür.

Bu modül, matplotlib'in sunduğu görsel öğeleri animasyonlu bir şekilde göstermemize olanak sağlar.

Özellikle zamanla değişen veri görselleştirmeleri yapmak istiyorsanız kullanışlıdır.


### Algoritmaların Çalışma Mantığı 

#### 1. BFS (Breadth-First Search) Algoritması:

Çalışma Mantığı: BFS, en kısa yol problemi gibi durumlarda genişleme stratejisini kullanarak çalışır. Temel olarak, BFS algoritması şu şekilde işler:

Başlangıç noktasını belirleyin.

Kuyruk kullanarak (Queue), her bir komşuya genişleyin. Kuyruk, bir FIFO (First In, First Out) yapısına sahiptir, yani önce eklenen elemanlar önce çıkar.

Her bir düğüm (node) ziyaret edilir ve daha önce ziyaret edilmemiş düğümler kuyrukta beklemeye alınır. Bu süreç, hedefe ulaşana kadar devam eder.

BFS, her zaman en kısa yolu bulur çünkü önceki seviyelerdeki tüm düğümleri ziyaret ettikten sonra bir sonraki seviyedeki düğümlere geçer.

### Neden BFS Kullandık?

BFS, genellikle en kısa yol gibi problemlerde kullanılır, çünkü her bir adımda tüm komşu düğümleri kontrol ederek ilerler. 
Bu sayede, hedefe ulaşan ilk yol, en kısa yol olacaktır.
Eğer arama ağında her bir adım aynı maliyeti taşıyorsa ve optimizasyon gereksiniminiz varsa, BFS etkili bir çözüm sunar.



### 2. A* Algoritması:
Çalışma Mantığı: A* algoritması, en kısa yol bulma algoritmalarından biridir ve
genellikle yol bulma, harita üzerinde en kısa mesafe hesaplama gibi görevlerde kullanılır.

A* algoritması, f(n) = g(n) + h(n) formülüne dayalı olarak çalışır:

g(n): Başlangıç noktasından şu anki düğüme kadar olan maliyet (mesafe).

h(n): Şu anki düğümden hedef düğüme olan tahmini mesafe (hedef fonksiyonu).

f(n): Toplam maliyet, yani g(n) + h(n).

#### A* algoritması şu şekilde çalışır:

Başlangıç noktasından başlar ve her adımda en düşük f(n) değerine sahip düğümü seçer.

Her bir komşuya olan mesafeyi ve tahmini hedef mesafesini hesaplar ve ilerler.

Her seferinde, daha düşük toplam maliyeti olan yol seçilir, böylece daha verimli bir arama yapılır.

### Neden A* Kullandık? 

A* algoritması, BFS’ye göre daha verimlidir çünkü hem gerçek mesafeyi (g(n)) hem de hedefe olan tahmini mesafeyi (h(n)) dikkate alır. 
Bu sayede, gereksiz dallanmayı engeller ve hedefe daha hızlı ulaşır. 
BFS, sadece mesafe hesaplar, A* ise daha stratejik bir yaklaşım kullanır ve daha hızlı sonuca ulaşır.



## 4. Örnek Kullanım ve Test Sonuçları:



## 5.Projeyi Geliştirme Fikirleri:

### 1. Dinamik Zaman Yönetimi ve Rotalar:

Metro sistemlerinde en önemli unsurlardan biri zaman yönetimidir.

Bu simülasyona, trenlerin hızlarının, bekleme sürelerinin, yolcu yoğunluklarının, ve istasyonlar arası mesafelerin dinamik olarak değişmesini eklenebilir.

Zaman Tabanlı Simülasyon: Gerçek zamanlı bir simülasyon yerine, simülasyonun hızını kontrol edebileceğiniz bir sistem eklenebilir.


### 2. Yolcu Akışı ve Yoğunluk Yönetimi:
   
Metro sistemlerinin verimli çalışabilmesi için yolcu akışını iyi yönetmek gerekir.

Bu simülasyona, istasyonlardaki yolcu yoğunluğunu ve trenlerin doluluk oranlarını daha gerçekçi bir şekilde simüle edilebilir.

Yolcu Akışı Simülasyonu: Yolcuların geliş saatlerini ve istasyonlardaki yoğunlukları modellenebilir.


### 3. Tren Hareketleri ve Hız Kontrolü:
   
Metro trenlerinin hızlarının ve hareketlerinin dinamik olarak değişmesi, simülasyonu daha gerçekçi ve eğlenceli kılacaktır.

Farklı Hız Modları: Trenlerin hızları arttırılıp azaltılabilir.


### 4. Gerçekçi İstasyonlar ve İstasyonlar Arası Mesafeler:
   
Metro simülasyonunun daha gerçekçi olması için istasyonlar arasındaki mesafeleri ve her bir istasyonun özellikleri detaylandırabilir.


### 5. Gerçekçi Işıklandırma ve Çevresel Faktörler:

Metro sisteminin daha gerçekçi hale gelmesi için çevresel faktörler ve ışıklandırma eklemek projeyi güzelleştirebilir.


### 6. Yapay Zeka ile Trafik Yönetimi:

Metro sistemlerinin yönetiminde yapay zeka kullanımı, trenlerin birbirleriyle olan etkileşimini yönetmek için faydalı olabilir.




























