# Trailer-to-Campaign Autopilot 🎬

**Transform movie trailers into data-driven marketing campaigns with AI-powered content generation.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-purple.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What It Does

This system analyzes movie/OTT trailers from YouTube and generates complete marketing campaigns including:

- 🎨 **AI-Enhanced Ad Copy** (5+ variants optimized by Gemini)
- 📱 **Social Media Posts** (Twitter, Instagram, Facebook, TikTok)
- 🌍 **Regional Rollout Plans** (6-week phased strategy)
- 📊 **Market Analysis** (sentiment, trends, engagement metrics)
- 💡 **Strategic Insights** (AI-powered opportunities & recommendations)
- 🔗 **Source Tracing** (every claim linked to data)

**All outputs are grounded in real data** from YouTube comments, TMDb metadata, Google Trends, and Wikipedia pageviews.

---

## ✨ Key Features

### 🖥️ Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Progress**: Watch campaign generation step-by-step
- **Campaign Management**: Browse and reload previous campaigns
- **AI Enhancement**: Powered by Google Gemini for creative content

### 🤖 AI-Powered Content
- **Gemini Integration**: Enhanced ad copy and strategic insights
- **Sentiment Analysis**: VADER + TextBlob for audience sentiment
- **Trend Detection**: Momentum and spike detection
- **Regional Scoring**: Intelligent market prioritization

### 📊 Multi-Source Data Collection

| Source | Purpose | Data Collected |
|--------|---------|----------------|
| **TMDb** | Movie metadata | Cast, genres, ratings, budget, images |
| **YouTube** | Engagement | Views, likes, comments, sentiment |
| **Wikipedia** | Public interest | Pageview trends by region |
| **Google Trends** | Search trends | Regional interest over time |
| **Gemini AI** | Content enhancement | Creative ad copy, strategic insights |

### 🎯 Smart Campaign Generation
- **6-Week Rollout Plan**: Phased regional strategy
- **Budget Allocation**: Data-driven budget distribution
- **Platform Optimization**: Tailored content for each social platform
- **Source Citations**: Every claim linked to original data
- **Graceful Degradation**: Works even if some APIs fail

---

## 🚀 Quick Start

### Installation (3 Steps)

```bash
# 1. Clone and navigate
git clone https://github.com/anubhav-77-dev/t2a.git
cd t2a

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

### Launch Web Interface

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python web/app.py

# Open browser to http://localhost:8080
```

**Full installation guide:** [INSTALLATION.md](INSTALLATION.md)

---

## 🎬 Screenshots

### Web Interface
![Web UI](https://via.placeholder.com/800x400/667eea/ffffff?text=Campaign+Generation+Form)
*Modern, responsive interface for campaign generation*

### Real-time Progress
![Progress Tracking](https://via.placeholder.com/800x400/764ba2/ffffff?text=Real-time+Progress+Tracking)
*Watch as your campaign is built step-by-step*

### AI-Enhanced Results
![Campaign Results](https://via.placeholder.com/800x400/10b981/ffffff?text=AI-Enhanced+Campaign+Results)
*Comprehensive results with AI insights*

---

## 📖 Usage

### Web Interface (Recommended)

1. **Start Server**: `python web/app.py`
2. **Open Browser**: Go to `http://localhost:8080`
3. **Enter Details**:
   - Paste YouTube trailer URL
   - Enter movie title
   - (Optional) Specify target regions
4. **Generate**: Click "Generate Campaign"
5. **View Results**: See AI-enhanced content, social posts, rollout plan, and insights

### Command Line Interface

```bash
# Generate campaign
python main.py generate \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Movie Title"

# With custom regions
python main.py generate \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "Movie Title" \
  --regions US,UK,IN,CA,AU

# View campaigns
python main.py show

# Check configuration
python main.py config-check
```

---

## 🔑 API Keys Required

### Essential (Free)
- **TMDb API**: https://www.themoviedb.org/settings/api
- **YouTube Data API**: https://console.cloud.google.com/apis/library/youtube.googleapis.com

### Optional (Recommended)
- **Google Gemini AI**: https://makersuite.google.com/app/apikey (for AI enhancement)

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## Installation

```bash
# Clone or navigate to the project
cd t2a

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
# Required
TMDB_API_KEY=your_tmdb_key_here
YOUTUBE_API_KEY=your_youtube_key_here

# Optional (for advanced features)
OPENAI_API_KEY=your_openai_key_here  # For enhanced copy generation
```

### Getting API Keys

1. **TMDb**: Register at https://www.themoviedb.org/settings/api
2. **YouTube**: Create project at https://console.developers.google.com/
   - Enable YouTube Data API v3
   - Create credentials (API key)

## Quick Start

```bash
# Basic usage - analyze a trailer
python main.py --trailer-url "https://www.youtube.com/watch?v=TRAILER_ID" --movie-title "Dune Part Two"

# With TMDb ID
python main.py --tmdb-id 693134 --trailer-url "https://www.youtube.com/watch?v=Way9Dexny3w"

# Generate specific content types
python main.py --trailer-url "URL" --generate ad-copy,social-posts,rollout-plan

# Regional focus
python main.py --trailer-url "URL" --regions US,UK,IN,BR
```

## Project Structure

```
t2a/
├── src/
│   ├── collectors/          # Data collection modules
│   │   ├── tmdb_client.py
│   │   ├── youtube_client.py
│   │   ├── wikipedia_client.py
│   │   ├── trends_client.py
│   │   └── weather_client.py
│   ├── analyzers/           # Signal analysis
│   │   ├── sentiment_analyzer.py
│   │   ├── trend_detector.py
│   │   └── regional_scorer.py
│   ├── generators/          # Content generation
│   │   ├── ad_copy_generator.py
│   │   ├── social_post_generator.py
│   │   ├── email_generator.py
│   │   └── thumbnail_generator.py
│   ├── planners/            # Campaign planning
│   │   └── rollout_planner.py
│   └── utils/               # Helpers
│       ├── source_tracker.py
│       └── config.py
├── examples/                # Example outputs
├── tests/                   # Unit tests
├── main.py                  # CLI entry point
├── requirements.txt
└── README.md
```

## Example Output

```json
{
  "campaign_id": "dune-part-two-2024",
  "generated_at": "2024-03-15T10:30:00Z",
  "ad_copy": [
    {
      "variant": "short",
      "text": "The desert calls. #DunePartTwo - In theaters March 15",
      "sources": ["youtube_comment:xyz", "tmdb:tagline"],
      "confidence": 0.92
    }
  ],
  "rollout_plan": {
    "priority_regions": [
      {"region": "US", "score": 0.95, "reasoning": "High Google Trends + pageviews"},
      {"region": "UK", "score": 0.87, "reasoning": "Strong comment engagement"}
    ]
  }
}
```

## Use Cases

- **Marketing Teams**: Auto-generate campaign materials from trailer drops
- **Distribution**: Prioritize markets based on real-time interest
- **Social Media Managers**: Platform-optimized content with trending hooks
- **Agencies**: Rapid campaign prototyping with data backing

## Roadmap

- [ ] Multi-language support for international campaigns
- [ ] A/B testing variant generator
- [ ] TikTok/Shorts optimization
- [ ] Competitive analysis (compare similar films)
- [ ] Budget allocation suggestions
- [ ] Real-time dashboard

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Please open an issue first to discuss major changes.

---

Built with publicly available APIs and transparent data sourcing. 🎥✨
