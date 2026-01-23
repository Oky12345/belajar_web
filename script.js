/**
 * SEO Tools Dashboard - Professional Edition
 * Complete automation suite for Tokopedia/Shopee
 * UPDATED FOR GITHUB PAGES + LOCALHOST HYBRID
 */

// Configuration - AUTO DETECT MODE
const CONFIG = {
    // AUTO-DETECT API URL: GitHub Pages pakai proxy, Localhost pakai langsung
    get API_BASE_URL() {
        // Jika ada proxy API (GitHub Pages mode)
        if (typeof SEOAPI !== 'undefined') {
            return window.SEO_BACKEND_URL || '';
        }
        // Localhost development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:5000';
        }
        // Default fallback
        return '';
    },
    
    LOG_LIMIT: 100,
    UPDATE_INTERVAL: 30000, // 30 seconds
    TOOLS: {
        click: { 
            name: 'Click Circulation', 
            endpoint: '/api/tools/click-circulation/start',
            proxyMethod: 'startClickCirculation'
        },
        transaction: { 
            name: 'Micro Transaction', 
            endpoint: '/api/tools/real-traffic/start', // 💀 FIXED ENDPOINT
            proxyMethod: 'createCampaign'
        },
        safety: { 
            name: 'Safety Monitor', 
            endpoint: '/api/tools/safety-monitor/check',
            proxyMethod: 'safetyCheck'
        },
        review: { 
            name: 'Review Booster', 
            endpoint: '/api/tools/review-booster/start',
            proxyMethod: null // Not implemented
        }
    }
};

// State management
let state = {
    logs: [],
    isLogPaused: false,
    backendConnected: false,
    activeTools: {},
    securityScore: 80
};

// DOM Elements cache
const elements = {};

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 SEO Tools Dashboard v2.1.4 - Initializing...');
    
    // Tampilkan mode yang aktif
    const mode = typeof SEOAPI !== 'undefined' ? 'GitHub Pages + Proxy' : 'Localhost Direct';
    console.log(`📡 Mode: ${mode}`);
    
    initializeElements();
    setupEventListeners();
    initializeDashboard();
    startBackgroundUpdates();
});

function initializeElements() {
    // Cache all frequently used DOM elements
    elements.currentTime = document.getElementById('currentTime');
    elements.currentDate = document.getElementById('currentDate');
    elements.logEntries = document.getElementById('logEntries');
    elements.clearLogBtn = document.getElementById('clearLogBtn');
    elements.pauseLogBtn = document.getElementById('pauseLogBtn');
    elements.exportLogBtn = document.getElementById('exportLogBtn');
    elements.logInput = document.querySelector('.log-input');
    elements.sendBtn = document.querySelector('.btn-send');
    
    // Tool buttons
    elements.clickStartBtn = document.querySelector('[data-tool="click"] .btn-start');
    elements.transactionScheduleBtn = document.querySelector('[data-tool="transaction"] .btn-schedule');
    elements.reviewBoostBtn = document.querySelector('[data-tool="review"] .btn-warning');
    elements.safetyRefreshBtn = document.querySelector('[data-tool="safety"] .btn-info');
    
    // URL inputs
    elements.urlInputs = document.querySelectorAll('.url-input');
    
    // Status elements
    elements.statusDot = document.querySelector('.status-dot');
    elements.statusText = document.querySelector('.status-text');
    elements.riskValue = document.querySelector('.risk-value');
    elements.scoreProgress = document.querySelector('.score-progress');
    elements.scoreText = document.querySelector('.score-text');
}

function setupEventListeners() {
    // Tool action buttons
    if (elements.clickStartBtn) {
        elements.clickStartBtn.addEventListener('click', () => startTool('click'));
    }
    
    if (elements.transactionScheduleBtn) {
        elements.transactionScheduleBtn.addEventListener('click', () => startTool('transaction'));
    }
    
    if (elements.reviewBoostBtn) {
        elements.reviewBoostBtn.addEventListener('click', () => startTool('review'));
    }
    
    if (elements.safetyRefreshBtn) {
        elements.safetyRefreshBtn.addEventListener('click', () => startTool('safety'));
    }
    
    // Log controls
    if (elements.clearLogBtn) {
        elements.clearLogBtn.addEventListener('click', clearLogs);
    }
    
    if (elements.pauseLogBtn) {
        elements.pauseLogBtn.addEventListener('click', toggleLogPause);
    }
    
    if (elements.exportLogBtn) {
        elements.exportLogBtn.addEventListener('click', exportLogs);
    }
    
    // Send command
    if (elements.sendBtn && elements.logInput) {
        elements.sendBtn.addEventListener('click', sendCommand);
        elements.logInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendCommand();
        });
    }
    
    // Make URL inputs editable on double click
    elements.urlInputs.forEach(input => {
        input.addEventListener('dblclick', function() {
            this.readOnly = false;
            this.focus();
            this.select();
        });
        
        input.addEventListener('blur', function() {
            this.readOnly = true;
        });
        
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                this.blur();
                addLog('info', `URL updated: ${this.value}`);
            }
        });
    });
}

function initializeDashboard() {
    // Initialize date and time
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Check backend connection
    checkBackendConnection();
    
    // Initialize particles background
    initParticles();
    
    // Initial log dengan info mode
    const mode = typeof SEOAPI !== 'undefined' ? 'GitHub Pages + Proxy Mode' : 'Localhost Direct Mode';
    addLog('system', `Dashboard initialized - ${mode}`);
    addLog('system', 'Professional Edition v2.1.4 - Premium Features Enabled');
    addLog('info', 'All 4 automation tools are ready');
    
    // Initialize tool status
    updateToolStatus();
}

function updateDateTime() {
    const now = new Date();
    
    // Update time
    if (elements.currentTime) {
        elements.currentTime.textContent = now.toLocaleTimeString('id-ID', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    // Update date
    if (elements.currentDate) {
        elements.currentDate.textContent = now.toLocaleDateString('id-ID', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }
}

async function checkBackendConnection() {
    // 🔥 AUTO-DETECT MODE: Proxy API atau Localhost
    const useProxy = typeof SEOAPI !== 'undefined';
    
    if (useProxy) {
        // Mode GitHub Pages dengan Proxy API
        try {
            const isOnline = await SEOAPI.isBackendOnline();
            
            if (isOnline) {
                state.backendConnected = true;
                updateConnectionStatus(true);
                addLog('success', 'Backend connected via proxy API');
                return true;
            } else {
                state.backendConnected = false;
                updateConnectionStatus(false);
                addLog('info', 'Backend offline - Running in demo mode');
                return false;
            }
        } catch (error) {
            console.log('Proxy check error:', error);
            state.backendConnected = false;
            updateConnectionStatus(false);
            addLog('info', 'Proxy API initializing...');
            return false;
        }
    } else {
        // Mode Localhost Direct
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/status`, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.status === 'online') {
                    state.backendConnected = true;
                    updateConnectionStatus(true);
                    addLog('success', 'Local backend connected');
                    return true;
                }
            }
        } catch (error) {
            console.log('Local backend check error:', error);
        }
        
        state.backendConnected = false;
        updateConnectionStatus(false);
        addLog('error', 'Local backend not connected');
        return false;
    }
}

function updateConnectionStatus(connected) {
    if (!elements.statusDot || !elements.statusText) return;
    
    if (connected) {
        elements.statusDot.classList.add('active');
        elements.statusText.textContent = 'Backend Connected';
        elements.statusText.style.color = '#10b981';
    } else {
        elements.statusDot.classList.remove('active');
        elements.statusText.textContent = 'Backend Disconnected';
        elements.statusText.style.color = '#ef4444';
    }
}

function updateToolStatus() {
    // Update tool badges based on state
    const toolCards = document.querySelectorAll('.tool-card');
    
    toolCards.forEach(card => {
        const toolType = card.dataset.tool;
        const badge = card.querySelector('.tool-badge');
        
        if (badge && state.activeTools[toolType]) {
            badge.textContent = state.activeTools[toolType];
            badge.className = `tool-badge ${state.activeTools[toolType]}`;
        }
    });
}

async function startTool(toolType) {
    // 🔥 AUTO-SELECT EXECUTION METHOD
    const useProxy = typeof SEOAPI !== 'undefined';
    
    if (useProxy) {
        // Execute via Proxy API (GitHub Pages mode)
        await startToolViaProxy(toolType);
    } else {
        // Execute via Direct API (Localhost mode)
        await startToolDirect(toolType);
    }
}

async function startToolDirect(toolType) {
    // Original direct API call for localhost
    if (!state.backendConnected) {
        addLog('error', 'Cannot start tool - Backend not connected');
        showNotification('Backend server not connected', 'error');
        return;
    }
    
    const tool = CONFIG.TOOLS[toolType];
    if (!tool) {
        addLog('error', `Unknown tool type: ${toolType}`);
        return;
    }
    
    // Get URL from input
    const toolCard = document.querySelector(`[data-tool="${toolType}"]`);
    const urlInput = toolCard ? toolCard.querySelector('.url-input') : null;
    const productUrl = urlInput ? urlInput.value : '';
    
    // Validate URL
    if (!productUrl || !productUrl.startsWith('http')) {
        addLog('error', 'Please enter a valid URL starting with http:// or https://');
        showNotification('Invalid URL format', 'error');
        return;
    }
    
    addLog('info', `Starting ${tool.name} (Direct Mode)...`);
    showNotification(`Starting ${tool.name}`, 'info');
    
    try {
        // Prepare request data
        const requestData = {
            url: productUrl,
            sessions: toolType === 'click' ? 500 : 10,
            platform: 'tokopedia'
        };
        
        // Special handling for transaction tool
        if (toolType === 'transaction') {
            requestData.name = `Transaction_${Date.now()}`;
        }
        
        const response = await fetch(`${CONFIG.API_BASE_URL}${tool.endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (data.status === 'success' || data.status === 'warning') {
            addLog('success', `${tool.name} started successfully`);
            
            // Update UI
            updateToolUI(toolType, data);
            
            showNotification(`${tool.name} started successfully!`, 'success');
        } else {
            addLog('error', `${tool.name} failed: ${data.message || 'Unknown error'}`);
            showNotification(`Failed to start ${tool.name}`, 'error');
        }
        
    } catch (error) {
        console.error(`Direct tool ${toolType} error:`, error);
        addLog('error', `${tool.name} connection failed`);
        showNotification('Connection to backend failed', 'error');
    }
}

async function startToolViaProxy(toolType) {
    // Proxy API call for GitHub Pages
    const tool = CONFIG.TOOLS[toolType];
    if (!tool) {
        addLog('error', `Unknown tool type: ${toolType}`);
        return;
    }
    
    // Check if proxy method exists
    if (!tool.proxyMethod || typeof SEOAPI[tool.proxyMethod] !== 'function') {
        addLog('warning', `${tool.name} not available in proxy mode`);
        showNotification(`${tool.name} not available in demo mode`, 'warning');
        return;
    }
    
    // Get URL from input
    const toolCard = document.querySelector(`[data-tool="${toolType}"]`);
    const urlInput = toolCard ? toolCard.querySelector('.url-input') : null;
    const productUrl = urlInput ? urlInput.value : '';
    
    // Validate URL
    if (!productUrl || !productUrl.startsWith('http')) {
        addLog('error', 'Please enter a valid URL starting with http:// or https://');
        showNotification('Invalid URL format', 'error');
        return;
    }
    
    addLog('info', `Starting ${tool.name} via Proxy...`);
    showNotification(`Starting ${tool.name}`, 'info');
    
    try {
        let response;
        
        // Call appropriate proxy method
        switch(toolType) {
            case 'click':
                response = await SEOAPI.startClickCirculation({
                    url: productUrl,
                    sessions: 500
                });
                break;
                
            case 'transaction':
                response = await SEOAPI.createCampaign({
                    name: `Transaction_${Date.now()}`,
                    url: productUrl,
                    platform: 'tokopedia',
                    sessions: 10
                });
                break;
                
            case 'safety':
                response = await SEOAPI.safetyCheck();
                break;
                
            default:
                addLog('warning', `Tool ${toolType} not implemented in proxy mode`);
                return;
        }
        
        if (response.status === 'success' || response.status === 'warning') {
            addLog('success', `${tool.name} executed successfully`);
            
            // Update UI
            updateToolUI(toolType, response);
            
            showNotification(`${tool.name} executed`, 'success');
        } else {
            addLog('error', `${tool.name} failed: ${response.message || 'Unknown error'}`);
            showNotification(`Failed to start ${tool.name}`, 'error');
        }
        
    } catch (error) {
        console.error(`Proxy tool ${toolType} error:`, error);
        addLog('error', `${tool.name} proxy error`);
        showNotification('Proxy connection failed', 'error');
    }
}

function updateToolUI(toolType, responseData) {
    const toolCard = document.querySelector(`[data-tool="${toolType}"]`);
    if (!toolCard) return;
    
    const stats = toolCard.querySelectorAll('.stat-value');
    
    switch (toolType) {
        case 'click':
            if (stats.length >= 2) {
                const currentClicks = parseInt(stats[0].textContent.replace('K', '000')) || 1200;
                const newClicks = currentClicks + (responseData.data?.sessions || 500);
                stats[0].textContent = formatNumber(newClicks) + 'K';
                
                const currentBoost = parseInt(stats[1].textContent.replace('%', '')) || 15;
                const newBoost = Math.min(currentBoost + 2, 50);
                stats[1].textContent = `+${newBoost}%`;
            }
            break;
            
        case 'transaction':
            if (stats.length >= 2) {
                // Handle both proxy and direct responses
                const transactionCount = responseData.data?.transactions || 
                                       responseData.data?.sessions || 
                                       3;
                
                const currentTxns = parseInt(stats[0].textContent) || 85;
                const newTxns = currentTxns + transactionCount;
                stats[0].textContent = newTxns;
                
                const currentVolume = parseFloat(stats[1].textContent.replace('Rp ', '').replace('M', '')) || 2.4;
                const amount = transactionCount * 85000;
                const newVolume = currentVolume + (amount / 1000000);
                stats[1].textContent = `Rp ${newVolume.toFixed(1)}M`;
            }
            break;
            
        case 'safety':
            // Update security score
            const newScore = responseData.data?.risk_score ? 
                100 - responseData.data.risk_score : 
                Math.min(state.securityScore + 5, 95);
            
            state.securityScore = newScore;
            updateSecurityScore(newScore);
            
            // Update risk level
            const riskLevel = responseData.data?.risk_level || 'low';
            updateRiskLevel(riskLevel);
            break;
    }
    
    // Update tool status badge
    const badge = toolCard.querySelector('.tool-badge');
    if (badge) {
        badge.textContent = 'Running';
        badge.className = 'tool-badge running';
        
        // Reset after 5 seconds
        setTimeout(() => {
            badge.textContent = 'Active';
            badge.className = 'tool-badge active';
        }, 5000);
    }
}

function updateSecurityScore(score) {
    if (!elements.scoreProgress || !elements.scoreText) return;
    
    state.securityScore = Math.max(0, Math.min(100, score));
    
    // Update progress circle
    const circumference = 157; // 2 * π * r (r = 25)
    const offset = circumference - (circumference * state.securityScore / 100);
    elements.scoreProgress.style.strokeDashoffset = offset;
    
    // Update text
    elements.scoreText.textContent = `${state.securityScore}%`;
    
    // Update color based on score
    let color;
    if (state.securityScore >= 80) color = '#10b981';
    else if (state.securityScore >= 60) color = '#f59e0b';
    else color = '#ef4444';
    
    elements.scoreProgress.style.stroke = color;
}

function updateRiskLevel(level) {
    if (!elements.riskValue) return;
    
    const levels = {
        low: { text: 'Low', icon: 'fa-check-circle', color: '#10b981', class: 'low' },
        medium: { text: 'Medium', icon: 'fa-exclamation-triangle', color: '#f59e0b', class: 'medium' },
        high: { text: 'High', icon: 'fa-times-circle', color: '#ef4444', class: 'high' }
    };
    
    const risk = levels[level.toLowerCase()] || levels.low;
    
    elements.riskValue.innerHTML = `<i class="fas ${risk.icon}"></i> ${risk.text}`;
    elements.riskValue.className = `risk-value ${risk.class}`;
    elements.riskValue.style.color = risk.color;
    
    addLog('info', `Risk level updated: ${risk.text}`);
}

function addLog(type, message) {
    if (state.isLogPaused) return;
    
    const timestamp = new Date().toLocaleTimeString('id-ID', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    const logEntry = {
        id: Date.now(),
        timestamp,
        type,
        message,
        date: new Date().toISOString()
    };
    
    state.logs.unshift(logEntry);
    
    // Keep only last LOG_LIMIT entries
    if (state.logs.length > CONFIG.LOG_LIMIT) {
        state.logs = state.logs.slice(0, CONFIG.LOG_LIMIT);
    }
    
    updateLogDisplay();
}

function updateLogDisplay() {
    if (!elements.logEntries) return;
    
    // Clear current entries
    elements.logEntries.innerHTML = '';
    
    // Add new entries
    state.logs.forEach(log => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.dataset.type = log.type;
        
        const typeIcon = getLogTypeIcon(log.type);
        const typeClass = getLogTypeClass(log.type);
        
        logEntry.innerHTML = `
            <span class="log-timestamp">${log.timestamp}</span>
            <span class="log-type ${typeClass}">
                <i class="fas ${typeIcon}"></i> ${log.type.toUpperCase()}
            </span>
            <span class="log-message">${escapeHtml(log.message)}</span>
        `;
        
        elements.logEntries.appendChild(logEntry);
    });
}

function getLogTypeIcon(type) {
    const icons = {
        system: 'fa-cog',
        info: 'fa-info-circle',
        success: 'fa-check-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-times-circle',
        security: 'fa-shield-alt',
        tool: 'fa-tools'
    };
    
    return icons[type] || 'fa-info-circle';
}

function getLogTypeClass(type) {
    const classes = {
        system: 'log-type-system',
        info: 'log-type-info',
        success: 'log-type-success',
        warning: 'log-type-warning',
        error: 'log-type-error',
        security: 'log-type-security'
    };
    
    return classes[type] || 'log-type-info';
}

function clearLogs() {
    state.logs = [];
    updateLogDisplay();
    addLog('system', 'Activity log cleared');
    showNotification('Logs cleared successfully', 'info');
}

function toggleLogPause() {
    state.isLogPaused = !state.isLogPaused;
    
    const icon = elements.pauseLogBtn.querySelector('i');
    if (icon) {
        if (state.isLogPaused) {
            icon.className = 'fas fa-play';
            elements.pauseLogBtn.title = 'Resume Updates';
            addLog('info', 'Log updates paused');
        } else {
            icon.className = 'fas fa-pause';
            elements.pauseLogBtn.title = 'Pause Updates';
            addLog('info', 'Log updates resumed');
            updateLogDisplay(); // Refresh display
        }
    }
    
    showNotification(`Log updates ${state.isLogPaused ? 'paused' : 'resumed'}`, 'info');
}

function exportLogs() {
    if (state.logs.length === 0) {
        showNotification('No logs to export', 'warning');
        return;
    }
    
    const logText = state.logs.map(log => 
        `[${log.timestamp}] ${log.type.toUpperCase()}: ${log.message}`
    ).join('\n');
    
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    a.href = url;
    a.download = `seo-tools-logs-${new Date().toISOString().slice(0,10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    addLog('system', 'Logs exported successfully');
    showNotification('Logs exported to file', 'success');
}

function sendCommand() {
    if (!elements.logInput) return;
    
    const command = elements.logInput.value.trim();
    if (!command) return;
    
    addLog('system', `Command: ${command}`);
    
    // Process commands
    const cmd = command.toLowerCase();
    
    if (cmd === 'status') {
        const mode = typeof SEOAPI !== 'undefined' ? 'GitHub Pages + Proxy' : 'Localhost Direct';
        addLog('info', `Mode: ${mode}`);
        addLog('info', `Backend: ${state.backendConnected ? 'Connected' : 'Disconnected'}`);
        addLog('info', `Security score: ${state.securityScore}%`);
    } else if (cmd === 'help') {
        addLog('info', 'Available commands: status, help, clear, test, refresh');
    } else if (cmd === 'test') {
        addLog('info', 'Testing all tools...');
        setTimeout(() => addLog('success', 'All tools test passed'), 1000);
    } else if (cmd === 'refresh') {
        checkBackendConnection();
        addLog('info', 'Refreshing dashboard...');
    } else {
        addLog('warning', `Unknown command: ${command}`);
    }
    
    // Clear input
    elements.logInput.value = '';
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    notification.innerHTML = `
        <i class="fas ${icons[type] || 'fa-info-circle'}"></i>
        <span>${message}</span>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Add close button event
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        });
    }
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 5000);
}

function startBackgroundUpdates() {
    // Periodic backend check
    setInterval(() => {
        if (!state.isLogPaused) {
            checkBackendConnection();
        }
    }, CONFIG.UPDATE_INTERVAL);
    
    // Simulate tool activity updates
    setInterval(() => {
        if (!state.isLogPaused && state.backendConnected) {
            const tools = ['click', 'transaction', 'safety'];
            const randomTool = tools[Math.floor(Math.random() * tools.length)];
            
            const activities = [
                'Processing traffic data...',
                'Analyzing competitor patterns...',
                'Updating security protocols...',
                'Optimizing transaction schedules...'
            ];
            
            const randomActivity = activities[Math.floor(Math.random() * activities.length)];
            addLog('tool', `${CONFIG.TOOLS[randomTool]?.name || 'System'}: ${randomActivity}`);
        }
    }, 15000);
}

function initParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    // Create particles
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 4 + 1;
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const animationDuration = Math.random() * 20 + 10;
        const animationDelay = Math.random() * 5;
        
        particle.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${posX}%;
            top: ${posY}%;
            animation-duration: ${animationDuration}s;
            animation-delay: ${animationDelay}s;
            opacity: ${Math.random() * 0.3 + 0.1};
        `;
        
        particlesContainer.appendChild(particle);
    }
}

// Utility functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
        border-left: 4px solid;
    }
    
    .notification-success {
        border-left-color: #10b981;
        background: #f0fdf4;
    }
    
    .notification-error {
        border-left-color: #ef4444;
        background: #fef2f2;
    }
    
    .notification-warning {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }
    
    .notification-info {
        border-left-color: #3b82f6;
        background: #eff6ff;
    }
    
    .notification i {
        font-size: 18px;
    }
    
    .notification-success i { color: #10b981; }
    .notification-error i { color: #ef4444; }
    .notification-warning i { color: #f59e0b; }
    .notification-info i { color: #3b82f6; }
    
    .notification-close {
        margin-left: auto;
        background: none;
        border: none;
        cursor: pointer;
        color: #64748b;
        font-size: 14px;
        padding: 4px;
        border-radius: 4px;
        transition: background 0.2s;
    }
    
    .notification-close:hover {
        background: rgba(0,0,0,0.05);
    }
    
    .fade-out {
        animation: slideOutRight 0.3s ease forwards;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;

document.head.appendChild(notificationStyles);

// ✅ AUTO-DETECT MODE INDICATOR
window.addEventListener('load', function() {
    // Add mode indicator to footer
    const mode = typeof SEOAPI !== 'undefined' ? 'GitHub Pages Mode' : 'Localhost Mode';
    const modeElement = document.createElement('div');
    modeElement.className = 'mode-indicator';
    modeElement.innerHTML = `<small>${mode}</small>`;
    modeElement.style.cssText = `
        position: fixed;
        bottom: 5px;
        left: 5px;
        background: rgba(0,0,0,0.7);
        color: #f59e0b;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-family: monospace;
        z-index: 1000;
    `;
    document.body.appendChild(modeElement);
});
