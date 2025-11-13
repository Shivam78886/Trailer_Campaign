# Complete Installation & Setup Guide

## 🎬 Trailer-to-Campaign Autopilot

Transform movie trailers into data-driven marketing campaigns with AI-powered content generation and a modern web interface.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [API Keys Setup](#api-keys-setup)
4. [Running the Application](#running-the-application)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [Features Overview](#features-overview)

---

## 🔧 Prerequisites

### Required Software

- **Python 3.8+** (Python 3.9 or 3.10 recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Virtual environment** (recommended)

### Check Your Python Version

```bash
python3 --version
# Should show Python 3.8.0 or higher
```

### Required API Keys

You'll need API keys from the following services:

1. **TMDb (The Movie Database)** - Required
   - Get free API key: https://www.themoviedb.org/settings/api
   
2. **YouTube Data API v3** - Required
   - Get free API key: https://console.cloud.google.com/apis/library/youtube.googleapis.com
   
3. **Google Gemini AI** - Optional but recommended
   - Get free API key: https://makersuite.google.com/app/apikey

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/anubhav-77-dev/t2a.git
cd t2a
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- google-generativeai (Gemini AI)
- requests (HTTP client)
- python-dotenv (environment variables)
- vaderSentiment, textblob (sentiment analysis)
- pandas, numpy (data processing)
- google-api-python-client (YouTube API)
- pytrends (Google Trends)
- And more...

**Installation time:** ~2-3 minutes

---

## 🔑 API Keys Setup

### Step 1: Create .env File

Copy the example file:

```bash
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in your text editor and add your API keys:

```bash
nano .env
# or
code .env
# or
vim .env
```

### Step 3: Add Your API Keys

```env
# Required - TMDb API (v3 or v4)
TMDB_API_KEY=your_tmdb_api_key_here
# OR use TMDb v4 Bearer Token (preferred)
TMDB_BEARER_TOKEN=your_tmdb_bearer_token_here

# Required - YouTube Data API
YOUTUBE_API_KEY=your_youtube_api_key_here

# Optional but Recommended - Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - OpenAI (alternative to Gemini)
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Default regions to analyze
DEFAULT_REGIONS=US,UK,IN,CA,AU
```

### How to Get Each API Key:

#### TMDb API Key
1. Go to https://www.themoviedb.org/signup
2. Create free account
3. Go to Settings → API
4. Request API key (select "Developer")
5. Copy your API key

#### YouTube Data API Key
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "YouTube Data API v3"
4. Go to Credentials → Create Credentials → API Key
5. Copy your API key

#### Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

---

## 🚀 Running the Application

### Option 1: Web Interface (Recommended)

The web interface provides a modern, user-friendly way to generate campaigns.

#### Start the Web Server

```bash
# Make sure you're in the venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the server
python web/app.py
```

You should see:

```
🎬 Trailer-to-Campaign Autopilot Web UI
============================================================
🐍 Python: /path/to/your/venv/bin/python
🌐 Server: http://localhost:8080
📊 TMDb: ✓
📺 YouTube: ✓
✅ Gemini AI initialized successfully
🤖 AI: ✓ Gemini
============================================================
Press Ctrl+C to stop

 * Running on http://127.0.0.1:8080
```

#### Access the Web UI

Open your browser and go to:

```
http://localhost:8080
```

**Features:**
- 🎬 Modern, responsive interface
- 📊 Real-time progress tracking
- 💾 Campaign management
- 🤖 AI-enhanced content generation
- 📈 Visual analytics display

---

### Option 2: Command Line Interface

For advanced users and automation.

#### Generate a Campaign

```bash
python main.py generate \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Movie Title"
```

**Example:**

```bash
python main.py generate \
  --url "https://www.youtube.com/watch?v=Way9Dexny3w" \
  --title "Dune: Part Two"
```

#### With Custom Regions

```bash
python main.py generate \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Movie Title" \
  --regions US,UK,IN,CA,AU
```

#### View Generated Campaigns

```bash
# List all campaigns
python main.py show

# View specific campaign
python main.py show "Movie_Title_20251113_123456.json"
```

#### Check Configuration

```bash
python main.py config-check
```

---

## 📖 Usage Guide

### Web Interface Workflow

1. **Start Server**: `python web/app.py`
2. **Open Browser**: Go to http://localhost:8080
3. **Enter Details**:
   - Paste YouTube trailer URL
   - Enter movie title
   - (Optional) Specify target regions
4. **Generate Campaign**: Click "Generate Campaign"
5. **Track Progress**: Watch real-time progress (6 steps)
6. **View Results**: Automatically redirected when complete

### Generated Campaign Includes:

#### 1. **Movie Metadata**
- Title, genres, cast, director
- Release date, runtime, budget
- TMDb ratings and popularity

#### 2. **Engagement Analytics**
- YouTube views, likes, comments
- Engagement rate
- Sentiment analysis (POSITIVE/NEGATIVE/NEUTRAL)

#### 3. **AI-Enhanced Ad Copy** (with Gemini)
- 5+ variants optimized for different lengths
- Platform-specific targeting
- Grounded in actual trailer metrics

#### 4. **Social Media Posts**
- Twitter/𝕏 (280 chars)
- Instagram (caption + hashtags)
- Facebook (engaging copy)
- TikTok (short, punchy)

#### 5. **Regional Analysis**
- Market prioritization (Tier A/B/C/D)
- Budget allocation by region
- Recommended strategies

#### 6. **Rollout Plan**
- 6-week phased campaign
- Week-by-week timeline
- Budget breakdown
- Key activities per phase

#### 7. **AI Strategic Insights** (with Gemini)
- 🟢 Opportunities
- 🟡 Risks
- 🔵 Recommendations

---

## 🎯 Features Overview

### Core Features

- ✅ **Multi-Source Data Collection**
  - TMDb movie metadata
  - YouTube engagement metrics
  - Sentiment analysis (310+ comments)
  - Google Trends (with rate limit handling)
  - Wikipedia pageviews

- ✅ **AI Enhancement (Gemini)**
  - Creative ad copy generation
  - Strategic campaign insights
  - Market opportunity analysis
  - Risk assessment

- ✅ **Modern Web Interface**
  - Responsive design (mobile-friendly)
  - Real-time progress tracking
  - Campaign management
  - Tabbed results display

- ✅ **CLI Support**
  - Automation-friendly
  - Batch processing
  - JSON output

### Advanced Features

- **Source Tracing**: Every claim linked to data source
- **Regional Scoring**: Intelligent market prioritization
- **Budget Allocation**: Data-driven budget distribution
- **Graceful Degradation**: Works even if some APIs fail
- **Rate Limit Handling**: Smart retry logic for Google Trends

---

## 🔍 Troubleshooting

### Web Server Issues

#### Port 5000 Already in Use (macOS)

**Problem**: AirPlay Receiver uses port 5000

**Solution**: The app now uses port 8080 by default. If you need a different port, edit `web/app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

#### "Flask not found"

**Problem**: Flask not installed in current environment

**Solution**:
```bash
# Activate venv
source venv/bin/activate

# Install Flask
pip install flask
```

#### "No module named 'dotenv'"

**Problem**: python-dotenv not installed

**Solution**:
```bash
pip install python-dotenv
```

### API Issues

#### TMDb Connection Errors

**Problem**: SSL/connection errors

**Solutions**:
1. Check internet connection
2. Try TMDb v4 Bearer Token instead of API key
3. Wait a moment and retry

#### YouTube API Quota Exceeded

**Problem**: Daily quota of 10,000 units exceeded

**Solution**:
1. Wait until next day (quota resets daily)
2. Or create additional Google Cloud projects with new API keys

#### Google Trends Rate Limiting

**Problem**: HTTP 429 errors

**Solution**: 
- The system automatically handles this with graceful degradation
- Campaign generation continues without Trends data
- Wait 1-2 hours before retrying if needed

#### Gemini Not Working

**Problem**: "AI variants not generated"

**Solution**:
```bash
# 1. Check API key is set
grep GEMINI_API_KEY .env

# 2. Test Gemini setup
python test_gemini.py

# 3. Check server logs for errors
# Look for "✅ Gemini AI initialized successfully"
```

### Data Issues

#### "No campaigns found"

**Problem**: No campaigns in `outputs/` directory

**Solution**: Generate a campaign first using either web UI or CLI

#### Campaign Data Missing

**Problem**: Some sections empty in results

**Solution**:
- Check terminal output for API errors
- Verify all required API keys are set
- Some data (like Trends) may be unavailable due to rate limits

---

## 📂 Project Structure

```
t2a/
├── web/                      # Web interface
│   ├── app.py               # Flask server
│   ├── templates/           # HTML templates
│   │   ├── base.html       # Base layout
│   │   ├── index.html      # Campaign form
│   │   └── results.html    # Results display
│   └── static/
│       └── styles.css      # Custom CSS
│
├── src/                     # Core application
│   ├── collectors/          # Data collection
│   │   ├── tmdb_client.py
│   │   ├── youtube_client.py
│   │   ├── trends_client.py
│   │   └── ...
│   ├── analyzers/           # Data analysis
│   │   ├── sentiment_analyzer.py
│   │   ├── trend_detector.py
│   │   └── regional_scorer.py
│   ├── generators/          # Content generation
│   │   ├── ad_copy_generator.py
│   │   ├── social_post_generator.py
│   │   └── gemini_enhancer.py
│   ├── planners/            # Campaign planning
│   │   └── rollout_planner.py
│   ├── utils/               # Utilities
│   │   ├── config.py
│   │   └── source_tracker.py
│   └── autopilot.py         # Main orchestrator
│
├── docs/                    # Documentation
│   └── WEB_UI.md           # Web UI guide
│
├── examples/                # Example scripts
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── ...
│
├── outputs/                 # Generated campaigns (gitignored)
├── cache/                   # API cache (gitignored)
├── venv/                    # Virtual environment (gitignored)
│
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── .env                     # API keys (gitignored)
├── .env.example            # API key template
├── README.md               # Project overview
├── QUICKSTART.md           # Quick start guide
├── INSTALLATION.md         # This file
└── PROJECT_SUMMARY.md      # Technical summary
```

---

## 🎓 Example Workflows

### Workflow 1: Quick Campaign Generation

```bash
# 1. Start web server
python web/app.py

# 2. Open browser to http://localhost:8080

# 3. Paste trailer URL
https://www.youtube.com/watch?v=Way9Dexny3w

# 4. Enter movie title
Dune: Part Two

# 5. Click "Generate Campaign"

# 6. Wait ~15-20 seconds

# 7. View results with AI-enhanced content
```

### Workflow 2: CLI Batch Processing

```bash
# Generate multiple campaigns
python main.py generate --url "URL1" --title "Movie 1"
python main.py generate --url "URL2" --title "Movie 2"
python main.py generate --url "URL3" --title "Movie 3"

# List all campaigns
python main.py show

# Export specific campaign
cat outputs/Movie_1_20251113_123456.json
```

### Workflow 3: Development Testing

```bash
# 1. Test configuration
python main.py config-check

# 2. Test Gemini setup
python test_gemini.py

# 3. Run web server in debug mode
python web/app.py

# 4. Check server logs in terminal
```

---

## 🔒 Security Notes

### Important

- **Never commit `.env` file** to Git (already in .gitignore)
- **Keep API keys private** - don't share them
- **Use environment variables** for production deployment
- **Enable HTTPS** for production web server
- **Add authentication** if deploying publicly

### For Production

1. **Disable Flask debug mode** in `web/app.py`:
   ```python
   app.run(debug=False)
   ```

2. **Use production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 web.app:app
   ```

3. **Set up reverse proxy** (Nginx/Apache)

4. **Use SSL certificates** (Let's Encrypt)

5. **Implement rate limiting** to prevent API quota exhaustion

---

## 📊 Performance Tips

### Optimize Campaign Generation

- **Use TMDb v4 Bearer Token** for better rate limits
- **Limit target regions** to 3-5 for faster processing
- **Cache enabled** by default for TMDb/Wikipedia data
- **Parallel API calls** where possible

### Web Server Performance

- **Single user**: Default Flask server is fine
- **Multiple users**: Use Gunicorn with 4-8 workers
- **High traffic**: Add Redis for job queue and caching

### Expected Timings

- Metadata collection: 1-2 seconds
- YouTube engagement: 2-3 seconds
- Sentiment analysis: 1-2 seconds
- Google Trends: 3-5 seconds (or skipped if rate limited)
- Ad copy generation: 1-2 seconds
- Gemini AI enhancement: 3-5 seconds

**Total**: ~12-20 seconds per campaign

---

## 🆘 Getting Help

### Documentation

- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick setup
- [WEB_UI.md](docs/WEB_UI.md) - Web interface guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details

### Common Commands

```bash
# Check Python version
python3 --version

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check configuration
python main.py config-check

# Test Gemini
python test_gemini.py

# Start web server
python web/app.py

# Generate campaign (CLI)
python main.py generate --url "URL" --title "Title"
```

### Still Having Issues?

1. Check the [Troubleshooting](#troubleshooting) section above
2. Verify all API keys are correctly set in `.env`
3. Run `python main.py config-check` to validate setup
4. Check terminal output for specific error messages
5. Make sure you're in the virtual environment (`(venv)` in prompt)

---

## 🎉 You're All Set!

Your Trailer-to-Campaign Autopilot is ready to use!

### Quick Start Reminder

```bash
# 1. Activate venv
source venv/bin/activate

# 2. Start web server
python web/app.py

# 3. Open browser
open http://localhost:8080

# 4. Generate your first campaign!
```

**Happy campaigning! 🎬✨**
