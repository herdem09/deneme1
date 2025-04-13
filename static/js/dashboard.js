// Kontrol Paneli JavaScript Kodu
document.addEventListener('DOMContentLoaded', function() {
    // API Bilgileri
    const API_URL = '/data';
    const API_KEY = 'herdem1940';
    
    // HTML Elementleri
    const refreshBtn = document.getElementById('refreshBtn');
    const saveChangesBtn = document.getElementById('saveChangesBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const connectionStatus = document.getElementById('connectionStatus');
    const updateTimeElement = document.getElementById('updateTime');
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    
    // Kontrol değişkenleri
    const controls = {
        kapi: document.getElementById('kapi-toggle'),
        vantilator: document.getElementById('vantilator-toggle'),
        pencere: document.getElementById('pencere-toggle'),
        perde: document.getElementById('perde-toggle')
    };

    const kapiTimer = document.getElementById('kapi-timer');
    let kapiTimerId = null;
    
    // Sayfa yüklendiğinde verileri al
    fetchData();
    
    // Yenile butonu
    refreshBtn.addEventListener('click', function() {
        animateRefreshButton();
        fetchData();
    });
    
    // Değişiklikleri kaydet butonu
    saveChangesBtn.addEventListener('click', function() {
        saveChanges();
    });
    
    // Çıkış butonu
    logoutBtn.addEventListener('click', function() {
        window.location.href = 'index.html';
    });
    
    // Sunucudan veri çekme fonksiyonu
    function fetchData() {
        showLoadingState(true);
        
        fetch(API_URL, {
            method: 'GET',
            headers: {
                'Authorization': API_KEY,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Sunucu bağlantısı başarısız oldu');
            }
            return response.json();
        })
        .then(data => {
            updateUIWithData(data);
            updateConnectionStatus(true);
            showNotification('Veriler başarıyla güncellendi', 'success');
        })
        .catch(error => {
            console.error('Veri alınamadı:', error);
            updateConnectionStatus(false);
            showNotification('Veri alınamadı: ' + error.message, 'error');
        })
        .finally(() => {
            showLoadingState(false);
            updateLastUpdateTime();
        });
    }
    
    // Verileri sunucuya gönderme fonksiyonu
    function saveChanges() {
        const updatedData = {
            kapi: controls.kapi.checked,
            vantilator: controls.vantilator.checked,
            pencere: controls.pencere.checked,
            perde: controls.perde.checked
        };
        
        // Kapı otomatik kapanma kontrolü
        if (controls.kapi.checked) {
            startKapiTimer();
        } else {
            stopKapiTimer();
        }
        
        showLoadingState(true);
        
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': API_KEY,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Veriler kaydedilemedi');
            }
            return response.json();
        })
        .then(data => {
            console.log('Güncelleme başarılı:', data);
            updateConnectionStatus(true);
            showNotification('Değişiklikler başarıyla kaydedildi', 'success');
            
            // Kapı animasyonu
            if (updatedData.kapi) {
                animateItem('kapi-toggle');
            }
        })
        .catch(error => {
            console.error('Veriler kaydedilemedi:', error);
            updateConnectionStatus(false);
            showNotification('Veriler kaydedilemedi: ' + error.message, 'error');
        })
        .finally(() => {
            showLoadingState(false);
            updateLastUpdateTime();
        });
    }
    
    // UI'ı verilerle güncelleme fonksiyonu
    function updateUIWithData(data) {
        for (const [key, value] of Object.entries(data)) {
            if (controls[key]) {
                controls[key].checked = value === true;
                
                // Kapı otomatik kapanma kontrolü
                if (key === 'kapi' && value === true) {
                    startKapiTimer();
                }
            }
        }
    }
    
    // Kapı otomatik kapanma zamanlayıcısı
    function startKapiTimer() {
        // Eğer önceki zamanlayıcı varsa temizle
        stopKapiTimer();
        
        let secondsLeft = 10;
        updateKapiTimerDisplay(secondsLeft);
        
        kapiTimerId = setInterval(() => {
            secondsLeft--;
            updateKapiTimerDisplay(secondsLeft);
            
            if (secondsLeft <= 0) {
                stopKapiTimer();
                controls.kapi.checked = false;
                
                // Kapı kapandı bildirimi
                showNotification('Kapı otomatik olarak kapatıldı', 'info');
                
                // Sunucuya kapı kapandı durumunu gönder
                const updatedData = { kapi: false };
                
                fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Authorization': API_KEY,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedData)
                })
                .then(response => response.json())
                .then(data => console.log('Kapı otomatik kapatıldı:', data))
                .catch(error => console.error('Kapı kapatma hatası:', error));
            }
        }, 1000);
    }
    
    // Kapı zamanlayıcısını durdurma
    function stopKapiTimer() {
        if (kapiTimerId !== null) {
            clearInterval(kapiTimerId);
            kapiTimerId = null;
            kapiTimer.textContent = '';
        }
    }
    
    // Kapı zamanlayıcı ekranını güncelleme
    function updateKapiTimerDisplay(seconds) {
        kapiTimer.textContent = `Otomatik kapanacak: ${seconds} saniye`;
        
        // Kalan zamanla renk değiştirme
        if (seconds <= 3) {
            kapiTimer.style.color = '#dc3545'; // Kırmızı
        } else if (seconds <= 5) {
            kapiTimer.style.color = '#ffc107'; // Sarı
        } else {
            kapiTimer.style.color = '#17a2b8'; // Mavi
        }
    }
    
    // Bağlantı durumunu güncelleme
    function updateConnectionStatus(isConnected) {
        if (isConnected) {
            connectionStatus.className = 'connected';
            connectionStatus.innerHTML = '<i class="fas fa-plug"></i> Bağlantı: Aktif';
        } else {
            connectionStatus.className = 'disconnected';
            connectionStatus.innerHTML = '<i class="fas fa-plug-circle-xmark"></i> Bağlantı: Kesildi';
        }
    }
    
    // Son güncelleme zamanını ayarlama
    function updateLastUpdateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('tr-TR');
        updateTimeElement.textContent = timeString;
    }
    
    // Yükleniyor durumunu gösterme
    function showLoadingState(isLoading) {
        if (isLoading) {
            document.body.classList.add('loading');
            refreshBtn.disabled = true;
            saveChangesBtn.disabled = true;
        } else {
            document.body.classList.remove('loading');
            refreshBtn.disabled = false;
            saveChangesBtn.disabled = false;
        }
    }
    
    // Bildirim gösterme fonksiyonu
    function showNotification(message, type = 'info') {
        notification.className = 'notification ' + type;
        notificationText.textContent = message;
        
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
    
    // Yenile butonuna animasyon ekleme
    function animateRefreshButton() {
        refreshBtn.classList.add('rotating');
        setTimeout(() => {
            refreshBtn.classList.remove('rotating');
        }, 1000);
    }
    
    // Öğeye animasyon ekleme
    function animateItem(itemId) {
        const element = document.getElementById(itemId).parentElement.parentElement.parentElement;
        element.classList.add('pulse-animation');
        setTimeout(() => {
            element.classList.remove('pulse-animation');
        }, 1000);
    }
    
    // CSS ile animasyon ekleme
    const style = document.createElement('style');
    style.textContent = `
        body.loading {
            cursor: progress;
        }
        
        .rotating {
            animation: rotate 1s linear;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .pulse-animation {
            animation: pulse-item 1s ease;
        }
        
        @keyframes pulse-item {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
});
