document.addEventListener('DOMContentLoaded', function() {
    // API anahtarı
    const API_KEY = 'herdem1940';
    
    // HTML Elementleri
    const kapiToggle = document.getElementById('kapiToggle');
    const ventilatorToggle = document.getElementById('ventilatorToggle');
    const pencereToggle = document.getElementById('pencereToggle');
    const perdeToggle = document.getElementById('perdeToggle');
    
    const kapiDurum = document.getElementById('kapiDurum');
    const ventilatorDurum = document.getElementById('ventilatorDurum');
    const pencereDurum = document.getElementById('pencereDurum');
    const perdeDurum = document.getElementById('perdeDurum');
    
    const kaydetBtn = document.getElementById('kaydetBtn');
    const yenileBtn = document.getElementById('yenileBtn');
    const bildirim = document.getElementById('bildirim');
    const kapiTimer = document.getElementById('kapi-timer');
    const kapiTimerCount = document.getElementById('kapi-timer-count');
    
    // Veri Durumu
    let veriDurumu = {
        kapi: false,
        vantilator: false,
        pencere: false,
        perde: false
    };
    
    // Güncellemeler
    let bekleyenGuncellemeler = {};
    
    // Vantilatör animasyonu için fan ikonunu seç
    const fanIkonu = document.querySelector('.fa-fan');
    
    // Değişkenleri güncelle
    function arayuzuGuncelle() {
        // Kapı durumu
        kapiToggle.checked = veriDurumu.kapi;
        kapiDurum.textContent = veriDurumu.kapi ? 'Açık' : 'Kapalı';
        kapiDurum.style.color = veriDurumu.kapi ? '#2ecc71' : '#e74c3c';
        
        // Vantilatör durumu
        ventilatorToggle.checked = veriDurumu.vantilator;
        ventilatorDurum.textContent = veriDurumu.vantilator ? 'Açık' : 'Kapalı';
        ventilatorDurum.style.color = veriDurumu.vantilator ? '#2ecc71' : '#e74c3c';
        
        // Vantilatör animasyonu
        if (veriDurumu.vantilator) {
            fanIkonu.classList.add('spin-animation');
        } else {
            fanIkonu.classList.remove('spin-animation');
        }
        
        // Pencere durumu
        pencereToggle.checked = veriDurumu.pencere;
        pencereDurum.textContent = veriDurumu.pencere ? 'Açık' : 'Kapalı';
        pencereDurum.style.color = veriDurumu.pencere ? '#2ecc71' : '#e74c3c';
        
        // Perde durumu
        perdeToggle.checked = veriDurumu.perde;
        perdeDurum.textContent = veriDurumu.perde ? 'Açık' : 'Kapalı';
        perdeDurum.style.color = veriDurumu.perde ? '#2ecc71' : '#e74c3c';
    }
    
    // Verileri sunucudan al
    async function verileriGetir() {
        try {
            const response = await fetch('/data', {
                method: 'GET',
                headers: {
                    'Authorization': API_KEY
                }
            });
            
            if (!response.ok) {
                throw new Error('Veri alınamadı');
            }
            
            const data = await response.json();
            
            // Verileri güncelle
            veriDurumu = {
                kapi: data.kapi || false,
                vantilator: data.vantilator || false,
                pencere: data.pencere || false,
                perde: data.perde || false
            };
            
            // Arayüzü güncelle
            arayuzuGuncelle();
            
            // Bildirim göster
            bildirimGoster('Veriler başarıyla alındı', 'success');
            
        } catch (error) {
            console.error('Veri getirme hatası:', error);
            bildirimGoster('Veriler alınamadı! Bir hata oluştu.', 'error');
        }
    }
    
    // Değişiklikleri sunucuya gönder
    async function degisiklikleriKaydet() {
        if (Object.keys(bekleyenGuncellemeler).length === 0) {
            bildirimGoster('Kaydedilecek değişiklik yok!', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/data', {
                method: 'POST',
                headers: {
                    'Authorization': API_KEY,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bekleyenGuncellemeler)
            });
            
            if (!response.ok) {
                throw new Error('Değişiklikler kaydedilemedi');
            }
            
            const data = await response.json();
            
            // Mevcut durumu güncelle
            for (const key in bekleyenGuncellemeler) {
                veriDurumu[key] = bekleyenGuncellemeler[key];
            }
            
            // Bekleyen güncellemeleri temizle
            bekleyenGuncellemeler = {};
            
            // Arayüzü güncelle
            arayuzuGuncelle();
            
            // Bildirim göster
            bildirimGoster('Değişiklikler başarıyla kaydedildi', 'success');
            
            // Kapı açıldıysa zamanlayıcıyı başlat
            if (veriDurumu.kapi) {
                kapiTimerBaslat();
            }
            
        } catch (error) {
            console.error('Kaydetme hatası:', error);
            bildirimGoster('Değişiklikler kaydedilemedi! Bir hata oluştu.', 'error');
        }
    }
    
    // Bildirim göster
    function bildirimGoster(mesaj, tur = 'success') {
        bildirim.textContent = mesaj;
        bildirim.style.display = 'block';
        
        // Bildirim stilini ayarla
        if (tur === 'success') {
            bildirim.style.backgroundColor = '#2ecc71';
        } else if (tur === 'error') {
            bildirim.style.backgroundColor = '#e74c3c';
        } else if (tur === 'warning') {
            bildirim.style.backgroundColor = '#f39c12';
        }
        
        // 3 saniye sonra bildirim kaybolsun
        setTimeout(() => {
            bildirim.style.display = 'none';
        }, 3000);
    }
    
    // Kapı için zamanlayıcı başlat
    function kapiTimerBaslat() {
        let kalanSure = 10;
        kapiTimer.style.display = 'flex';
        
        // Zamanlayıcı gösterim
        const sayac = setInterval(() => {
            kalanSure--;
            kapiTimerCount.textContent = kalanSure;
            
            if (kalanSure <= 0) {
                clearInterval(sayac);
                kapiTimer.style.display = 'none';
            }
        }, 1000);
    }
    
    // Toggle butonları için olay dinleyicileri
    kapiToggle.addEventListener('change', function() {
        bekleyenGuncellemeler.kapi = this.checked;
    });
    
    ventilatorToggle.addEventListener('change', function() {
        bekleyenGuncellemeler.vantilator = this.checked;
    });
    
    pencereToggle.addEventListener('change', function() {
        bekleyenGuncellemeler.pencere = this.checked;
    });
    
    perdeToggle.addEventListener('change', function() {
        bekleyenGuncellemeler.perde = this.checked;
    });
    
    // Kaydet butonu için olay dinleyicisi
    kaydetBtn.addEventListener('click', degisiklikleriKaydet);
    
    // Yenile butonu için olay dinleyicisi
    yenileBtn.addEventListener('click', verileriGetir);
    
    // Sayfa yüklendiğinde verileri getir
    verileriGetir();
});
