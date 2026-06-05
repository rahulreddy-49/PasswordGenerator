/* 
 * CipherVault - Core Platform Logic
 * Handles animations, backgrounds, and global UI state.
 */

document.addEventListener('DOMContentLoaded', () => {
    initMatrix();
    initRevealAnimations();
    initSmoothScroll();
});

/* --- Subtle Matrix Rain Implementation --- */
function initMatrix() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    const chars = "0123456789ABCDEFHIJKLMNOPQRSTUVWXYZ@#$%&*+=".split("");
    const fontSize = 14;
    const columns = width / fontSize;
    const drops = [];

    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }

    function draw() {
        // Subtle fade effect for tails
        ctx.fillStyle = "rgba(11, 17, 32, 0.05)";
        ctx.fillRect(0, 0, width, height);

        // Soft Cyan/Green color for a premium tech look
        ctx.fillStyle = "rgba(0, 255, 204, 0.15)";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 33);

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });
}

/* --- Card Spotlight Mouse Tracking --- */
document.addEventListener('mousemove', e => {
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
    });
});

/* --- Scroll Reveal Animations --- */
function initRevealAnimations() {
    const reveals = document.querySelectorAll('.reveal');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1
    });

    reveals.forEach(reveal => {
        revealObserver.observe(reveal);
    });

    // Fallback: If elements are already in view or observer fails, show them after a delay
    setTimeout(() => {
        reveals.forEach(reveal => {
            const rect = reveal.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                reveal.classList.add('active');
            }
        });
    }, 500);
}

/* --- Smooth Scrolling --- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* --- UI Utilities --- */
function showToast(message, type = 'info') {
    const colors = {
        success: "linear-gradient(to right, #00b09b, #96c93d)",
        error: "linear-gradient(to right, #ff5f6d, #ffc371)",
        info: "linear-gradient(to right, #2193b0, #6dd5ed)",
        warning: "linear-gradient(to right, #f83600, #f9d423)"
    };

    if (typeof Toastify !== 'undefined') {
        Toastify({
            text: message,
            duration: 3000,
            gravity: "bottom",
            position: "right",
            style: {
                background: colors[type] || colors.info,
                borderRadius: "10px",
                fontFamily: "'Poppins', sans-serif",
                fontSize: "14px",
                boxShadow: "0 10px 20px rgba(0,0,0,0.2)"
            }
        }).showToast();
    } else {
        console.log(`Toast (${type}): ${message}`);
    }
}

/* --- Glassmorphism Mouse Interaction --- */
document.addEventListener('mousemove', e => {
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
    });
});
