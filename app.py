from flask import Flask, render_template, request, jsonify
import pickle
import os
import re
import random

app = Flask(__name__)

# Digital Hygiene Tips
SECURITY_INSIGHTS = [
    {
        'title': 'Urgency is a Red Flag',
        'tip': 'Never trust urgent financial threats. Legitimate organizations give you time to respond and won\'t pressure you with "act now" language.',
        'icon': '⏰'
    },
    {
        'title': 'Domain Verification',
        'tip': 'Check domain spelling carefully. Phishers use look-alike domains like "paypa1.com" instead of "paypal.com". Always verify the exact URL.',
        'icon': '🔍'
    },
    {
        'title': 'Password Protection',
        'tip': 'Institutions never ask for passwords via email. No bank, service, or company will ever request your password through email or text.',
        'icon': '🔐'
    },
    {
        'title': 'Link Inspection',
        'tip': 'Hover over links before clicking to see the real destination. If the URL looks suspicious or doesn\'t match the claimed sender, don\'t click.',
        'icon': '🔗'
    },
    {
        'title': 'Two-Factor Authentication',
        'tip': 'Enable 2FA on all important accounts. Even if someone gets your password, they can\'t access your account without the second factor.',
        'icon': '🛡️'
    },
    {
        'title': 'Verify the Sender',
        'tip': 'Contact organizations directly using official contact info from their website, not from the suspicious message. Never use contact details provided in the email.',
        'icon': '📞'
    },
    {
        'title': 'Grammar and Spelling',
        'tip': 'Poor grammar and spelling errors are common in phishing emails. Professional organizations proofread their communications.',
        'icon': '✍️'
    },
    {
        'title': 'Attachment Caution',
        'tip': 'Never open unexpected attachments, especially from unknown senders. They may contain malware or ransomware.',
        'icon': '📎'
    },
    {
        'title': 'Too Good to Be True',
        'tip': 'If an offer seems too good to be true, it probably is. Free prizes, unexpected inheritances, and lottery wins are classic scam tactics.',
        'icon': '🎁'
    },
    {
        'title': 'Personal Information',
        'tip': 'Never share personal information like SSN, account numbers, or passwords through email. Legitimate companies already have this information.',
        'icon': '🚫'
    },
    {
        'title': 'Email Address Verification',
        'tip': 'Check the sender\'s full email address, not just the display name. Scammers can fake display names but the actual email address reveals the truth.',
        'icon': '📧'
    },
    {
        'title': 'Trust Your Instincts',
        'tip': 'If something feels off, it probably is. Take time to verify before taking any action. It\'s better to be cautious than compromised.',
        'icon': '💭'
    },
    {
        'title': 'Secure Connections',
        'tip': 'Only enter sensitive information on websites with HTTPS (look for the padlock icon). HTTP sites are not secure.',
        'icon': '🔒'
    },
    {
        'title': 'Regular Updates',
        'tip': 'Keep your software, browser, and operating system updated. Security patches protect you from known vulnerabilities.',
        'icon': '🔄'
    },
    {
        'title': 'Password Managers',
        'tip': 'Use a password manager to create and store unique, strong passwords for each account. Never reuse passwords across sites.',
        'icon': '🗝️'
    }
]

def get_random_security_insight():
    """Get a random security insight for educational purposes"""
    return random.choice(SECURITY_INSIGHTS)

# Cognitive manipulation detection keywords
MANIPULATION_KEYWORDS = {
    'fear': {
        'keywords': ['suspended', 'blocked', 'locked', 'breach', 'hacked', 'compromised', 
                    'unauthorized', 'suspicious activity', 'security alert', 'fraud', 
                    'stolen', 'virus', 'malware', 'threat', 'danger', 'risk'],
        'weight': 1.5
    },
    'urgency': {
        'keywords': ['urgent', 'immediate', 'act now', 'expires', 'limited time', 
                    'hurry', 'quickly', 'asap', 'within 24 hours', 'today only',
                    'last chance', 'don\'t wait', 'time sensitive', 'expiring'],
        'weight': 1.3
    },
    'authority': {
        'keywords': ['verify your account', 'confirm your identity', 'update your information',
                    'security team', 'customer service', 'support team', 'administrator',
                    'official', 'department', 'compliance', 'legal', 'government',
                    'irs', 'bank', 'paypal', 'amazon', 'microsoft'],
        'weight': 1.4
    },
    'financial': {
        'keywords': ['payment', 'refund', 'overdue', 'debt', 'owe', 'credit card',
                    'bank account', 'transfer', 'invoice', 'billing', 'charge',
                    'transaction', 'money', 'fee', 'penalty', 'fine'],
        'weight': 1.6
    },
    'reward': {
        'keywords': ['won', 'winner', 'prize', 'congratulations', 'claim', 'free',
                    'gift', 'bonus', 'reward', 'selected', 'lucky', 'exclusive',
                    'special offer', 'discount', 'cash', 'inheritance'],
        'weight': 1.2
    },
    'scarcity': {
        'keywords': ['limited', 'only', 'few left', 'running out', 'while supplies last',
                    'exclusive', 'rare', 'one time', 'never again', 'final'],
        'weight': 1.1
    },
    'guilt': {
        'keywords': ['disappointed', 'failed', 'missed', 'neglected', 'ignored',
                    'haven\'t responded', 'final notice', 'last warning', 'overdue'],
        'weight': 1.0
    },
    'trust': {
        'keywords': ['trusted', 'secure', 'verified', 'guaranteed', 'protected',
                    'safe', 'confidential', 'privacy', 'legitimate', 'authentic'],
        'weight': 0.8
    }
}

def calculate_risk_level(phishing_probability):
    """Calculate risk level and color based on probability"""
    if phishing_probability < 30:
        return 'LOW', '#00ff88'
    elif phishing_probability < 70:
        return 'MEDIUM', '#ffaa00'
    else:
        return 'HIGH', '#ff3232'

def get_feature_importance(text, cognitive_scores, phishing_probability):
    """Identify and rank the most important threat indicators"""
    features = []
    
    # Add cognitive manipulation scores as features
    if cognitive_scores['fear_score'] > 20:
        features.append({
            'name': 'Fear-Based Language',
            'score': cognitive_scores['fear_score'],
            'impact': 'high' if cognitive_scores['fear_score'] > 50 else 'medium'
        })
    
    if cognitive_scores['urgency_score'] > 20:
        features.append({
            'name': 'Urgency Pressure',
            'score': cognitive_scores['urgency_score'],
            'impact': 'high' if cognitive_scores['urgency_score'] > 50 else 'medium'
        })
    
    if cognitive_scores['authority_score'] > 20:
        features.append({
            'name': 'Authority Impersonation',
            'score': cognitive_scores['authority_score'],
            'impact': 'high' if cognitive_scores['authority_score'] > 50 else 'medium'
        })
    
    if cognitive_scores['financial_score'] > 20:
        features.append({
            'name': 'Financial Threats',
            'score': cognitive_scores['financial_score'],
            'impact': 'high' if cognitive_scores['financial_score'] > 50 else 'medium'
        })
    
    if cognitive_scores['reward_score'] > 20:
        features.append({
            'name': 'Reward Bait',
            'score': cognitive_scores['reward_score'],
            'impact': 'medium' if cognitive_scores['reward_score'] > 50 else 'low'
        })
    
    if cognitive_scores['scarcity_score'] > 20:
        features.append({
            'name': 'Scarcity Tactics',
            'score': cognitive_scores['scarcity_score'],
            'impact': 'medium' if cognitive_scores['scarcity_score'] > 50 else 'low'
        })
    
    if cognitive_scores['guilt_score'] > 20:
        features.append({
            'name': 'Guilt Manipulation',
            'score': cognitive_scores['guilt_score'],
            'impact': 'medium' if cognitive_scores['guilt_score'] > 50 else 'low'
        })
    
    if cognitive_scores['trust_score'] > 30:
        features.append({
            'name': 'Trust Exploitation',
            'score': cognitive_scores['trust_score'],
            'impact': 'medium' if cognitive_scores['trust_score'] > 50 else 'low'
        })
    
    # Check for specific threat indicators
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['click', 'link', 'here', 'download']):
        features.append({
            'name': 'Suspicious Links',
            'score': 75,
            'impact': 'high'
        })
    
    if any(word in text_lower for word in ['password', 'credit card', 'ssn', 'account number']):
        features.append({
            'name': 'Requests Sensitive Data',
            'score': 85,
            'impact': 'high'
        })
    
    # Sort by score (descending)
    features.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top 5 features
    return features[:5]

def detect_suspicious_words(text):
    """Detect and explain suspicious words/phrases in the text"""
    text_lower = text.lower()
    detected_words = []
    
    # Define suspicious word categories with explanations
    word_categories = {
        'urgency': {
            'keywords': ['urgent', 'immediately', 'act now', 'expires', 'limited time', 
                        'hurry', 'quickly', 'asap', 'within 24 hours', 'time sensitive'],
            'explanation': 'These phrases create artificial urgency to pressure you into acting without thinking.',
            'weight': 'High'
        },
        'fear': {
            'keywords': ['suspended', 'blocked', 'locked', 'breach', 'compromised', 
                        'unauthorized', 'suspicious activity', 'fraud', 'security alert'],
            'explanation': 'These words trigger fear and panic to bypass your rational decision-making.',
            'weight': 'High'
        },
        'verification': {
            'keywords': ['verify now', 'confirm your', 'update your', 'validate', 
                        'reactivate', 'restore access'],
            'explanation': 'Legitimate companies rarely ask you to verify information via email links.',
            'weight': 'High'
        },
        'action': {
            'keywords': ['click here', 'click now', 'download', 'open attachment', 
                        'follow this link', 'tap here'],
            'explanation': 'These phrases push you to click malicious links or download harmful files.',
            'weight': 'High'
        },
        'financial': {
            'keywords': ['payment', 'refund', 'overdue', 'debt', 'owe', 'invoice',
                        'billing', 'transaction failed', 'account charged'],
            'explanation': 'Financial pressure tactics are designed to make you act impulsively.',
            'weight': 'High'
        },
        'reward': {
            'keywords': ['won', 'winner', 'prize', 'congratulations', 'claim', 
                        'free gift', 'selected', 'lucky'],
            'explanation': 'Unrealistic rewards are bait to get your personal information or money.',
            'weight': 'Medium'
        },
        'authority': {
            'keywords': ['security team', 'customer service', 'support team', 'administrator',
                        'official notice', 'compliance', 'legal department'],
            'explanation': 'Attackers impersonate authority figures to appear legitimate and trustworthy.',
            'weight': 'High'
        },
        'sensitive': {
            'keywords': ['password', 'credit card', 'ssn', 'social security', 
                        'account number', 'pin', 'cvv'],
            'explanation': 'No legitimate organization will ask for sensitive credentials via email.',
            'weight': 'Critical'
        }
    }
    
    # Detect words from each category
    for category, data in word_categories.items():
        found_words = []
        for keyword in data['keywords']:
            if keyword in text_lower:
                found_words.append(keyword)
        
        if found_words:
            detected_words.append({
                'category': category.replace('_', ' ').title(),
                'words': found_words[:3],  # Limit to 3 words per category
                'explanation': data['explanation'],
                'weight': data['weight']
            })
    
    # Sort by weight priority
    weight_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    detected_words.sort(key=lambda x: weight_order.get(x['weight'], 4))
    
    return detected_words[:5]  # Return top 5 categories

def analyze_cognitive_manipulation(text):
    """Analyze text for psychological manipulation tactics"""
    text_lower = text.lower()
    scores = {}
    
    for category, data in MANIPULATION_KEYWORDS.items():
        keywords = data['keywords']
        weight = data['weight']
        
        # Count keyword matches
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Calculate raw score (0-100 scale)
        raw_score = min((matches / len(keywords)) * 100 * weight, 100)
        
        # Apply non-linear scaling for better distribution
        if raw_score > 0:
            scaled_score = min(raw_score * 1.5, 100)
        else:
            scaled_score = 0
            
        scores[f'{category}_score'] = round(scaled_score, 2)
    
    # Calculate overall cognitive manipulation score
    # Weight dangerous categories more heavily
    weighted_sum = (
        scores['fear_score'] * 2.0 +
        scores['urgency_score'] * 1.8 +
        scores['authority_score'] * 1.6 +
        scores['financial_score'] * 1.9 +
        scores['reward_score'] * 1.4 +
        scores['scarcity_score'] * 1.2 +
        scores['guilt_score'] * 1.3 +
        scores['trust_score'] * 0.5  # Trust exploitation is subtle
    )
    
    total_weight = 2.0 + 1.8 + 1.6 + 1.9 + 1.4 + 1.2 + 1.3 + 0.5
    overall_score = round((weighted_sum / total_weight), 2)
    
    scores['overall_cognitive_score'] = overall_score
    
    return scores

app = Flask(__name__)

# Load model and vectorizer
MODEL_PATH = 'model/phishing_model.pkl'
VECTORIZER_PATH = 'model/vectorizer.pkl'

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-insight', methods=['GET'])
def get_insight():
    """Endpoint to get a random security insight"""
    insight = get_random_security_insight()
    return jsonify(insight)

@app.route('/get-demo-example/<example_type>', methods=['GET'])
def get_demo_example(example_type):
    """Endpoint to get demo examples for live demonstrations"""
    examples = {
        'safe': {
            'text': """Hi Team,

This is a reminder that our quarterly team meeting is scheduled for Friday, March 15th at 2:00 PM in Conference Room B.

Agenda:
- Q1 Performance Review
- Q2 Goals and Objectives
- New Project Assignments

Please review the attached documents before the meeting and come prepared with any questions.

Looking forward to seeing everyone there!

Best regards,
Sarah Johnson
Project Manager
Tech Solutions Inc.""",
            'description': 'Legitimate business email with no threat indicators'
        },
        'medium': {
            'text': """Dear Valued Customer,

Your recent order #45892 has been processed and will be shipped within 2-3 business days.

However, we noticed that your shipping address may be incomplete. Please verify your address by clicking the link below to ensure timely delivery:

http://verify-shipping-info.com/confirm

If you have any questions, please contact our customer service team.

Thank you for your business!

Customer Support Team""",
            'description': 'Suspicious verification request with external link'
        },
        'danger': {
            'text': """URGENT SECURITY ALERT - IMMEDIATE ACTION REQUIRED

Your account has been SUSPENDED due to suspicious activity detected on your account. Unauthorized access was attempted from an unknown location.

You must verify your identity IMMEDIATELY to restore access. Your account will be permanently locked within 24 hours if you do not act now.

CLICK HERE to verify your account: http://secure-verify-account.net/login

Enter your username, password, and social security number to confirm your identity.

This is your FINAL WARNING. Do not ignore this message.

Security Team
Account Protection Department""",
            'description': 'High-risk phishing attempt with multiple red flags'
        }
    }
    
    if example_type in examples:
        return jsonify(examples[example_type])
    else:
        return jsonify({'error': 'Invalid example type'}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not model or not vectorizer:
        return jsonify({'error': 'Model not trained yet. Please train the model first.'}), 400
    
    # Vectorize and predict
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    probability = model.predict_proba(text_vectorized)[0]
    
    # Calculate scores
    phishing_probability = float(probability[1]) * 100
    confidence_score = float(max(probability)) * 100
    
    # Determine threat level (SAFE / WARNING / DANGER)
    if phishing_probability < 30:
        threat_level = 'SAFE'
    elif phishing_probability < 70:
        threat_level = 'WARNING'
    else:
        threat_level = 'DANGER'
    
    is_threat = prediction == 1
    
    # Analyze cognitive manipulation
    cognitive_scores = analyze_cognitive_manipulation(text)
    
    # Calculate risk level and color
    risk_level, risk_color = calculate_risk_level(phishing_probability)
    
    # Get feature importance
    feature_importance = get_feature_importance(text, cognitive_scores, phishing_probability)
    
    # Detect suspicious words
    suspicious_words = detect_suspicious_words(text)
    
    # Get a random security insight
    security_insight = get_random_security_insight()
    
    # Generate teach-back guidance
    teachback = generate_teachback(text, phishing_probability, cognitive_scores, threat_level)
    
    # Generate educational feedback
    feedback = generate_feedback(text, is_threat, phishing_probability, cognitive_scores)
    
    return jsonify({
        'is_threat': bool(is_threat),
        'phishing_probability': round(phishing_probability, 2),
        'confidence_score': round(confidence_score, 2),
        'threat_level': threat_level,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'cognitive_scores': cognitive_scores,
        'feature_importance': feature_importance,
        'suspicious_words': suspicious_words,
        'security_insight': security_insight,
        'teachback': teachback,
        'feedback': feedback
    })

def generate_teachback(text, phishing_probability, cognitive_scores, threat_level):
    """Generate dynamic teach-back guidance based on detected threats"""
    
    if phishing_probability < 30:
        return None
    
    teachback = {
        'why_dangerous': '',
        'attacker_goal': '',
        'what_to_do': '',
        'safety_tip': ''
    }
    
    # Identify primary manipulation tactics
    tactics = []
    if cognitive_scores['fear_score'] > 30:
        tactics.append('fear')
    if cognitive_scores['urgency_score'] > 30:
        tactics.append('urgency')
    if cognitive_scores['authority_score'] > 30:
        tactics.append('authority')
    if cognitive_scores['financial_score'] > 30:
        tactics.append('financial')
    if cognitive_scores['reward_score'] > 30:
        tactics.append('reward')
    if cognitive_scores['scarcity_score'] > 30:
        tactics.append('scarcity')
    if cognitive_scores['guilt_score'] > 30:
        tactics.append('guilt')
    
    # Build "Why this is dangerous" explanation
    danger_parts = []
    
    if 'fear' in tactics:
        danger_parts.append("creates panic by threatening your account security")
    if 'urgency' in tactics:
        danger_parts.append("pressures you to act quickly without thinking")
    if 'authority' in tactics:
        danger_parts.append("impersonates trusted organizations to gain credibility")
    if 'financial' in tactics:
        danger_parts.append("uses financial threats to trigger emotional responses")
    if 'reward' in tactics:
        danger_parts.append("offers unrealistic rewards to lure you in")
    if 'scarcity' in tactics:
        danger_parts.append("creates false urgency with limited-time claims")
    if 'guilt' in tactics:
        danger_parts.append("manipulates your emotions through guilt")
    
    if danger_parts:
        if len(danger_parts) == 1:
            teachback['why_dangerous'] = f"This message {danger_parts[0]}. These psychological tactics are designed to bypass your critical thinking and make you act impulsively."
        elif len(danger_parts) == 2:
            teachback['why_dangerous'] = f"This message {danger_parts[0]} and {danger_parts[1]}. These combined tactics are designed to overwhelm your judgment and force hasty decisions."
        else:
            tactics_list = ', '.join(danger_parts[:-1]) + f", and {danger_parts[-1]}"
            teachback['why_dangerous'] = f"This message uses multiple manipulation tactics: {tactics_list}. This layered approach is a hallmark of sophisticated phishing attacks."
    else:
        teachback['why_dangerous'] = "This message contains patterns commonly found in phishing attempts. The language and structure are designed to manipulate your decision-making."
    
    # Build "What attacker wants" explanation
    text_lower = text.lower()
    attacker_goals = []
    
    if any(word in text_lower for word in ['click', 'link', 'here', 'download']):
        attacker_goals.append("click a malicious link")
    if any(word in text_lower for word in ['verify', 'confirm', 'update', 'login']):
        attacker_goals.append("enter your credentials on a fake website")
    if any(word in text_lower for word in ['password', 'credit card', 'ssn', 'account number']):
        attacker_goals.append("provide sensitive personal or financial information")
    if any(word in text_lower for word in ['call', 'phone', 'contact']):
        attacker_goals.append("contact them directly to manipulate you further")
    if any(word in text_lower for word in ['download', 'attachment', 'file']):
        attacker_goals.append("download malware onto your device")
    if any(word in text_lower for word in ['transfer', 'payment', 'send money']):
        attacker_goals.append("transfer money or make unauthorized payments")
    
    if attacker_goals:
        if len(attacker_goals) == 1:
            teachback['attacker_goal'] = f"The attacker wants you to {attacker_goals[0]}."
        else:
            goals_list = ', '.join(attacker_goals[:-1]) + f", or {attacker_goals[-1]}"
            teachback['attacker_goal'] = f"The attacker wants you to {goals_list}."
    else:
        teachback['attacker_goal'] = "The attacker wants you to take action without verifying the message's authenticity, potentially compromising your security."
    
    # Build "What you should do instead"
    actions = []
    
    if threat_level == 'DANGER':
        actions.append("Do NOT click any links or download attachments")
        actions.append("Do NOT provide any information")
        actions.append("Delete this message immediately after reporting it")
    else:
        actions.append("Do not click any links until verified")
        actions.append("Do not provide sensitive information")
    
    actions.append("Verify the sender by contacting the organization directly using official contact information (not from this message)")
    
    if 'authority' in tactics:
        actions.append("Check the sender's email address carefully - phishers often use similar-looking domains")
    
    actions.append("Report this message to your IT security team or email provider")
    
    teachback['what_to_do'] = " ".join(actions)
    
    # Generate 30-second safety tip
    tips = [
        "Always pause before responding to urgent requests. Legitimate organizations rarely demand immediate action.",
        "Hover over links (don't click) to see the real destination. If it looks suspicious, it probably is.",
        "Check the sender's email address carefully. Phishers use domains that look similar to real ones.",
        "When in doubt, contact the organization directly using contact info from their official website, not from the message.",
        "No legitimate organization will ask for passwords, PINs, or full credit card numbers via email.",
        "Be skeptical of unexpected prizes, refunds, or urgent security alerts. Verify independently.",
        "Trust your instincts. If something feels off, it probably is. Take time to verify before acting."
    ]
    
    # Select most relevant tip
    if 'urgency' in tactics or 'fear' in tactics:
        teachback['safety_tip'] = tips[0]
    elif any(word in text_lower for word in ['click', 'link']):
        teachback['safety_tip'] = tips[1]
    elif 'authority' in tactics:
        teachback['safety_tip'] = tips[2]
    elif 'reward' in tactics or 'financial' in tactics:
        teachback['safety_tip'] = tips[5]
    else:
        teachback['safety_tip'] = tips[6]
    
    return teachback

def generate_feedback(text, is_threat, score, cognitive_scores):
    feedback = []
    text_lower = text.lower()
    
    if is_threat or score > 30:
        if score >= 70:
            feedback.append("🚨 HIGH THREAT DETECTED - DANGER")
        elif score >= 30:
            feedback.append("⚠️ MODERATE THREAT - WARNING")
        
        # Add cognitive manipulation insights
        if cognitive_scores['fear_score'] > 30:
            feedback.append("• Uses fear-based language to create panic")
        
        if cognitive_scores['urgency_score'] > 30:
            feedback.append("• Employs urgency tactics to pressure quick action")
        
        if cognitive_scores['authority_score'] > 30:
            feedback.append("• Impersonates authority figures or organizations")
        
        if cognitive_scores['financial_score'] > 30:
            feedback.append("• Contains financial threats or pressure tactics")
        
        if cognitive_scores['reward_score'] > 30:
            feedback.append("• Offers unrealistic rewards or prizes (reward bait)")
        
        if cognitive_scores['scarcity_score'] > 30:
            feedback.append("• Uses scarcity tactics (limited time/availability)")
        
        if cognitive_scores['guilt_score'] > 30:
            feedback.append("• Employs guilt manipulation techniques")
        
        if cognitive_scores['trust_score'] > 40:
            feedback.append("• Exploits trust with false security claims")
        
        if cognitive_scores['overall_cognitive_score'] > 50:
            feedback.append(f"• High cognitive manipulation score: {cognitive_scores['overall_cognitive_score']:.1f}/100")
        
        # Check for sensitive data requests
        sensitive_words = ['password', 'credit card', 'ssn', 'account number', 'pin', 'social security']
        if any(word in text_lower for word in sensitive_words):
            feedback.append("• Requests sensitive personal/financial information")
        
        # Check for suspicious links
        if any(word in text_lower for word in ['click', 'link', 'here', 'download']):
            feedback.append("• Contains suspicious call-to-action links")
        
        if len(feedback) == 1:  # Only threat level message
            feedback.append("• ML model detected suspicious patterns in text")
    else:
        feedback.append("✓ Message appears SAFE")
        feedback.append("• No significant threat indicators detected")
        feedback.append("• Low phishing probability")
        
        if cognitive_scores['overall_cognitive_score'] > 20:
            feedback.append(f"• Minor manipulation tactics detected (score: {cognitive_scores['overall_cognitive_score']:.1f}/100)")
    
    return feedback

if __name__ == '__main__':
    app.run(debug=True, port=5000)
