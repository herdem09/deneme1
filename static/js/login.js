document.addEventListener('DOMContentLoaded', function() {
    // Particles.js başlatma
    particlesJS('particles-js', {
        particles: {
            number: {
                value: 80,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: '#ffffff'
            },
            shape: {
                type: 'circle',
                stroke: {
                    width: 0,
                    color: '#000000'
                },
            },
            opacity: {
                value: 0.5,
                random: false,
                anim: {
                    enable: false,
                    speed: 1,
                    opacity_min: 0.1,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                anim: {
                    enable: false,
                    speed: 40,
                    size_min: 0.1,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#ffffff',
                opacity: 0.4,
                width: 1
            },
            move: {
                enable: true,
                speed: 3,
                direction: 'none',
                random: false,
                straight: false,
                out_mode: 'out',
                bounce: false,
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: {
                    enable: true,
                    mode: 'grab'
                },
                onclick: {
                    enable: true,
                    mode: 'push'
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 140,
                    line_linked: {
                        opacity: 1
                    }
                },
                push: {
                    particles_nb: 4
                }
            }
        },
        retina_detect: true
    });

    // HTML elementleri
    const girisBtn = document.getElementById('girisBtn');
    const dogrulaBtn = document.getElementById('dogrulaBtn');
    const kullaniciAdi = document.getElementById('kullaniciAdi');
    const sifre = document.getElementById('sifre');
    const dogrulamaKodu = document.getElementById('dogrulamaKodu');
    const loginContainer = document.getElementById('loginContainer');
    const verifyContainer = document.getElementById('verifyContainer');
    const hataGiris = document.getElementById('hataGiris');
    const hataDogrulama = document.getElementById('hataDogrulama');

    // Giriş butonu tıklama olayı
    girisBtn.addEventListener('click', async () => {
        if (!kullaniciAdi.value || !sifre.value) {
            hataGiris.textContent = 'Lütfen kullanıcı adı ve şifre girin!';
            return;
        }

        try {
            const response = await fetch('/giris', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    kullanici_adi: kullaniciAdi.value,
                    sifre: sifre.value
                })
            });

            const data = await response.json();

            if (data.success) {
                // Giriş başarılı, doğrulama ekranını göster
                loginContainer.style.display = 'none';
                verifyContainer.style.display = 'block';
                
                // E-posta gönderildiğini simüle etmek için bilgi mesajı
                console.log('E-posta gönderildi: hidayete369@gmail.com');
                console.log('Gönderen: herdemerasmus@gmail.com');
                console.log('Uygulama kodu: kmop hzuo yoqp ztnr');
            } else {
                // Hata mesajı göster
                hataGiris.textContent = data.mesaj || 'Giriş başarısız!';
            }
        } catch (error) {
            hataGiris.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
            console.error('Giriş hatası:', error);
        }
    });

    // Doğrulama butonu tıklama olayı
    dogrulaBtn.addEventListener('click', async () => {
        if (!dogrulamaKodu.value) {
            hataDogrulama.textContent = 'Lütfen doğrulama kodunu girin!';
            return;
        }

        try {
            const response = await fetch('/dogrula', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    kod: dogrulamaKodu.value
                })
            });

            const data = await response.json();

            if (data.success) {
                // Doğrulama başarılı, dashboard'a yönlendir
                window.location.href = '/dashboard';
            } else {
                // Hata mesajı göster
                hataDogrulama.textContent = data.mesaj || 'Doğrulama başarısız!';
            }
        } catch (error) {
            hataDogrulama.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
            console.error('Doğrulama hatası:', error);
        }
    });

    // Enter tuşu ile giriş/doğrulama
    kullaniciAdi.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sifre.focus();
    });

    sifre.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') girisBtn.click();
    });

    dogrulamaKodu.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') dogrulaBtn.click();
    });
});
