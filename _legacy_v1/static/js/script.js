// --- Password Generator Logic ---
async function generatePassword() {
    const length = document.getElementById('length').value;
    const upper = document.getElementById('upper').checked;
    const lower = document.getElementById('lower').checked;
    const digits = document.getElementById('digits').checked;
    const symbols = document.getElementById('symbols').checked;

    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ length, upper, lower, digits, symbols })
    });

    const data = await response.json();
    const pwdInput = document.getElementById('generated-password');
    pwdInput.value = data.password;
    updateStrengthMeter(data.analysis);
}

// --- Strength Meter UI ---
function updateStrengthMeter(analysis) {
    const bar = document.getElementById('strength-bar');
    const text = document.getElementById('strength-text');
    const entropy = document.getElementById('entropy-score');
    const crackTime = document.getElementById('crack-time');

    const scores = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
    const colors = ['#ef4444', '#f59e0b', '#fbbf24', '#10b981', '#00ffcc'];

    const percentage = (analysis.score + 1) * 20;
    bar.style.width = percentage + '%';
    bar.style.backgroundColor = colors[analysis.score];
    text.innerText = scores[analysis.score];
    text.style.color = colors[analysis.score];

    if (entropy) entropy.innerText = analysis.entropy;
    if (crackTime) crackTime.innerText = analysis.crack_time;
}

// --- Password Analyzer Logic ---
let analyzeTimeout;
function analyzePasswordInput(value) {
    if (analyzeTimeout) clearTimeout(analyzeTimeout);
    analyzeTimeout = setTimeout(async () => {
        if (!value) return;
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: value })
        });
        const data = await response.json();
        updateStrengthMeter(data);
        
        // Show suggestions if any
        const suggestionsDiv = document.getElementById('analysis-feedback');
        if (suggestionsDiv) {
            let html = '';
            if (data.warning) html += `<p class="text-danger small">⚠️ ${data.warning}</p>`;
            data.suggestions.forEach(s => {
                html += `<p class="text-muted small">💡 ${s}</p>`;
            });
            suggestionsDiv.innerHTML = html;
        }
    }, 500);
}

// --- Vault Operations ---
async function saveToVault() {
    const site = document.getElementById('vault-site').value;
    const username = document.getElementById('vault-user').value;
    const password = document.getElementById('vault-password').value;

    if (!site || !username || !password) {
        showToast('Please fill all fields', 'warning');
        return;
    }

    const response = await fetch('/api/vault/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ site, username, password })
    });

    const result = await response.json();
    if (result.success) {
        showToast('Password saved to vault!');
        if (window.location.pathname === '/vault') location.reload();
    } else {
        showToast('Error saving password', 'error');
    }
}

async function deleteFromVault(id) {
    if (!confirm('Are you sure you want to delete this entry?')) return;

    const response = await fetch(`/api/vault/delete/${id}`, {
        method: 'DELETE'
    });

    const result = await response.json();
    if (result.success) {
        document.getElementById(`entry-${id}`).remove();
        showToast('Deleted successfully');
    }
}

// --- Utility: Copy to Clipboard ---
function copyToClipboard(elementId) {
    const copyText = document.getElementById(elementId);
    copyText.select();
    document.execCommand("copy");
    showToast('Copied to clipboard!');
}

// --- Utility: Toast Notifications ---
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'primary' : 'danger'} border-0 show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Initialize tooltips/popovers
document.addEventListener('DOMContentLoaded', () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(t => new bootstrap.Tooltip(t));
});
