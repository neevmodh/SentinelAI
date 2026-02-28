# ⚡ Quick Start Guide

Get SentinelAI up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- pip
- 4GB RAM
- Modern web browser

## Installation (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Train the Model
```bash
cd model
python train.py
cd ..
```

**Expected output:**
- Training progress
- Accuracy: ~98.65%
- Model saved: `phishing_model.pkl`

### 3️⃣ Run the Application
```bash
python app.py
```

**Open browser:** http://localhost:5000

## First Analysis

1. Click **"🎯 Demo Attack Mode"**
2. Select **"🚨 High Risk Phishing"**
3. Click **"Analyze Threat"**
4. Explore the results!

## What You'll See

✅ **Threat Level**: DANGER (red)
✅ **Phishing Probability**: ~95%
✅ **Cognitive Analysis**: Radar chart with 8 tactics
✅ **Suspicious Words**: Highlighted dangerous phrases
✅ **Teach-Back**: Educational explanation
✅ **Recommendations**: What to do next

## Try Your Own Text

1. Clear the text area
2. Paste any email or message
3. Press `Ctrl+Enter` or click "Analyze Threat"
4. Review the comprehensive analysis

## Keyboard Shortcuts

- `Ctrl+Enter` - Analyze message
- Click "Get New Insight" - Load new security tip

## Troubleshooting

### Model Not Found Error
```bash
cd model
python train.py
```

### Port Already in Use
```bash
# Change port in app.py (last line)
app.run(debug=True, port=5001)
```

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

- 📚 Read the full [README.md](README.md)
- 🤝 Check [CONTRIBUTING.md](CONTRIBUTING.md)
- 🚀 Push to GitHub using [SETUP_GITHUB.md](SETUP_GITHUB.md)

## Need Help?

Open an issue on GitHub or check the documentation!

---

**Happy threat hunting! 🛡️**
