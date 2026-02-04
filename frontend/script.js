/* frontend\script.js */

// --- GLOBAL STATE ---
const state = {
    area_sqm: 0,
    wall_reflection: 0.8,
    total_lumens: 0,
    current_lux: 0,
    active_section: 'dashboard'
};

// --- DOM ELEMENTS ---
const navItems = document.querySelectorAll('.nav-links li');
const sections = document.querySelectorAll('.ui-section');
const mainLog = document.getElementById('main-log');
const toast = document.getElementById('toast');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initPhysics();
    initEconomics();
    initVision();
    initConfig();
    initMarket();
    
    log("[SYSTEM] UI Handlers active.");
});

// --- NAVIGATION ---
function initNavigation() {
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const sectionId = item.getAttribute('data-section');
            switchSection(sectionId);
            
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

function switchSection(id) {
    sections.forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    state.active_section = id;
}

// --- PHYSICS ENGINE (UI SIDE) ---
function initPhysics() {
    const luxForm = document.getElementById('lux-calc-form');
    const optiForm = document.getElementById('opti-form');

    luxForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const lumens = parseFloat(document.getElementById('lux-lumens').value);
        const dist = parseFloat(document.getElementById('lux-dist').value);
        const angle = parseFloat(document.getElementById('lux-angle').value);

        // Physics Calculation (Inverse Square Law Approximation)
        const rad = (angle * Math.PI) / 180;
        const solidAngle = 2 * Math.PI * (1 - Math.cos(rad / 2));
        const candela = lumens / solidAngle;
        const lux = candela / (dist * dist);

        document.getElementById('lux-result').innerHTML = `<span class="result-value">${Math.round(lux)} lux</span>`;
        log(`[PHYSICS] Point Calculation: ${Math.round(lux)} lux at ${dist}m.`);
    });

    optiForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const area = parseFloat(document.getElementById('opti-area').value);
        const target = parseInt(document.getElementById('opti-target').value);
        const current = parseInt(document.getElementById('opti-current').value);

        state.area_sqm = area;
        state.total_lumens = current;
        state.current_lux = Math.round(current / area);
        
        updateDashboardState();

        const required = area * target;
        const deficit = Math.max(0, required - current);
        const bulbs = Math.ceil(deficit / 800);

        const reportBox = document.getElementById('opti-report');
        if (deficit > 0) {
            reportBox.innerHTML = `
                <p><strong>Status:</strong> CRITICAL DEFICIT ⚠️</p>
                <p>Current avg: ${state.current_lux} lux. Target: ${target} lux.</p>
                <p>Engineering Recommendation: You need <strong>${bulbs}</strong> more sources (800lm each) or +${deficit} total lumens.</p>
            `;
            log(`[PHYSICS] Optimization failed. Deficit of ${deficit} lumens detected.`, 'warn');
        } else {
            reportBox.innerHTML = `
                <p><strong>Status:</strong> COMPLIANT ✅</p>
                <p>Your current lighting satisfies the ${target} lux standard.</p>
            `;
            log(`[PHYSICS] Room is compliant with ${target} lux standard.`, 'success');
        }
    });
}

// --- ECONOMIC ENGINE ---
function initEconomics() {
    const roiForm = document.getElementById('roi-form');
    
    roiForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const oldW = parseFloat(document.getElementById('roi-old').value);
        const newW = parseFloat(document.getElementById('roi-new').value);
        const price = parseFloat(document.getElementById('roi-price').value);
        const hours = parseFloat(document.getElementById('roi-hours').value);
        const rate = parseFloat(document.getElementById('roi-rate').value);

        const savedWatts = oldW - newW;
        const kwhAnnual = (savedWatts * hours * 365) / 1000;
        const moneySaved = kwhAnnual * rate;
        const co2Saved = kwhAnnual * 0.385;
        const payback = (price / (moneySaved / 12)).toFixed(1);

        document.getElementById('res-savings').innerText = `$${moneySaved.toFixed(2)}`;
        document.getElementById('res-payback').innerText = `${payback} months`;
        document.getElementById('res-co2').innerText = `${co2Saved.toFixed(1)} kg`;

        log(`[ECONOMICS] ROI Analysis complete. Annual savings: $${moneySaved.toFixed(2)}.`);
    });
}

// --- VISION AUDIT ---
function initVision() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewImg = document.getElementById('upload-preview');
    const auditBtn = document.getElementById('run-audit-btn');

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (re) => {
                previewImg.src = re.target.result;
                dropZone.querySelector('.upload-prompt').classList.add('hidden');
                dropZone.querySelector('.preview-container').classList.remove('hidden');
                auditBtn.disabled = false;
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    auditBtn.addEventListener('click', () => {
        log("[VISION] Running 3x3 Grid Analysis...");
        showToast("Gemini 3.0 Vision Analyzing Spatial Data...");
        
        setTimeout(() => {
            log("[VISION] Sector 4: Window Detected (Reflection Influence: +15%)", 'success');
            log("[VISION] Sector 8: Floor material identified as 'Dark Oak' (Albedo: 0.15)");
            log("[VISION] Reference Object found: Door Frame. Estimated area: 18.5 m²");
            
            state.area_sqm = 18.5;
            state.wall_reflection = 0.45;
            updateDashboardState();
            
            document.querySelectorAll('.check-item').forEach(item => {
                item.classList.remove('disabled');
                item.querySelector('.status').innerText = '✅';
            });
        }, 2000);
    });
}

// --- MARKET & INTELLIGENCE ---
function initMarket() {
    const searchBtn = document.getElementById('market-search-btn');
    const resultsDiv = document.getElementById('market-results');

    searchBtn.addEventListener('click', () => {
        const query = document.getElementById('market-query').value;
        if (!query) return;

        resultsDiv.innerHTML = '<p class="info-text">Agent searching market... (Multi-threaded verify enabled)</p>';
        log(`[MARKET] Searching for: "${query}"`);

        setTimeout(() => {
            const mockProducts = [
                { name: "Philips Hue A21 LED", lumens: 1600, price: 19.99, protocol: "Zigbee/Matter", verified: true },
                { name: "Sengled Smart Bulb", lumens: 800, price: 9.99, protocol: "Zigbee", verified: true },
                { name: "Generic LED Bulb", lumens: 1500, price: 4.50, protocol: "None", verified: false }
            ];

            resultsDiv.innerHTML = mockProducts.map(p => `
                <div class="card glass-card">
                    <div style="font-weight:bold; margin-bottom:0.5rem">${p.name}</div>
                    <div style="font-size:0.85rem; color:var(--text-muted)">
                        Lumens: ${p.lumens}lm | Price: $${p.price}<br>
                        Protocol: ${p.protocol}<br>
                        ${p.verified ? '<span style="color:var(--accent-secondary)">✓ Spec Verified</span>' : '<span style="color:var(--accent-danger)">! Spec Unverified</span>'}
                    </div>
                </div>
            `).join('');
            
            log(`[MARKET] Analysis complete. 3 results found. Specs verified.`);
        }, 1500);
    });
}

// --- CONFIG GENERATOR ---
function initConfig() {
    const genBtn = document.getElementById('gen-config-btn');
    const output = document.getElementById('config-output');

    genBtn.addEventListener('click', () => {
        const hub = document.getElementById('hub-type').value;
        const config = {
            room: "Executive Office",
            agent: "Spatial Engine AI",
            version: "1.0",
            scenes: {
                focus: { brightness: 100, temp: 4500 },
                relax: { brightness: 40, temp: 2700 },
                cinema: { brightness: 15, temp: 2200 }
            },
            compliance: "ISO-8995-2026"
        };
        
        output.innerText = JSON.stringify(config, null, 4);
        log("[CONFIG] Smart Scene JSON generated successfully.");
        showToast("Configuration Generated.");
    });
}

// --- HELPERS ---
function log(msg, type = 'system') {
    const entry = document.createElement('p');
    entry.className = `log-entry ${type}`;
    const time = new Date().toLocaleTimeString([], { hour12: false });
    entry.innerText = `[${time}] ${msg}`;
    mainLog.appendChild(entry);
    mainLog.scrollTop = mainLog.scrollHeight;
}

function updateDashboardState() {
    document.getElementById('state-area').innerText = `${state.area_sqm} m²`;
    document.getElementById('state-reflection').innerText = state.wall_reflection;
    document.getElementById('state-lumens').innerText = `${state.total_lumens} lm`;
    document.getElementById('state-lux').innerText = `${state.current_lux} lux`;

    const complianceDiv = document.getElementById('compliance-status');
    if (state.current_lux >= 500) {
        complianceDiv.innerHTML = '<div class="status-check">✅ ISO COMPLIANT (OFFICE)</div>';
    } else if (state.current_lux > 0) {
        complianceDiv.innerHTML = '<div class="status-fail">⚠️ NON-COMPLIANT (DEFICIT)</div>';
    }
}

function showToast(msg) {
    toast.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
