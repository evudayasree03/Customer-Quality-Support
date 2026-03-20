# SamiX ~ samiksha
## GenAI-Powered Customer Support Quality Auditor
> *The All-Seeing Eye of Quality* · ಸಮೀಕ್ಷೆ

---

## Quick start (Windows 11 Pro — 5 steps)

### 1  Prerequisites
```
Python 3.11+   →  https://www.python.org/downloads/
Git            →  https://git-scm.com/download/win
FFmpeg         →  https://ffmpeg.org/download.html  (needed by pydub)
               →  Add to PATH: C:\ffmpeg\bin
```

### 2  Clone & create virtual environment
```bat
git clone https://github.com/YOUR_USERNAME/samix.git
cd samix
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3  Set your admin password
```bat
python generate_hash.py
```
Copy the hash printed to the terminal.

### 4  Configure secrets
Edit `.streamlit/secrets.toml` — paste your hash and API keys:
```toml
[auth]
hashed_password = "$2b$12$YOUR_HASH_HERE"
cookie_key      = "change_this_to_any_random_string"
admin_name      = "Your Name"
admin_email     = "you@company.com"

[groq]
api_key = "gsk_your_groq_key"          # https://console.groq.com

[deepgram]
api_key = "your_deepgram_key"          # https://console.deepgram.com

[email]                                # optional — for real email alerts
smtp_host       = "smtp.gmail.com"
smtp_port       = 587
sender_address  = "alerts@yourmail.com"
sender_password = "your_app_password"
```
> ⚠ Never commit `secrets.toml` — it is in `.gitignore`.

### 5  Run
```bat
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
Login: username `admin` + the password you set in step 3.

---

## Free cloud hosting on Streamlit Community Cloud

1. Push your repo to GitHub (see below — secrets are excluded by .gitignore)
2. Go to https://share.streamlit.io → **New app**
3. Select your repo + `app.py`
4. Click **Advanced settings → Secrets** and paste the contents of your `secrets.toml`
5. Click **Deploy** — live in ~2 minutes

---

## Push to GitHub

```bat
# First time
git init                          # already done if you cloned
git add .
git commit -m "Initial SamiX commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/samix.git
git push -u origin main

# Subsequent updates
git add .
git commit -m "Your message"
git push
```

---

## Project structure

```
samix/
├── app.py                        ← Streamlit entry point
├── generate_hash.py              ← run once to hash your password
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml               ← Deep Slate dark theme
│   └── secrets.toml              ← NEVER commit · listed in .gitignore
├── src/
│   ├── auth/
│   │   └── authenticator.py      ← streamlit-authenticator wrapper
│   ├── pipeline/
│   │   ├── groq_client.py        ← dual-call LLM (mock fallback)
│   │   ├── stt_processor.py      ← Deepgram + Whisper + chat parser
│   │   └── alert_engine.py       ← st.toast + SMTP email
│   ├── ui/
│   │   ├── styles.py             ← CSS injection (Deep Slate theme)
│   │   ├── components.py         ← gauges, charts, transcript, cost card
│   │   ├── login_page.py         ← professional login screen
│   │   ├── agent_panel.py        ← client workspace
│   │   └── admin_panel.py        ← admin dashboard
│   └── utils/
│       ├── history_manager.py    ← JSON persistence · filename consistency
│       ├── audio_processor.py    ← pydub + TTS summary
│       ├── cost_tracker.py       ← token × price → profit/loss
│       └── kb_manager.py         ← Milvus Lite RAG KB
└── data/
    ├── history/                  ← audit JSON files
    ├── kb/                       ← indexed KB documents
    └── uploads/                  ← raw uploaded files
```

---

## Features

| Feature | Implementation |
|---|---|
| Secure login | streamlit-authenticator · bcrypt hash in secrets.toml |
| Speaker separation | Deepgram diarize=true · Twilio dual-stream for live |
| Filename consistency | uploaded name = stored name = history name = report name |
| Audio player + summary | pydub WAV 16kHz · gTTS / pyttsx3 synthesis |
| Dual scoring | Agent QA 0–100 · Customer sentiment 0–10 per turn |
| ECharts gauges | Empathy · Professionalism · Compliance |
| Dual score chart | Plotly · red-zone markers · hover breakdown |
| Where it went wrong | Exact turn · verbatim quote · wrong fact · correct fact · specific correction |
| RAG KB | Milvus Lite · LangChain · all-MiniLM-L6-v2 · PDF/TXT upload |
| Generalised KB | ITIL · ISO 9001 · GDPR · de-escalation · 50 empathy phrases |
| Alert system | st.toast (screen pop) · SMTP email |
| Cost evaluation | Token count × price · profit/loss per audit |
| Download report | TXT · JSON · CSV · email |
| Admin: model perf | Groq latency · scoring accuracy · STT stats · RAG stats |
| Admin: users | Usage · growth · churn · email action |
| Admin: billing | Revenue vs cost · send invoice emails · margin |
| Admin: RAG KB | Upload · index · delete files · collection tags |
| Admin: system health | Service uptime · latency chart · queue stats |

---

## API keys (all free tiers sufficient for development)

| Service | Free tier | Link |
|---|---|---|
| Groq | ~14,400 requests/day | https://console.groq.com |
| Deepgram | $200 credit | https://console.deepgram.com |
| Streamlit Cloud | Unlimited public apps | https://share.streamlit.io |

Whisper, Milvus Lite, pydub, gTTS — all free, no account needed.

---

## Troubleshooting

**`pydub` audio error** — Install FFmpeg and add to PATH.

**`streamlit-authenticator` import error** — Run `pip install streamlit-authenticator==0.3.2`

**`sentence-transformers` slow first run** — It downloads the MiniLM model (~90 MB) once.

**Groq mock data showing** — Check your Groq API key in secrets.toml starts with `gsk_` (not `gsk_REPLACE`).

**Login not working** — Re-run `python generate_hash.py`, copy the new hash exactly into secrets.toml.
