// Animacja tła - zabezpieczona przed brakiem elementu i wielokrotnym uruchomieniem
function initBackgroundAnimation() {
    const img = document.getElementById('img');

    // Sprawdź czy element istnieje i czy nie ma już uruchomionej animacji
    if (img && !img.dataset.animated) {
        img.dataset.animated = "true";

        // Konfiguracja
        let vx = 0.5; // Prędkość X
        let vy = 0.3; // Prędkość Y

        // Pozycja początkowa (środek dostępnego zakresu)
        let x = -window.innerWidth * 0.15;
        let y = -window.innerHeight * 0.15;

        function animate() {
            // Jeśli element zniknął z DOM, zakończ pętlę
            if (!document.getElementById('img')) {
                return;
            }

            const minX = -window.innerWidth * 0.25;
            const maxX = -window.innerWidth * 0.05;
            const minY = -window.innerHeight * 0.25;
            const maxY = -window.innerHeight * 0.05;

            x += vx;
            y += vy;

            // Odbijanie od granic
            if (x >= maxX || x <= minX) vx = -vx;
            if (y >= maxY || y <= minY) vy = -vy;

            // Zabezpieczenie przed "ucieczką" poza zakres
            if (x > maxX) x = maxX;
            if (x < minX) x = minX;
            if (y > maxY) y = maxY;
            if (y < minY) y = minY;

            img.style.transform = `translate3d(${x}px, ${y}px, 0)`;
            requestAnimationFrame(animate);
        }

        animate();
    }
}

// Inicjalizacja przy ładowaniu strony i po swapie HTMX
document.addEventListener('DOMContentLoaded', initBackgroundAnimation);
document.body.addEventListener('htmx:afterOnLoad', initBackgroundAnimation);
// Wywołaj od razu na wypadek gdyby skrypt był ładowany dynamicznie
initBackgroundAnimation();



let currentNumber = 1;

// Funkcja zmiany liczby
function changeNumber(change) {
    currentNumber += change;

    if (currentNumber < 1) currentNumber = 1;
    if (currentNumber > 20) currentNumber = 20;

    document.getElementById('numberDisplay').textContent = currentNumber;
}

// TYLKO JEDEN DOMContentLoaded - obsługa wszystkich przycisków b1-b7
document.addEventListener('DOMContentLoaded', function () {
    const diceMap = {
        b1: "4",
        b2: "6",
        b3: "8",
        b4: "10",
        b5: "12",
        b6: "20"
    };

    const buttons = document.querySelectorAll('.buttonrol');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            // Pobieramy ID przycisku
            const btnId = button.id || button.querySelector('img')?.id;
            if (!btnId) return;

            let diceValue;

            // Obsługa przycisku b7 (custom dice)
            if (btnId === 'b7') {
                const customInput = document.getElementById('customInput');
                const customSides = customInput.value.trim();

                // Sprawdź czy wartość jest poprawna
                if (!customSides || isNaN(customSides) || customSides < 1) {
                    alert('Wpisz poprawną liczbę ścian (np. 100)');
                    return;
                }

                diceValue = customSides; // Użyj wartości z input
            } else {
                // Obsługa przycisków b1-b6
                diceValue = diceMap[btnId];
                if (!diceValue) {
                    console.warn('Brak mapowania dla przycisku:', btnId);
                    return;
                }
            }

            const boxId = btnId.replace(/^b/, 'box'); // np. b3 -> box3
            const box = document.getElementById(boxId);
            if (!box) {
                console.warn(`Element o id "${boxId}" nie znaleziony w DOM`);
                return;
            }

            // Wyślij do Flask
            fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dice_type: diceValue,
                    dice_number: currentNumber
                })
            })
                .then(response => {
                    if (!response.ok) throw new Error('HTTP error ' + response.status);
                    return response.json();
                })
                .then(data => {
                    const result = data?.calculated_value ?? '';

                    // Usuń animację jeśli istnieje, żeby można było ją ponownie uruchomić
                    box.classList.remove('roll-animation');

                    // Wymuszenie reflow (restart animacji)
                    void box.offsetWidth;

                    // Dodaj animację
                    box.classList.add('roll-animation');

                    // Ustaw wynik
                    box.textContent = result;
                })
                .catch(err => {
                    console.error('Błąd:', err);
                    box.textContent = 'Błąd';
                });
        });
    });
}); // DODANE: zamykający nawias dla DOMContentLoaded

// ROLLER SIDEBAR TOGGLE
function toggleRoller() {
    const sidebar = document.getElementById('rollerSidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Zamknij roller klikając poza nim
document.addEventListener('click', function (e) {
    const sidebar = document.getElementById('rollerSidebar');
    const toggle = document.querySelector('.roller-toggle');

    if (sidebar &&
        !e.target.closest('.roller-sidebar') &&
        !e.target.closest('.roller-toggle')) {
        sidebar.classList.remove('active');
    }
});

// Opcjonalnie: zamknij na ESC
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        const sidebar = document.getElementById('rollerSidebar');
        if (sidebar) {
            sidebar.classList.remove('active');
        }
    }
});

// ===== OBSŁUGA GESTÓW SWIPE DLA ROLLER SIDEBAR (MOBILE) =====

(function () {
    const sidebar = document.getElementById('rollerSidebar');
    if (!sidebar) return;

    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    let isSwiping = false;

    // Minimalna odległość swipe (w pikselach)
    const minSwipeDistance = 50;

    // Maksymalna różnica pionowa (aby nie mylić z scrollowaniem)
    const maxVerticalDiff = 100;

    // SWIPE OD LEWEJ KRAWĘDZI EKRANU - otwiera sidebar
    document.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
        touchStartY = e.changedTouches[0].screenY;

        // Sprawdź czy dotknięto lewej krawędzi ekranu (pierwsze 30px)
        if (touchStartX < 30 && !sidebar.classList.contains('active')) {
            isSwiping = true;
        }
    }, { passive: true });

    document.addEventListener('touchend', function (e) {
        if (!isSwiping) return;

        touchEndX = e.changedTouches[0].screenX;
        touchEndY = e.changedTouches[0].screenY;

        const diffX = touchEndX - touchStartX;
        const diffY = Math.abs(touchEndY - touchStartY);

        // Swipe w prawo od lewej krawędzi - otwórz sidebar
        if (diffX > minSwipeDistance && diffY < maxVerticalDiff) {
            sidebar.classList.add('active');
        }

        isSwiping = false;
    }, { passive: true });

    // SWIPE W LEWO NA SIDEBARZE - zamyka sidebar
    sidebar.addEventListener('touchstart', function (e) {
        if (!sidebar.classList.contains('active')) return;

        touchStartX = e.changedTouches[0].screenX;
        touchStartY = e.changedTouches[0].screenY;
        isSwiping = true;
    }, { passive: true });

    sidebar.addEventListener('touchend', function (e) {
        if (!isSwiping || !sidebar.classList.contains('active')) return;

        touchEndX = e.changedTouches[0].screenX;
        touchEndY = e.changedTouches[0].screenY;

        const diffX = touchStartX - touchEndX; // Odwrotnie - chcemy swipe w lewo
        const diffY = Math.abs(touchEndY - touchStartY);

        // Swipe w lewo na sidebarze - zamknij
        if (diffX > minSwipeDistance && diffY < maxVerticalDiff) {
            sidebar.classList.remove('active');
        }

        isSwiping = false;
    }, { passive: true });

    // DRAG SIDEBAR - przesuń palcem
    let isDragging = false;
    let currentX = 0;
    let initialX = 0;

    sidebar.addEventListener('touchstart', function (e) {
        if (!sidebar.classList.contains('active')) return;

        // Sprawdź czy dotknięto sidebara (nie iframe wewnątrz)
        if (e.target.closest('.roller-iframe')) return;

        initialX = e.touches[0].clientX;
        isDragging = true;
    }, { passive: true });

    sidebar.addEventListener('touchmove', function (e) {
        if (!isDragging) return;

        currentX = e.touches[0].clientX - initialX;

        // Tylko przesuwanie w lewo (zamykanie)
        if (currentX < 0) {
            sidebar.style.transform = `translateX(${currentX}px)`;
        }
    }, { passive: true });

    sidebar.addEventListener('touchend', function (e) {
        if (!isDragging) return;

        isDragging = false;

        // Jeśli przeciągnięto więcej niż połowę szerokości - zamknij
        const sidebarWidth = sidebar.offsetWidth;
        if (Math.abs(currentX) > sidebarWidth / 3) {
            sidebar.classList.remove('active');
        }

        // Reset transform
        sidebar.style.transform = '';
        currentX = 0;
    }, { passive: true });
})();
// ===== AJAX FORM SUBMISSION & TOAST NOTIFICATIONS =====

document.addEventListener('DOMContentLoaded', function () {
    // 1. Dodaj kontener na toasty jeśli nie istnieje
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000;';
        document.body.appendChild(container);
    }

    // 2. Funkcja wyświetlająca toast
    window.showToast = function (message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div style="background: ${type === 'success' ? '#2c5f2d' : '#8b0000'}; 
                        color: white; padding: 15px 25px; border-radius: 8px; 
                        margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                        border: 2px solid #FFD700; font-family: sans-serif;
                        animation: slideIn 0.3s ease-out forwards;">
                ${message}
            </div>
        `;
        document.getElementById('toast-container').appendChild(toast);

        // Usuń po 5 sekundach
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    };

    // Dodaj style animacji do dokumentu
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
    `;
    document.head.appendChild(style);

    // 3. Interceptuj wszystkie formularze kart postaci
    const forms = document.querySelectorAll('form.character-form-warhammer, form.character-form-cthulhu, form.character-form-dnd5e, form.skills-form-warhammer, form.weapons-form-warhammer, form.equipment-form-warhammer');

    // Dodaj ogólny selektor dla wszystkich formularzy w kontenerach kart
    const allForms = document.querySelectorAll('form');

    allForms.forEach(form => {
        // Tylko formularze które nie mają wyłączonego AJAXa
        if (form.dataset.noAjax === 'true') return;

        // Sprawdź czy to formularz zapisu (zwykle ma button type=submit)
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(form);
            const action = form.getAttribute('action') || window.location.href;

            submitBtn.disabled = true;
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Zapisywanie...';

            fetch(action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    // Jeśli nastąpiło przekierowanie (np. sesja wygasła)
                    if (response.redirected) {
                        window.location.href = response.url;
                        return;
                    }

                    const contentType = response.headers.get("content-type");
                    if (contentType && contentType.indexOf("application/json") !== -1) {
                        return response.json();
                    } else {
                        // Logowanie błędu dla dewelopera
                        console.error('Oczekiwano JSON, otrzymano:', contentType);
                        throw new Error('Serwer zwrócił nieprawidłowy format odpowiedzi. Odśwież stronę.');
                    }
                })
                .then(data => {
                    if (data.success) {
                        showToast(data.message || 'Zapisano pomyślnie!');
                        if (data.redirect) {
                            setTimeout(() => window.location.href = data.redirect, 1000);
                        }
                    } else {
                        showToast(data.message || 'Błąd podczas zapisywania', 'error');
                    }
                })
                .catch(err => {
                    console.error('AJAX Error:', err);
                    showToast(err.message || 'Błąd połączenia.', 'error');
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                });
        });
    });
});
