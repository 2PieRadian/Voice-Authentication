# 🏛️ BankVoice AI – Customer Voice Authentication & Banking Analytics

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/2PieRadian/Voice-Authentication)
**Repository URL:** [https://github.com/2PieRadian/Voice-Authentication](https://github.com/2PieRadian/Voice-Authentication)

---

## 📌 Executive Project Synopsis

**BankVoice AI** is an institutional, privacy-first analytics terminal that transforms unstructured customer audio calls into structured, categorized, and auditable banking intelligence in real time. 

Operating **100% locally on CPU** with zero audio data transmitted to third-party clouds, the platform automates contact center compliance triage, flags critical fraud incidents, and surfaces executive risk telemetry.

### Key Capabilities at a Glance:
1. **Audio Ingestion & Signal Conditioning:** Ingests `.wav`, `.mp3`, and `.m4a` audio files. Includes a custom native PCM decoder allowing uncompressed WAV files to run out-of-the-box on Windows without requiring FFmpeg.
2. **Local Neural Speech-to-Text (STT):** Transcribes audio using **OpenAI Whisper** via 80-channel log-mel spectrograms and encoder-decoder transformer attention.
3. **Contextual Sentiment Scoring:** Evaluates customer emotion and distress using **Hugging Face DistilBERT** with calibrated probability scores (0–100%) and heuristic fallback arbitration.
4. **Regulatory Complaint Classification:** Categorizes interactions into 6 statutory banking domains (**Fraud Complaints**, **Transaction Issues**, **Card Issues**, **Loan Issues**, **Account Issues**, **General Enquiries**) with automatic priority escalation for fraud/AML risk.
5. **Acoustic Voice Biometrics (Demonstration):** Extracts 64-bin spectral centroid vectors and computes cosine similarity against enrolled customer voiceprints to prototype speaker verification.
6. **Executive Analytics & Persistent Audit:** Visualizes real-time KPIs and Plotly charts (sentiment donut, complaint distribution, stacked domain cross-tabulation) with permanent local CSV logging (`data/interactions.csv`).

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Interface & Visuals** | Streamlit + Plotly | Institutional dark navy dashboard with interactive charts |
| **Speech-to-Text** | OpenAI Whisper (`base`/`tiny`) | On-premise neural speech transcription |
| **Sentiment Analysis** | Hugging Face Transformers (`DistilBERT`) | Contextual emotional polarity and confidence scoring |
| **Data Processing** | Pandas + NumPy | Tabular transformation, aggregation, and metrics |
| **Storage & Persistence**| Local CSV Ledger | Stateful audit history and sample/live record tracking |
| **Audio Processing** | Python `wave` + `scipy` | Resilient native PCM decoding and spectral feature extraction |

---

## 🚀 Quickstart & Execution

```powershell
# 1. Clone repository
git clone https://github.com/2PieRadian/Voice-Authentication.git
cd Voice-Authentication

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📂 Project Directory Structure

```text
Voice-Authentication/
│
├── app.py                      # Main Streamlit analytics application
├── requirements.txt            # Python dependencies
├── README.md                   # Operational guide & synopsis
├── BankVoice_AI_Technical_Architecture_Document.docx  # Comprehensive whitepaper (.docx)
│
├── data/
│   └── interactions.csv        # Persistent CSV database (15 pre-seeded sample records)
│
├── samples/                    # Pre-recorded realistic banking audio WAV files
│   ├── sample_fraud_alert.wav          # Marcus Vance (Unauthorized charge dispute)
│   ├── sample_loan_inquiry.wav         # Sarah Jenkins (Mortgage refinancing query)
│   └── sample_card_appreciation.wav    # Arthur Pendelton (Card unblock praise)
│
└── utils/
    ├── transcription.py        # Whisper STT pipeline with native WAV PCM decoder
    ├── sentiment.py            # Hugging Face DistilBERT sentiment engine
    ├── classification.py       # 6-category keyword rule engine with urgency scoring
    ├── analytics.py            # Plotly chart generators and KPI metrics
    └── voice_auth.py           # Acoustic voiceprint cosine similarity demo
```

---

## ⚖️ Regulatory & Biometric Disclaimer
The speaker verification module calculates acoustic spectral cosine similarity for architectural demonstration. Speech recognition and sentiment analysis do not authenticate identity. In enterprise production, voice biometrics must be paired with anti-spoofing liveness detection and FIDO2 multi-factor tokens.
