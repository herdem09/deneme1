document.addEventListener('DOMContentLoaded', function() {
    // Kontrol elemanlarını seçme
    const kapiControl = document.getElementById('kapiControl');
    const vantilatorControl = document.getElementById('vantilatorControl');
    const pencereControl = document.getElementById('pencereControl');
    const perdeControl = document.getElementById('perdeControl');
    
    const kapiIcon = document.getElementById('kapiIcon');
    const vantilatorIcon = document.getElementById('vantilatorIcon');
    const pencereIcon = document.getElementById('pencereIcon');
    const perdeIcon = document.getElementById('perdeIcon');
    
    const kapiStatus = document.getElementById('kapiStatus');
    const vantilatorStatus = document.getElementById('vantilatorStatus');
    const pencereStatus = document.getElementById('pencereStatus');
    const perdeStatus = document.getElementById('perdeStatus');
    
    const saveButton = document.getElementById('saveChangesButton');
    const refreshButton = document.getElementById('refreshButton');
    const saveMessage = document.getElementById('saveMessage');
    
    // Değişiklik durumlarını izleme
    let hasChanges = false;
    let originalStates = {};
    
    // Tüm kontrolleri dinleme
    [kapiControl, vantilatorControl, pencereControl, perdeControl].forEach(control => {
        control.addEventListener('change', function() {
            hasChanges = true;
            updateStatusText(this);
            updateIcon(this);
            
            // Kapı özel durumu (10 saniye sonra otomatik kapanma)
            if (this.id === 'kapiControl' && this.checked) {
                setTimeout(() => {
                    if (this.checked) { // Hala açıksa kapat
                        this.checked = false;
                        updateStatusText(this);
                        updateIcon(this);
                    }
                }, 10000);
            }
        });
    });
    
    // Durum metinlerini güncelleme
    function updateStatusText(control) {
        const statusElement = document.getElementById(control.id.replace('Control', 'Status'));
        if (statusElement) {
            statusElement.textContent = control.checked ? 'Açık' : 'Kapalı';
            statusElement.style.color = control.checked ? '#1cc88a' : '#5a5c69';
        }
    }
    
    // Durum ikonlarını güncelleme
    function updateIcon(control) {
        const iconId = control.id.replace('Control', 'Icon');
        const iconElement = document.getElementById(iconId);
        
        if (iconElement) {
            // Ikon sınıfını değiştir
            if (control.id === 'kapiControl') {
                iconElement.className = control.checked ? 'fas fa-door-open active' : 'fas fa-door-closed';
            } else if (control.id === 'vantilatorControl') {
                iconElement.className = control.checked ? 'fas fa-fan active' : 'fas fa-fan';
            } else if (control.id === 'pencereControl') {
                iconElement.className = control.checked ? 'fas fa-window-maximize active' : 'fas fa-window-maximize';
            } else if (control.id === 'perdeControl') {
                iconElement.className = control.checked ? 'fas fa-blinds active' : 'fas fa-blinds';
            }
        }
    }
    
    // Verileri sunucudan alma
    function fetchData() {
        showMessage('Veriler yükleniyor...', '');
        
        fetch('/api/data')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Veri yüklenirken hata oluştu.');
                }
                return response.json();
            })
            .then(data => {
                // Orijinal durumları kaydet
                originalStates = {...data};
                
                // Arayüzü güncelle
                kapiControl.checked = data.kapi;
                vantilatorControl.checked = data.vantilator;
                pencereControl.checked = data.pencere;
                perdeControl.checked = data.perde;
                
                // Durum metinlerini güncelle
                [kapiControl, vantilatorControl, pencereControl, perdeControl].forEach(updateStatusText);
                [kapiControl, vantilatorControl, pencereControl, perdeControl].forEach(updateIcon);
                
                hasChanges = false;
                saveMessage.textContent = '';
                saveMessage.className = 'save-message';
            })
            .catch(error => {
                showMessage(error.message, 'error-message');
            });
    }
    
    // Değişiklikleri kaydetme
    function saveChanges() {
        if (!hasChanges) {
            showMessage('Değişiklik yapılmadı.', '');
            return;
        }
        
        const updatedData = {
            kapi: kapiControl.checked,
            vantilator: vantilatorControl.checked,
            pencere: pencereControl.checked,
            perde: perdeControl.checked
        };
        
        showMessage('Değişiklikler kaydediliyor...', '');
        
        fetch('/api/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Değişiklikler kaydedilirken hata oluştu.');
                }
                return response.json();
            })
            .then(data => {
                showMessage('Değişiklikler başarıyla kaydedildi!', 'success-message');
                hasChanges = false;
                originalStates = {...updatedData};
            })
            .catch(error => {
                showMessage(error.message, 'error-message');
            });
    }
    
    // Mesaj gösterme
    function showMessage(message, className) {
        saveMessage.textContent = message;
        saveMessage.className = 'save-message ' + className;
    }
    
    // Sayfa yüklendiğinde verileri getir
    fetchData();
    
    // Buton olaylarını dinleme
    saveButton.addEventListener('click', saveChanges);
    refreshButton.addEventListener('click', fetchData);
});
