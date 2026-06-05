/* CipherVault API Middleware */
const BASE_URL = 'http://127.0.0.1:5000/api';

const ApiService = {
    async generatePassword(options) {
        try {
            const res = await fetch(`${BASE_URL}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(options)
            });
            return await res.json();
        } catch (e) { 
            console.error("Generate error:", e); 
            return { password: "ERROR_GENERATING" }; 
        }
    },

    async analyzePassword(password) {
        try {
            const res = await fetch(`${BASE_URL}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            return await res.json();
        } catch (e) { 
            console.error("Analyze error:", e); 
            return { score: 0, feedback: { warning: "Scan failed", suggestions: [] }, crack_times_display: { offline_fast_hashing_1e10_per_second: "0s" } }; 
        }
    },

    async savePassword(data) {
        try {
            const res = await fetch(`${BASE_URL}/passwords`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await res.json();
        } catch (e) { 
            console.error("Save error:", e); 
            return { success: false }; 
        }
    },

    async getPasswords() {
        try {
            const res = await fetch(`${BASE_URL}/passwords`);
            return await res.json();
        } catch (e) { 
            console.error("Fetch error:", e); 
            return []; 
        }
    },

    async deletePassword(id) {
        try {
            const res = await fetch(`${BASE_URL}/passwords/${id}`, {
                method: 'DELETE'
            });
            return await res.json();
        } catch (e) { 
            console.error("Delete error:", e); 
            return { success: false }; 
        }
    },

    async getStats() {
        try {
            const res = await fetch(`${BASE_URL}/stats`);
            return await res.json();
        } catch (e) { 
            console.error("Stats error:", e); 
            return { total_passwords: 0, avg_strength: 0, strength_dist: {}, categories: {} }; 
        }
    }
};
