// Sayfa yüklendiğinde çalışacak kod
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const mailModal = document.getElementById('mailModal');
    const closeModalBtn = document.querySelector('.close');
    const verifyCodeBtn = document.getElementById('verifyCodeBtn');
    const verifyErrorMessage = document.getElementById('verifyErrorMessage');
    
    // Doğru kullanıcı adı ve şifre
    const CORRECT_USERNAME = "herdem";
    const CORRECT_PASSWORD = "1940";
    const CORRECT_CODE = "kmop hzuo yoqp ztnr";
    
    // Giriş formu gönderildiğinde
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Kullanıcı adı ve şifre kontrolü
        if (username === CORRECT_USERNAME && password === CORRECT_PASSWORD) {
            errorMessage.textContent = '';
            showNotification('Giriş bilgileri doğru! Onay kodu gönderiliyor...', 'success');
            
            // E-posta gönderiliyor simülasyonu
            setTimeout(() => {
                mailModal.style.display = 'block';
                simulateEmailSent();
            }, 1500);
        } else {
            errorMessage.textContent = 'Kullanıcı adı veya şifre hatalı!';
            shakeElement(loginForm);
        }
    });
    
    // Modal kapatma butonu
    closeModalBtn.addEventListener('click', function() {
        mailModal.style.display = 'none';
    });
    
    // Modal dışına tıklanırsa kapatma
    window.addEventListener('click', function(event) {
        if (event.target == mailModal) {
            mailModal.style.display = 'none';
        }
    });
    
    // Onay kodu doğrulama
    verifyCodeBtn.addEventListener('click', function() {
        const verificationCode = document.getElementById('verificationCode').value;
        
        if (verificationCode.trim() === CORRECT_CODE) {
            verifyErrorMessage.textContent = '';
            showNotification('Onay başarılı! Yönlendiriliyorsunuz...', 'success');
            
            // Dashboard'a yönlendirme
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        } else {
            verifyErrorMessage.textContent = 'Onay kodu hatalı!';
            shakeElement(document.getElementById('verificationCode'));
        }
    });
    
    // E-posta gönderildi simülasyonu
    function simulateEmailSent() {
        console.log("E-posta gönderildi: hidayete369@gmail.com");
        // Gerçekte burada bir API çağrısı yapılabilir
        const emailDetails = {
            to: "hidayete369@gmail.com",
            from: "herdemerasmus@gmail.com",
            subject: "İTÜ MTAL Akıllı Ev Sistemi - Giriş Onay Kodu",
            code: CORRECT_CODE
        };
        
        console.log("E-posta detayları:", emailDetails);
    }
    
    // Bildirim gösterme fonksiyonu
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    }
    
    // Element titreşim efekti
    function shakeElement(element) {
        element.classList.add('shake');
        setTimeout(() => {
            element.classList.remove('shake');
        }, 500);
    }
    
    // CSS ile titreşim animasyonu
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .shake {
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            z-index: 1000;
            transform: translateX(120%);
            transition: transform 0.3s ease-out;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification i {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        .notification.success {
            background-color: #28a745;
        }
        
        .notification.error {
            background-color: #dc3545;
        }
    `;
    document.head.appendChild(style);
});
