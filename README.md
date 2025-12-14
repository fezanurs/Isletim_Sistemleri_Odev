İşletim Sistemleri Ödevi
Merhaba bu projeyi İşletim Sistemleri dersi kapsamındaki CPU zamanlama algoritmalarını pekiştirmek için hazırladım. Ödevde istenen FCFS, SJF, Priority ve Round Robin algoritmalarının hepsini Python ile kodladım ve test ettim.

Amaç, verilen süreçleri  farklı algoritmalara sokup hangisinin daha hızlı veya verimli çalıştığını görmekti.

Dosyalar Neler?
Projeyi daha rahat yönetmek için her algoritmayı ayrı dosya yaptım, karışıklık olsun istemedim:
case1.csv ve case2.csv Ödevde verilen test verileri. Kodlar bunları otomatik okuyor.
fcfs_odev.py İlk gelen ilk hizmet alır (FCFS) mantığı.
sjf_np.py ve sjf_preemptive.py En kısa işi öne alan algoritmalar (SJF). Hem kesmeli hem kesmesiz versiyonları var.
priority_np.py ve priority_preemptive.py Öncelik sırasına göre çalışanlar.
round_robin.py Zaman paylaşımlı çalışan algoritma.

Nasıl Çalıştırılır?
Dosyaları indirdikten sonra terminali klasörün olduğu yerde açın.
Hangi algoritmayı denemek istiyorsanız ismini yazıp çalıştırın.
örnek : python round_robin.py

Kod çalıştığında case1.csv ve case2.csv dosyalarını okuyup sonuçları ekrana basıyor. Ayrıca çıktıları kaybetmemek için yanına .txt dosyası olarak da kaydediyor
