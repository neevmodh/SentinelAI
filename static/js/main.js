let threatChart = null;
let radarChart = null;
let stats = {
    total: 0,
    threats: 0,
    safe: 0
};

// Load stats from localStorage
function loadStats() {
    const saved = localStorage.getItem('sentinelStats');
    if (saved) {
        stats = JSON.parse(saved);
        updateStatsDisplay();
    }
}

function saveStats() {
    localStorage.setItem('sentinelStats', JSON.stringify(stats));
}

function updateStatsDisplay() {
    document.getElementById('totalScans').textContent = stats.total;
    document.getElementById('threatsDetected').textContent = stats.threats;
    document.getElementById('safeMsgs').textContent = stats.safe;
}

function createThreatChart(score) {
    const ctx = document.getElementById('threatChart').getContext('2d');
    
    if (threatChart) {
        threatChart.destroy();
    }
    
    let color = '#00ff88';
    if (score >= 70) color = '#ff3232';
    else if (score >= 30) color = '#ffaa00';
    
    threatChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [color, 'rgba(42, 63, 95, 0.3)'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

function createRadarChart(cognitiveScores) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    if (radarChart) {
        radarChart.destroy();
    }
    
    const data = {
        labels: [
            'Fear',
            'Urgency',
            'Authority',
            'Financial',
            'Reward',
            'Scarcity',
            'Guilt',
            'Trust Exploit'
        ],
        datasets: [{
            label: 'Manipulation Score',
            data: [
                cognitiveScores.fear_score,
                cognitiveScores.urgency_score,
                cognitiveScores.authority_score,
                cognitiveScores.financial_score,
                cognitiveScores.reward_score,
                cognitiveScores.scarcity_score,
                cognitiveScores.guilt_score,
                cognitiveScores.trust_score
            ],
            backgroundColor: 'rgba(0, 204, 255, 0.2)',
            borderColor: '#00ccff',
            borderWidth: 2,
            pointBackgroundColor: '#00ccff',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#00ccff',
            pointRadius: 4,
            pointHoverRadius: 6
        }]
    };
    
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: '#8b9dc3',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(139, 157, 195, 0.2)'
                    },
                    pointLabels: {
                        color: '#e0e0e0',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(10, 14, 39, 0.9)',
                    titleColor: '#00ccff',
                    bodyColor: '#e0e0e0',
                    borderColor: '#00ccff',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return context.parsed.r.toFixed(1) + '/100';
                        }
                    }
                }
            }
        }
    });
}

function updateRiskMeter(riskLevel, riskColor, probability) {
    const riskMeterFill = document.getElementById('riskMeterFill');
    const riskMeterText = document.getElementById('riskMeterText');
    
    // Animate the fill
    riskMeterFill.style.width = probability + '%';
    riskMeterFill.style.background = `linear-gradient(90deg, ${riskColor}, ${riskColor}dd)`;
    
    // Update text
    riskMeterText.textContent = `${riskLevel} RISK - ${probability.toFixed(1)}%`;
    riskMeterText.style.color = riskColor;
}

function displayFeatureImportance(features) {
    const featureList = document.getElementById('featureList');
    featureList.innerHTML = '';
    
    if (features.length === 0) {
        const li = document.createElement('li');
        li.style.borderLeftColor = '#00ff88';
        li.innerHTML = `
            <span class="feature-name">No significant threat indicators detected</span>
            <span class="feature-score" style="background: rgba(0, 255, 136, 0.1); color: #00ff88;">0</span>
        `;
        featureList.appendChild(li);
        return;
    }
    
    features.forEach(feature => {
        const li = document.createElement('li');
        li.className = `impact-${feature.impact}`;
        
        let scoreColor = '#00ff88';
        if (feature.score >= 70) scoreColor = '#ff3232';
        else if (feature.score >= 30) scoreColor = '#ffaa00';
        
        li.innerHTML = `
            <span class="feature-name">${feature.name}</span>
            <span class="feature-score" style="background: rgba(${scoreColor === '#ff3232' ? '255, 50, 50' : scoreColor === '#ffaa00' ? '255, 170, 0' : '0, 255, 136'}, 0.1); color: ${scoreColor};">${feature.score.toFixed(0)}</span>
        `;
        
        featureList.appendChild(li);
    });
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const threatStatus = document.getElementById('threatStatus');
    const scoreValue = document.getElementById('scoreValue');
    const feedbackList = document.getElementById('feedbackList');
    const recommendationsList = document.getElementById('recommendationsList');
    
    resultsSection.classList.remove('hidden');
    
    // Update threat status based on threat level
    const threatLevel = data.threat_level;
    let statusText = '';
    let statusClass = 'status';
    
    if (threatLevel === 'DANGER') {
        statusText = '🚨 DANGER';
        statusClass = 'status danger';
        stats.threats++;
    } else if (threatLevel === 'WARNING') {
        statusText = '⚠️ WARNING';
        statusClass = 'status warning';
        stats.threats++;
    } else {
        statusText = '✓ SAFE';
        statusClass = 'status safe';
        stats.safe++;
    }
    
    threatStatus.textContent = statusText;
    threatStatus.className = statusClass;
    
    stats.total++;
    saveStats();
    updateStatsDisplay();
    
    // Update score display
    const probability = data.phishing_probability;
    const confidence = data.confidence_score;
    
    scoreValue.innerHTML = `
        <div style="font-size: 28px; margin-bottom: 5px;">${probability.toFixed(1)}%</div>
        <div style="font-size: 14px; color: #8b9dc3;">Phishing Risk</div>
        <div style="font-size: 12px; color: #8b9dc3; margin-top: 8px;">Confidence: ${confidence.toFixed(1)}%</div>
    `;
    
    let scoreColor = '#00ff88';
    if (probability >= 70) scoreColor = '#ff3232';
    else if (probability >= 30) scoreColor = '#ffaa00';
    
    scoreValue.style.color = scoreColor;
    
    // Create charts
    createThreatChart(probability);
    createRadarChart(data.cognitive_scores);
    
    // Update risk meter
    updateRiskMeter(data.risk_level, data.risk_color, probability);
    
    // Display cognitive score
    const cognitiveScoreValue = document.getElementById('cognitiveScoreValue');
    const overallScore = data.cognitive_scores.overall_cognitive_score;
    
    let cognitiveColor = '#00ff88';
    if (overallScore >= 70) {
        cognitiveColor = '#ff3232';
    } else if (overallScore >= 30) {
        cognitiveColor = '#ffaa00';
    }
    
    cognitiveScoreValue.textContent = overallScore.toFixed(1);
    cognitiveScoreValue.style.color = cognitiveColor;
    cognitiveScoreValue.style.textShadow = `0 0 30px ${cognitiveColor}`;
    
    // Display feature importance
    displayFeatureImportance(data.feature_importance);
    
    // Display security insight
    if (data.security_insight) {
        displaySecurityInsight(data.security_insight);
    }
    
    // Display suspicious words analysis
    displaySuspiciousWords(data.suspicious_words);
    
    // Display teach-back guidance
    const teachbackSection = document.getElementById('teachbackSection');
    if (data.teachback) {
        teachbackSection.classList.remove('hidden');
        document.getElementById('whyDangerous').textContent = data.teachback.why_dangerous;
        document.getElementById('attackerGoal').textContent = data.teachback.attacker_goal;
        document.getElementById('whatToDo').textContent = data.teachback.what_to_do;
        document.getElementById('safetyTip').textContent = data.teachback.safety_tip;
    } else {
        teachbackSection.classList.add('hidden');
    }
    
    // Display feedback
    feedbackList.innerHTML = '';
    data.feedback.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        feedbackList.appendChild(li);
    });
    
    // Display recommendations based on threat level
    recommendationsList.innerHTML = '';
    let recommendations = [];
    
    if (threatLevel === 'DANGER') {
        recommendations = [
            '🛑 DO NOT click any links in this message',
            '🛑 DO NOT provide any personal or financial information',
            '📞 Contact the organization directly using official contact info',
            '🚨 Report this message to your IT security team immediately',
            '🗑️ Delete the message after reporting'
        ];
    } else if (threatLevel === 'WARNING') {
        recommendations = [
            '⚠️ Exercise caution with this message',
            '🔍 Verify sender identity through official channels',
            '🔗 Do not click links unless verified',
            '📧 Check sender email address carefully',
            '💭 If unsure, contact the organization directly'
        ];
    } else {
        recommendations = [
            '✓ Message appears legitimate, but stay vigilant',
            '🔍 Always verify sender if requesting sensitive actions',
            '📝 Check for spelling and grammar errors',
            '🔗 Hover over links before clicking',
            '🤔 When in doubt, verify through official channels'
        ];
    }
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displaySecurityInsight(insight) {
    document.getElementById('insightIcon').textContent = insight.icon;
    document.getElementById('insightTitle').textContent = insight.title;
    document.getElementById('insightTip').textContent = insight.tip;
}

function displaySuspiciousWords(suspiciousWords) {
    const explainableSection = document.getElementById('explainableSection');
    const suspiciousWordsList = document.getElementById('suspiciousWordsList');
    
    if (!suspiciousWords || suspiciousWords.length === 0) {
        explainableSection.classList.add('hidden');
        return;
    }
    
    explainableSection.classList.remove('hidden');
    suspiciousWordsList.innerHTML = '';
    
    suspiciousWords.forEach(category => {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = `word-category weight-${category.weight.toLowerCase()}`;
        
        const header = document.createElement('div');
        header.className = 'word-category-header';
        
        const categoryName = document.createElement('div');
        categoryName.className = 'category-name';
        categoryName.textContent = category.category;
        
        const categoryWeight = document.createElement('span');
        categoryWeight.className = `category-weight ${category.weight.toLowerCase()}`;
        categoryWeight.textContent = `${category.weight} Impact`;
        
        header.appendChild(categoryName);
        header.appendChild(categoryWeight);
        
        const wordsDiv = document.createElement('div');
        wordsDiv.className = 'detected-words';
        
        category.words.forEach(word => {
            const wordBadge = document.createElement('span');
            wordBadge.className = 'word-badge';
            wordBadge.textContent = `"${word}"`;
            wordsDiv.appendChild(wordBadge);
        });
        
        const explanation = document.createElement('div');
        explanation.className = 'word-explanation';
        explanation.textContent = category.explanation;
        
        categoryDiv.appendChild(header);
        categoryDiv.appendChild(wordsDiv);
        categoryDiv.appendChild(explanation);
        
        suspiciousWordsList.appendChild(categoryDiv);
    });
}

async function loadNewInsight() {
    try {
        const response = await fetch('/get-insight');
        const insight = await response.json();
        displaySecurityInsight(insight);
    } catch (error) {
        console.error('Error loading insight:', error);
    }
}

async function analyzeMessage() {
    const messageInput = document.getElementById('messageInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const text = messageInput.value.trim();
    
    if (!text) {
        alert('Please enter a message to analyze');
        return;
    }
    
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert(data.error || 'Analysis failed');
        }
    } catch (error) {
        alert('Error connecting to server: ' + error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Threat';
    }
}

// Event listeners
document.getElementById('analyzeBtn').addEventListener('click', analyzeMessage);

document.getElementById('newInsightBtn').addEventListener('click', loadNewInsight);

document.getElementById('demoModeBtn').addEventListener('click', toggleDemoMode);

// Demo example buttons
document.querySelectorAll('.demo-example-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const type = this.getAttribute('data-type');
        await loadDemoExample(type);
    });
});

document.getElementById('messageInput').addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        analyzeMessage();
    }
});

// Load stats and initial insight on page load
loadStats();
loadNewInsight();

function toggleDemoMode() {
    const demoExamples = document.getElementById('demoExamples');
    const demoBtn = document.getElementById('demoModeBtn');
    
    if (demoExamples.classList.contains('hidden')) {
        demoExamples.classList.remove('hidden');
        demoBtn.classList.add('active');
    } else {
        demoExamples.classList.add('hidden');
        demoBtn.classList.remove('active');
    }
}

async function loadDemoExample(type) {
    try {
        const response = await fetch(`/get-demo-example/${type}`);
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('messageInput').value = data.text;
            
            // Show a notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0, 204, 255, 0.9);
                color: #0d1117;
                padding: 15px 25px;
                border-radius: 8px;
                font-weight: bold;
                z-index: 1000;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = `Loaded: ${data.description}`;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    } catch (error) {
        console.error('Error loading demo example:', error);
    }
}
