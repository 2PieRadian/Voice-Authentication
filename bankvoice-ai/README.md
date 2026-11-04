# BankVoice AI – Customer Voice Authentication & Banking Analytics

An institutional-grade, privacy-first banking intelligence dashboard that processes incoming customer voice recordings, converts speech to text using **OpenAI Whisper**, classifies sentiment using **Hugging Face Transformers**, categorizes complaint vectors, and surfaces real-time risk telemetry through interactive **Plotly** visualizations.

---

## 1. Executive Summary & Objective

Modern banking contact centers process millions of spoken interactions daily. **BankVoice AI** transforms unstructured voice audio into actionable compliance and operational intelligence:

* **Voice Ingestion:** Ingest customer voice recordings in `.wav`, `.mp3`, or `.m4a` format.
* **Local Speech-to-Text:** Transcribe voice audio locally using OpenAI Whisper (no audio data leaves the local server boundary).
* **Customer Sentiment Analysis:** Classify caller sentiment as **Positive** or **Negative** with calibrated confidence scores using Hugging Face DistilBERT.
* **Complaint Vector Categorization:** Multi-keyword rule engine mapping calls to 6 institutional banking categories with priority urgency scoring.
* **Executive Analytics Telemetry:** Interactive Plotly charts (sentiment distribution donut, complaint category breakdown, domain cross-tabulation) and KPI metrics.
* **Audit Persistence:** Automatic write-back to persistent local storage (`data/interactions.csv`).
* **Voice Biometrics Demonstration:** Acoustic feature extraction and cosine similarity verification sandbox (clearly labeled as a prototype).

---

## 2. Technology Stack

* **Frontend & Interface:** Streamlit (Custom institutional dark navy unslop theme)
* **Speech-to-Text Engine:** OpenAI Whisper (`base` / `tiny` CPU-optimized)
* **Sentiment Analysis:** Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)
* **Data Processing & Analytics:** Pandas & NumPy
* **Interactive Visualizations:** Plotly Express & Plotly Graph Objects
* **Audio Processing:** Native Python `wave` PCM decoder (zero external C-library dependency for WAV files)

---

## 3. Project Directory Structure

```text
bankvoice-ai/
│
├── app.py                      # Main Streamlit application and UI layout
├── requirements.txt            # Locked project dependencies
├── README.md                   # Operational guide & setup manual
│
├── data/
│   └── interactions.csv        # Persistent CSV database with sample & live records
│
├── samples/                    # Realistic pre-recorded banking customer audio WAV files
│   ├── sample_fraud_alert.wav          # Marcus Vance: Unauthorized transaction dispute
│   ├── sample_loan_inquiry.wav         # Sarah Jenkins: Mortgage rate inquiry
│   └── sample_card_appreciation.wav    # Arthur Pendelton: Card unblock service compliment
│
└── utils/
    ├── __init__.py
    ├── transcription.py        # Whisper STT pipeline with native WAV PCM fallback
    ├── sentiment.py            # Hugging Face DistilBERT with resilient heuristic fallback
    ├── classification.py       # 6-domain banking complaint keyword classifier
    ├── analytics.py            # KPI metrics calculation and Plotly chart renderers
    └── voice_auth.py           # Acoustic voiceprint cosine similarity demo module
```

---

## 4. Banking Complaint Taxonomy

The application classifies transcripts into 6 regulated banking domains:

| Category | Typical Keywords | Urgency Level | Description |
| :--- | :--- | :--- | :--- |
| **Fraud Complaints** | *unauthorized, scam, phishing, cloned, stolen, hacked, compromised* | 🚨 **Critical** | Potential unauthorized account takeover or fraudulent charges. |
| **Transaction Issues** | *wire transfer, deposit, duplicate charge, failed payment, ATM dispensed* | 🟠 **High** | Payment discrepancies, duplicate debits, and pending SWIFT/ACH wires. |
| **Card Issues** | *debit card, credit card, chip declined, blocked, replacement card, PIN* | 🟠 **High** | Card terminal failures, chip malfunctions, and replacement requests. |
| **Loan Issues** | *mortgage, interest rate, EMI, repayment, refinance, auto loan* | 🔵 **Medium** | Inquiries regarding loan amortisation, rate adjustments, or payment queries. |
| **Account Issues** | *locked out, login portal, statement, overdraft, KYC update, profile* | 🔵 **Medium** | Account administration, credentials locked, and profile updates. |
| **General Enquiries** | *branch hours, representative, notary, appointment, timing, compliment* | ⚪ **Low** | Routine branch hours, notary queries, and positive service feedback. |

---

## 5. Voice Authentication Prototype Clarification

In compliance with banking security standards:

> **Important Disclaimer:**  
> The Voice Biometrics module provides a **demonstration** of speaker verification using acoustic spectral centroid and frequency feature vectors.  
> * Neither speech recognition nor customer sentiment analysis authenticates a customer's identity.
> * Biometric voiceprint similarity is displayed as an educational prototype and architectural proof-of-concept.
> * It is **not** certified cryptographic banking authentication (such as FIDO2 / WebAuthn).

---

## 6. Installation & Execution Guide (Windows & Cross-Platform)

### Step 1: Clone or Navigate to the Project

```powershell
cd c:\Users\raman\OneDrive\Desktop\hcl-project\bankvoice-ai
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Run the Streamlit Application

```powershell
streamlit run app.py
```

The application will start locally and open in your default browser at `http://localhost:8501`.

### Windows FFmpeg Notice (Optional)

* **WAV files work out-of-the-box:** The application includes a custom WAV PCM decoder that streams uncompressed audio directly into OpenAI Whisper **without requiring FFmpeg**.
* **For MP3/M4A files:** Whisper relies on FFmpeg for compressed audio decoding. If you wish to upload MP3 files on Windows, install FFmpeg via PowerShell:
  ```powershell
  winget install Gyan.FFmpeg
  ```
  *(Restart your terminal after installation so FFmpeg is picked up in your system `PATH`.)*

---

## 7. Sample Data & Demonstration Workflow

1. **Immediate Telemetry:** Upon launch, the dashboard loads **15 pre-loaded realistic fictional banking interactions** spanning all 6 categories, allowing you to explore the KPI metrics, donut chart, and bar charts immediately.
2. **Instant Audio Testing:** Go to **🎙️ Voice Analysis** in the sidebar. You can test immediately using the built-in preset audio clips (e.g., *Critical Fraud Alert*, *Mortgage Inquiry*, or *Card Appreciation*) or upload your own audio file.
3. **Click "⚡ Analyse Voice Recording":** Whisper transcribes the speech, DistilBERT scores customer sentiment, the classifier categorizes the complaint, and the speaker verification module calculates acoustic similarity.
4. **Commit to Database:** Click **"💾 Commit to Interaction Database"** to permanently append the interaction to `data/interactions.csv`. All dashboard statistics and charts update instantly.
5. **Audit History:** Navigate to **📜 Interaction History** to filter, search transcripts, and download the full dataset as a CSV.

