"""
BankVoice AI – Customer Voice Authentication & Banking Analytics
Production-grade Streamlit application for enterprise audio banking intelligence.
"""

import os
import sys
import time
import tempfile
from datetime import datetime
import pandas as pd
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="BankVoice AI | Banking Voice Analytics",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe relative module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils.transcription import transcribe_audio, get_audio_duration_wave
from utils.sentiment import analyze_sentiment
from utils.classification import classify_banking_complaint, CATEGORIES
from utils.analytics import (
    load_interactions,
    save_interaction,
    get_dashboard_metrics,
    create_sentiment_donut_chart,
    create_complaint_bar_chart,
    create_category_sentiment_stacked,
    get_csv_path
)
from utils.voice_auth import verify_customer_voice, DEMO_ENROLLED_PROFILES

# ==============================================================================
# INSTITUTIONAL STYLING (Unslop Design System)
# Palette: Deep Midnight Navy (#080E1E, #0F172A), Crisp Slate (#1E293B),
# Institutional Blue (#2563EB), Pure White (#FFFFFF), Semantic Emerald & Crimson
# ==============================================================================
CUSTOM_CSS = """
<style>
    /* Global Background & Core Font */
    .stApp {
        background-color: #070D1E;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #050914 !important;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1380px;
    }

    /* Typography & Tabular Figures */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    .metric-value {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-variant-numeric: tabular-nums;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.1;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 0.3rem;
    }

    /* Institutional Cards */
    .bank-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        transition: border-color 0.15s ease-in-out;
    }
    .bank-card:hover {
        border-color: #334155;
    }
    .bank-card-highlight {
        background: #0D1B2A;
        border: 1px solid #2563EB;
        border-radius: 8px;
        padding: 1.25rem 1.4rem;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.22rem 0.65rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.18);
        color: #F87171;
        border: 1px solid #EF4444;
    }
    .badge-high {
        background-color: rgba(245, 158, 11, 0.18);
        color: #FBBF24;
        border: 1px solid #F59E0B;
    }
    .badge-medium {
        background-color: rgba(59, 130, 246, 0.18);
        color: #60A5FA;
        border: 1px solid #3B82F6;
    }
    .badge-low {
        background-color: rgba(148, 163, 184, 0.15);
        color: #CBD5E1;
        border: 1px solid #475569;
    }
    .badge-positive {
        background-color: rgba(16, 185, 129, 0.18);
        color: #34D399;
        border: 1px solid #10B981;
    }
    .badge-negative {
        background-color: rgba(239, 68, 68, 0.18);
        color: #F87171;
        border: 1px solid #EF4444;
    }
    .badge-sample {
        background-color: rgba(148, 163, 184, 0.15);
        color: #94A3B8;
        border: 1px dashed #475569;
    }
    .badge-live {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1E40AF !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.15s ease-in-out !important;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
        border-color: #60A5FA !important;
        box-shadow: 0 0 12px rgba(37, 99, 235, 0.35) !important;
    }
    .stDownloadButton > button {
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #1E293B !important;
        border-color: #64748B !important;
    }

    /* Dataframe/Table styling */
    div[data-testid="stDataFrame"] {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
    }

    /* Alert callouts */
    .stAlert {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# STATE INITIALIZATION
# ==============================================================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

if "last_transcription" not in st.session_state:
    st.session_state.last_transcription = None

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None


# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 0.5rem 0 1rem 0;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
                🏛️ <span>BankVoice AI</span>
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;">
                Institutional Voice Analytics
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border: none; border-top: 1px solid #1E293B;' />", unsafe_allow_html=True)

    # Navigation Selection
    nav_options = [
        "📊 Dashboard",
        "🎙️ Voice Analysis",
        "📜 Interaction History",
        "🔐 Voice Biometrics Demo",
        "ℹ️ About Project"
    ]
    
    selected_nav = st.radio(
        "Navigation Menu",
        options=nav_options,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 1.5rem 0 1rem 0; border: none; border-top: 1px solid #1E293B;' />", unsafe_allow_html=True)

    # System Status & Storage Telemetry
    df_current = load_interactions()
    metrics = get_dashboard_metrics(df_current)

    st.markdown(f"""
        <div class="bank-card" style="padding: 0.85rem; margin-bottom: 0.75rem;">
            <div class="metric-label" style="margin-bottom: 0.2rem;">Telemetry Status</div>
            <div style="font-size: 0.82rem; color: #10B981; font-weight: 600;">
                ● Local Models Operational
            </div>
            <div class="metric-sub" style="font-size: 0.75rem; margin-top: 0.4rem;">
                Whisper: Base (Local CPU)<br>
                Sentiment: DistilBERT (HF)<br>
                Dataset: {metrics['total_interactions']} records committed
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Quick Action: Seed Data Reset
    if st.button("🔄 Reload Fictional Sample Data", use_container_width=True):
        from utils.analytics import DATA_FILENAME
        csv_file = get_csv_path()
        # Seed 15 realistic banking customer records
        sample_records = [
            ("INT-8921", "2026-11-01 09:14:22", "Marcus Vance", "call_rec_8921.wav", "Hi, I sent a wire transfer of $1,200 yesterday to my supplier, but the money was deducted twice from my checking account and the receiver only got one.", "Negative", 0.92, "Transaction Issues", "High", True, "Verified (Demo)"),
            ("INT-8922", "2026-11-01 10:45:10", "Elena Rostova", "call_rec_8922.wav", "My chip card keeps getting declined at the grocery store terminal even though I have over five thousand dollars in my checking account.", "Negative", 0.88, "Card Issues", "High", True, "Verified (Demo)"),
            ("INT-8923", "2026-11-01 11:30:45", "David Chen", "call_rec_8923.wav", "Urgent! I noticed three unauthorized debit transactions from a merchant named Global Pay that I never visited. My account was compromised!", "Negative", 0.98, "Fraud Complaints", "Critical", True, "Not Enrolled"),
            ("INT-8924", "2026-11-01 14:15:02", "Sarah Jenkins", "call_rec_8924.wav", "I am calling to enquire about the current fixed interest rate for refinancing my existing thirty-year home mortgage loan and lowering my EMI.", "Positive", 0.76, "Loan Issues", "Low", True, "Verified (Demo)"),
            ("INT-8925", "2026-11-02 08:20:19", "Tariq Al-Mansoor", "call_rec_8925.wav", "My online banking portal was suddenly locked out after I tried logging in from my new office laptop this morning. I need to regain access immediately.", "Negative", 0.85, "Account Issues", "Medium", True, "Verified (Demo)"),
            ("INT-8926", "2026-11-02 11:05:33", "Grace O'Connor", "call_rec_8926.wav", "Good morning, could you please tell me the working hours for the downtown branch and whether certified notary services are available this Saturday?", "Positive", 0.84, "General Enquiries", "Low", True, "Not Enrolled"),
            ("INT-8927", "2026-11-02 13:40:11", "Julian Thorne", "call_rec_8927.wav", "Someone just cloned my platinum credit card and spent $850 at an electronics retailer across the country. Please freeze the card immediately!", "Negative", 0.99, "Fraud Complaints", "Critical", True, "Verified (Demo)"),
            ("INT-8928", "2026-11-02 15:55:40", "Amina Patel", "call_rec_8928.wav", "I unfortunately lost my corporate debit card during my morning commute. I need an expedited replacement card sent to my registered business address.", "Negative", 0.79, "Card Issues", "High", True, "Verified (Demo)"),
            ("INT-8929", "2026-11-03 09:10:04", "Lucas Meyer", "call_rec_8929.wav", "An international wire transfer sent to my business checking account from London four days ago has not reflected yet. The SWIFT reference is TX-44910.", "Negative", 0.91, "Transaction Issues", "High", True, "Not Enrolled"),
            ("INT-8930", "2026-11-03 10:25:50", "Victoria Sterling", "call_rec_8930.wav", "I want to express my appreciation for branch supervisor Rachel who resolved my business escrow account setup yesterday. Truly wonderful and professional service!", "Positive", 0.97, "General Enquiries", "Low", True, "Verified (Demo)"),
            ("INT-8931", "2026-11-03 12:00:15", "Carlos Mendez", "call_rec_8931.wav", "Can you explain why my monthly auto loan repayment jumped by forty-five dollars this billing cycle without any advance disclosure or explanation?", "Negative", 0.89, "Loan Issues", "Medium", True, "Verified (Demo)"),
            ("INT-8932", "2026-11-03 14:18:29", "Hannah Lindqvist", "call_rec_8932.wav", "I need to update my official mailing address and telephone number on my joint savings account before the month-end statements are generated.", "Positive", 0.72, "Account Issues", "Low", True, "Not Enrolled"),
            ("INT-8933", "2026-11-03 16:45:00", "Kwame Mensah", "call_rec_8933.wav", "I received a suspicious phishing SMS pretending to be the bank security department asking for my one-time password and debit card PIN. This is a scam.", "Negative", 0.96, "Fraud Complaints", "Critical", True, "Verified (Demo)"),
            ("INT-8934", "2026-11-04 09:05:42", "Priya Sharma", "call_rec_8934.wav", "The ATM at the corner of 5th Avenue debited two hundred dollars from my savings balance but did not dispense any cash notes. Please reverse the transaction.", "Negative", 0.94, "Transaction Issues", "High", True, "Verified (Demo)"),
            ("INT-8935", "2026-11-04 11:30:18", "Arthur Pendelton", "call_rec_8935.wav", "Thank you so much to your telephone support officer who promptly unblocked my card while I was traveling overseas. The issue was solved in five minutes!", "Positive", 0.95, "Card Issues", "Low", True, "Verified (Demo)")
        ]
        seed_df = pd.DataFrame(sample_records, columns=[
            "interaction_id", "timestamp", "customer_name", "audio_filename",
            "transcript", "sentiment", "sentiment_score", "complaint_category",
            "urgency", "is_sample", "voice_auth_status"
        ])
        seed_df.to_csv(csv_file, index=False)
        st.success("Sample dataset restored (15 records).")
        st.rerun()


# ==============================================================================
# VIEW 1: DASHBOARD
# ==============================================================================
if "Dashboard" in selected_nav:
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem;">
            <div>
                <h1 style="margin: 0; font-size: 1.85rem;">Executive Voice Analytics Dashboard</h1>
                <p style="color: #94A3B8; margin-top: 4px; font-size: 0.92rem;">
                    Institutional monitoring of inbound banking recordings, customer sentiment, and operational complaint vectors.
                </p>
            </div>
            <div style="text-align: right;">
                <span class="badge badge-sample">Source Mode: Consolidated (Sample + Live)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    df = load_interactions()
    metrics = get_dashboard_metrics(df)

    # Metric Row (5 KPI cards)
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
            <div class="bank-card">
                <div class="metric-label">Total Interactions</div>
                <div class="metric-value">{metrics['total_interactions']}</div>
                <div class="metric-sub">{metrics['live_records']} Live • {metrics['sample_records']} Sample</div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div class="bank-card">
                <div class="metric-label">Positive Sentiment</div>
                <div class="metric-value" style="color: #10B981;">{metrics['positive_count']}</div>
                <div class="metric-sub">{metrics['positive_pct']}% of interactions</div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
            <div class="bank-card">
                <div class="metric-label">Negative Sentiment</div>
                <div class="metric-value" style="color: #EF4444;">{metrics['negative_count']}</div>
                <div class="metric-sub">{metrics['negative_pct']}% of interactions</div>
            </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
            <div class="bank-card">
                <div class="metric-label">Primary Complaint</div>
                <div class="metric-value" style="font-size: 1.35rem; color: #60A5FA; padding-top: 0.35rem;">
                    {metrics['top_complaint']}
                </div>
                <div class="metric-sub">{metrics['top_complaint_count']} flagged incidents</div>
            </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
            <div class="bank-card">
                <div class="metric-label">High-Risk Escalations</div>
                <div class="metric-value" style="color: #F87171;">{metrics['critical_fraud_count']}</div>
                <div class="metric-sub">Fraud & Critical urgency</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Visual Analytics Row (Plotly Donut & Horizontal Bar)
    col_chart_left, col_chart_right = st.columns([1, 1.25])

    with col_chart_left:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        donut_fig = create_sentiment_donut_chart(df)
        st.plotly_chart(donut_fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart_right:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        bar_fig = create_complaint_bar_chart(df)
        st.plotly_chart(bar_fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Domain Stacked Analysis Row
    st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
    stacked_fig = create_category_sentiment_stacked(df)
    st.plotly_chart(stacked_fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Recent High-Priority Banking Alerts Feed
    st.markdown("### 🚨 Urgent Compliance & Security Escalations")
    critical_df = df[df["complaint_category"] == "Fraud Complaints"].tail(4).iloc[::-1]

    if critical_df.empty:
        st.info("No active high-risk fraud complaints currently flagged.")
    else:
        for _, row in critical_df.iterrows():
            st.markdown(f"""
                <div class="bank-card" style="border-left: 4px solid #DC2626; margin-bottom: 0.65rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <div>
                            <span class="badge badge-critical">FRAUD ESCALATION</span>
                            <strong style="margin-left: 8px; color: #FFFFFF;">{row['customer_name']}</strong>
                            <span style="color: #64748B; font-size: 0.8rem; margin-left: 6px;">({row['interaction_id']})</span>
                        </div>
                        <span style="color: #94A3B8; font-size: 0.8rem;">{row['timestamp']}</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.9rem; font-style: italic;">
                        "{row['transcript']}"
                    </div>
                </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# VIEW 2: VOICE ANALYSIS (Core Feature)
# ==============================================================================
elif "Voice Analysis" in selected_nav:
    st.markdown("""
        <div>
            <h1 style="margin: 0; font-size: 1.85rem;">Voice Ingestion & Analysis Terminal</h1>
            <p style="color: #94A3B8; margin-top: 4px; font-size: 0.92rem;">
                Ingest customer voice recordings, perform automated speech transcription via OpenAI Whisper, extract sentiment, and categorize banking complaints.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    col_input, col_meta = st.columns([1.4, 1])

    with col_input:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        st.markdown("#### 1. Audio Source Selection")
        
        input_mode = st.radio(
            "Select Audio Ingestion Mode",
            ["📁 Upload Customer Audio File (.wav, .mp3)", "🧪 Load Pre-Recorded Banking Sample Audio"],
            index=1,
            horizontal=True
        )

        audio_file_path = None
        display_filename = None

        if "Upload" in input_mode:
            uploaded_file = st.file_uploader(
                "Upload Customer Voice File",
                type=["wav", "mp3", "m4a"],
                help="Recommended: 16kHz uncompressed WAV format for instantaneous transcription without FFmpeg."
            )
            if uploaded_file is not None:
                # Save uploaded file to temp directory
                suffix = os.path.splitext(uploaded_file.name)[1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    audio_file_path = tmp.name
                display_filename = uploaded_file.name
                st.success(f"File uploaded: **{display_filename}** ({uploaded_file.size / 1024:.1f} KB)")
        else:
            # Preset banking test audio clips
            preset_options = {
                "🚨 Critical Fraud Complaint – Marcus Vance": "sample_fraud_alert.wav",
                "🏡 Mortgage Loan Inquiry – Sarah Jenkins": "sample_loan_inquiry.wav",
                "⭐ Card Support Appreciation – Arthur Pendelton": "sample_card_appreciation.wav"
            }
            chosen_preset = st.selectbox(
                "Choose Banking Scenario Audio",
                list(preset_options.keys())
            )
            sample_rel_path = preset_options[chosen_preset]
            
            # Locate sample file path
            candidates = [
                os.path.join(current_dir, "samples", sample_rel_path),
                os.path.join("samples", sample_rel_path),
                os.path.join("bankvoice-ai", "samples", sample_rel_path)
            ]
            for cand in candidates:
                if os.path.exists(cand):
                    audio_file_path = os.path.abspath(cand)
                    break
            display_filename = sample_rel_path

        # Audio Player Preview
        if audio_file_path and os.path.exists(audio_file_path):
            st.markdown("<div style='margin-top: 0.8rem;'><strong>Audio Playback:</strong></div>", unsafe_allow_html=True)
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/wav")
        else:
            st.info("Please select or upload an audio recording to proceed.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_meta:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        st.markdown("#### 2. Caller Context & Identity")
        
        customer_name_input = st.text_input(
            "Customer Full Name",
            value="Marcus Vance" if "Fraud" in str(display_filename) else ("Sarah Jenkins" if "Loan" in str(display_filename) else "Arthur Pendelton")
        )
        
        claimed_identity = st.selectbox(
            "Claimed Identity for Voice Verification (Demo)",
            options=list(DEMO_ENROLLED_PROFILES.keys()) + ["Unenrolled Caller (Simulate Failure)"],
            index=0 if "Marcus" in customer_name_input else (3 if "Sarah" in customer_name_input else 1)
        )
        
        whisper_tier = st.selectbox(
            "Whisper Model Tier",
            ["base (Balanced, ~74M params)", "tiny (Fastest, ~39M params)"],
            index=0
        )
        selected_model = "base" if "base" in whisper_tier else "tiny"

        st.markdown("""
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 0.75rem;">
                ℹ️ Audio will be transcribed locally on CPU using OpenAI Whisper. Sentiment evaluated via Hugging Face Transformers.
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ANALYSE VOICE ACTION BUTTON
    analyse_btn = st.button("⚡ Analyse Voice Recording", use_container_width=True)

    if analyse_btn:
        if not audio_file_path or not os.path.exists(audio_file_path):
            st.error("No valid audio file selected. Please upload or choose a banking recording.")
        else:
            with st.spinner("Processing speech transcription with OpenAI Whisper..."):
                t_start = time.time()
                transcription_result = transcribe_audio(audio_file_path, model_name=selected_model)
                t_elapsed = round(time.time() - t_start, 2)

            if transcription_result["status"] == "error":
                st.error(f"⚠️ {transcription_result['error_message']}")
            else:
                transcript_text = transcription_result["transcript"]

                # Perform Sentiment Analysis
                with st.spinner("Analyzing customer sentiment with Hugging Face Transformers..."):
                    sentiment_result = analyze_sentiment(transcript_text)

                # Perform Complaint Domain Categorization
                complaint_result = classify_banking_complaint(transcript_text)

                # Perform Speaker Verification Demonstration
                claimed_target = claimed_identity.split(" (")[0]
                auth_result = verify_customer_voice(audio_file_path, claimed_target)

                # Store into Session State
                st.session_state.last_analysis = {
                    "interaction_id": f"INT-{int(time.time()) % 10000:04d}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "customer_name": customer_name_input.strip() or "Caller",
                    "audio_filename": display_filename or "audio.wav",
                    "transcript": transcript_text,
                    "sentiment": sentiment_result["sentiment"],
                    "sentiment_score": float(sentiment_result["score"]),
                    "complaint_category": complaint_result["category"],
                    "urgency": complaint_result["urgency"],
                    "matched_keywords": complaint_result["matched_keywords"],
                    "is_sample": False,  # Live uploaded/processed recording
                    "voice_auth_status": "Verified (Demo)" if auth_result["is_verified"] else "Failed Match",
                    "auth_details": auth_result,
                    "transcription_meta": transcription_result,
                    "sentiment_engine": sentiment_result.get("engine", "Transformers"),
                    "elapsed_sec": t_elapsed
                }

    # ==========================================================================
    # DISPLAY ANALYSIS RESULTS
    # ==========================================================================
    if st.session_state.last_analysis:
        res = st.session_state.last_analysis
        st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #1E293B;' />", unsafe_allow_html=True)
        st.markdown(f"### 📋 Analytical Intelligence Report – {res['interaction_id']}")

        # Primary Metrics Row
        r1, r2, r3, r4 = st.columns(4)
        
        with r1:
            sent_badge = "badge-positive" if res["sentiment"] == "Positive" else "badge-negative"
            st.markdown(f"""
                <div class="bank-card">
                    <div class="metric-label">Customer Sentiment</div>
                    <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.35rem;">
                        <span class="badge {sent_badge}">{res['sentiment']}</span>
                    </div>
                    <div class="metric-sub">Confidence: <strong>{res['sentiment_score'] * 100:.1f}%</strong></div>
                    <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">{res['sentiment_engine']}</div>
                </div>
            """, unsafe_allow_html=True)

        with r2:
            urg_class = {
                "Critical": "badge-critical",
                "High": "badge-high",
                "Medium": "badge-medium",
                "Low": "badge-low"
            }.get(res["urgency"], "badge-low")

            st.markdown(f"""
                <div class="bank-card">
                    <div class="metric-label">Banking Complaint Vector</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.35rem;">
                        {res['complaint_category']}
                    </div>
                    <div class="metric-sub">Urgency: <span class="badge {urg_class}">{res['urgency']}</span></div>
                </div>
            """, unsafe_allow_html=True)

        with r3:
            auth_det = res.get("auth_details", {})
            auth_color = "#10B981" if auth_det.get("is_verified") else "#EF4444"
            st.markdown(f"""
                <div class="bank-card">
                    <div class="metric-label">Voice Biometrics (Demo)</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {auth_color}; margin-bottom: 0.35rem;">
                        {auth_det.get('status_label', 'Evaluated')}
                    </div>
                    <div class="metric-sub">Cosine Match: <strong>{auth_det.get('similarity_percent', 'N/A')}</strong></div>
                    <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">Profile: {auth_det.get('enrolled_id', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)

        with r4:
            t_meta = res.get("transcription_meta", {})
            st.markdown(f"""
                <div class="bank-card">
                    <div class="metric-label">Audio Telemetry</div>
                    <div style="font-size: 1.45rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.35rem;">
                        {t_meta.get('duration', 0.0):.1f}s
                    </div>
                    <div class="metric-sub">{t_meta.get('word_count', 0)} words • Whisper {res.get('elapsed_sec', 0)}s latency</div>
                </div>
            """, unsafe_allow_html=True)

        # Full Transcript Display Card
        st.markdown(f"""
            <div class="bank-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <div class="metric-label" style="margin-bottom: 0;">Speech-to-Text Transcript (OpenAI Whisper)</div>
                    <span class="badge badge-sample">Lang: {t_meta.get('language', 'en').upper()}</span>
                </div>
                <div style="background-color: #050914; border: 1px solid #1E293B; border-radius: 6px; padding: 1rem; color: #F1F5F9; font-size: 0.95rem; line-height: 1.6;">
                    "{res['transcript']}"
                </div>
                <div style="margin-top: 0.75rem; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.8rem; color: #94A3B8;">Matched Keywords:</span>
                    {' '.join([f'<span class="badge badge-low">{kw}</span>' for kw in res.get('matched_keywords', [])]) or '<span style="color:#64748B; font-size:0.8rem;">None (General Query)</span>'}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Voice Biometrics Prototype Disclaimer Callout
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.4); border-left: 3px solid #64748B; padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; color: #94A3B8; margin-bottom: 1rem;">
                ⚠️ <strong>Voice Biometric Demonstration Note:</strong> The speaker verification match score reflects acoustic spectral cosine similarity computed for architectural demonstration. Speech recognition and sentiment analysis do not authenticate identity.
            </div>
        """, unsafe_allow_html=True)

        # Persistence Action Button
        save_col1, save_col2 = st.columns([1, 2])
        with save_col1:
            if st.button("💾 Commit to Interaction Database", use_container_width=True):
                # Prepare record for CSV persistence
                record_to_save = {
                    "interaction_id": res["interaction_id"],
                    "timestamp": res["timestamp"],
                    "customer_name": res["customer_name"],
                    "audio_filename": res["audio_filename"],
                    "transcript": res["transcript"],
                    "sentiment": res["sentiment"],
                    "sentiment_score": res["sentiment_score"],
                    "complaint_category": res["complaint_category"],
                    "urgency": res["urgency"],
                    "is_sample": False,
                    "voice_auth_status": res["voice_auth_status"]
                }
                ok = save_interaction(record_to_save)
                if ok:
                    st.success(f"Interaction {res['interaction_id']} committed to {get_csv_path()}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to commit interaction to disk.")


# ==============================================================================
# VIEW 3: INTERACTION HISTORY
# ==============================================================================
elif "Interaction History" in selected_nav:
    st.markdown("""
        <div>
            <h1 style="margin: 0; font-size: 1.85rem;">Banking Interaction Audit History</h1>
            <p style="color: #94A3B8; margin-top: 4px; font-size: 0.92rem;">
                Permanent audit log of customer voice interactions stored in local CSV storage.
            </p>
        </div>
    """, unsafe_allow_html=True)

    df_history = load_interactions()

    if df_history.empty:
        st.warning("No interactions recorded in the database. Run a voice analysis or reload sample data from the sidebar.")
    else:
        # Search and Filtering Controls
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_query = st.text_input("🔍 Search Transcripts or Customer Names", "")
        with f2:
            cat_filter = st.selectbox(
                "Filter Domain",
                ["All Categories"] + list(CATEGORIES.keys())
            )
        with f3:
            sent_filter = st.selectbox(
                "Filter Sentiment",
                ["All Sentiments", "Positive", "Negative"]
            )

        filtered = df_history.copy()
        if search_query:
            q = search_query.lower()
            filtered = filtered[
                filtered["customer_name"].str.lower().str.contains(q, na=False) |
                filtered["transcript"].str.lower().str.contains(q, na=False) |
                filtered["interaction_id"].str.lower().str.contains(q, na=False)
            ]
        if cat_filter != "All Categories":
            filtered = filtered[filtered["complaint_category"] == cat_filter]
        if sent_filter != "All Sentiments":
            filtered = filtered[filtered["sentiment"] == sent_filter]

        st.markdown(f"Displaying **{len(filtered)}** of **{len(df_history)}** interactions:")

        # Display Dataframe with custom column configurations
        display_cols = [
            "interaction_id", "timestamp", "customer_name", "complaint_category",
            "sentiment", "sentiment_score", "urgency", "is_sample", "voice_auth_status", "transcript"
        ]
        
        st.dataframe(
            filtered[display_cols],
            column_config={
                "interaction_id": st.column_config.TextColumn("ID", width="small"),
                "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                "customer_name": st.column_config.TextColumn("Customer", width="medium"),
                "complaint_category": st.column_config.TextColumn("Category", width="medium"),
                "sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                "sentiment_score": st.column_config.NumberColumn("Score", format="%.2f", width="small"),
                "urgency": st.column_config.TextColumn("Urgency", width="small"),
                "is_sample": st.column_config.CheckboxColumn("Sample Record", width="small"),
                "voice_auth_status": st.column_config.TextColumn("Biometric Status", width="medium"),
                "transcript": st.column_config.TextColumn("Transcript", width="large")
            },
            hide_index=True,
            use_container_width=True,
            height=420
        )

        # Export CSV Button
        csv_bytes = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Interactions (CSV)",
            data=csv_bytes,
            file_name=f"bankvoice_interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


# ==============================================================================
# VIEW 4: VOICE BIOMETRICS DEMO
# ==============================================================================
elif "Voice Biometrics" in selected_nav:
    st.markdown("""
        <div>
            <h1 style="margin: 0; font-size: 1.85rem;">Customer Voice Authentication Sandbox</h1>
            <p style="color: #94A3B8; margin-top: 4px; font-size: 0.92rem;">
                Acoustic feature extraction and speaker similarity verification demonstration.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 3px solid #3B82F6; padding: 1rem 1.25rem; border-radius: 6px; margin: 1rem 0;">
            <strong style="color: #FFFFFF;">⚠️ Demonstration Disclaimer:</strong>
            <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 4px;">
                This module demonstrates how banking applications can compute speaker similarity scores using acoustic spectral centroid and pitch signatures. 
                In enterprise banking environments, this is combined with FIDO2 hardware tokens and cryptographically backed biometric models. 
                Neither speech-to-text nor sentiment analysis represents authentication.
            </div>
        </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns([1, 1.2])

    with b1:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        st.markdown("#### Enrolled Banking Voiceprints")
        st.markdown("Select a customer identity to test acoustic match against:")

        target_customer = st.selectbox(
            "Claimed Identity",
            list(DEMO_ENROLLED_PROFILES.keys())
        )
        
        prof = DEMO_ENROLLED_PROFILES[target_customer]
        st.markdown(f"""
            <div style="background: #050914; padding: 0.85rem; border-radius: 6px; border: 1px solid #1E293B; font-size: 0.85rem; line-height: 1.8; margin: 0.8rem 0;">
                <strong>Profile ID:</strong> {prof['enrolled_id']}<br>
                <strong>Nominal Fundamental Frequency:</strong> {prof['nominal_pitch']} Hz<br>
                <strong>Target Spectral Centroid:</strong> {prof['spectral_centroid']} Hz<br>
                <strong>Baseline Energy Signature:</strong> {prof['energy_signature']}
            </div>
        """, unsafe_allow_html=True)

        verify_threshold = st.slider("Verification Decision Threshold", min_value=0.50, max_value=0.95, value=0.75, step=0.05)
        st.markdown("</div>", unsafe_allow_html=True)

    with b2:
        st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
        st.markdown("#### Test Voice Sample")

        test_audio_sample = st.selectbox(
            "Select Audio Sample to Verify",
            [
                "sample_fraud_alert.wav (Spoken by Marcus Vance)",
                "sample_loan_inquiry.wav (Spoken by Sarah Jenkins)",
                "sample_card_appreciation.wav (Spoken by Arthur Pendelton)"
            ]
        )
        
        rel_fn = test_audio_sample.split(" ")[0]
        test_path = os.path.join(current_dir, "samples", rel_fn)
        if not os.path.exists(test_path):
            test_path = os.path.join("samples", rel_fn)

        if os.path.exists(test_path):
            with open(test_path, "rb") as f:
                st.audio(f.read(), format="audio/wav")

        if st.button("🔍 Run Biometric Comparison", use_container_width=True):
            auth_res = verify_customer_voice(test_path, target_customer, threshold=verify_threshold)
            
            sim = auth_res["similarity_score"]
            is_pass = auth_res["is_verified"]

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if is_pass:
                st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 6px; padding: 1rem;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #34D399;">
                            ✅ AUTHENTICATION PASSED (Demo)
                        </div>
                        <div style="color: #E2E8F0; font-size: 0.9rem; margin-top: 4px;">
                            Similarity Score: <strong>{auth_res['similarity_percent']}</strong> (Threshold: {verify_threshold * 100:.0f}%)
                        </div>
                        <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">
                            {auth_res['confidence_level']} – Voice biometric parameters fall within acceptable institutional tolerance.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 6px; padding: 1rem;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #F87171;">
                            ❌ BIOMETRIC MISMATCH DETECTED (Demo)
                        </div>
                        <div style="color: #E2E8F0; font-size: 0.9rem; margin-top: 4px;">
                            Similarity Score: <strong>{auth_res['similarity_percent']}</strong> (Required: {verify_threshold * 100:.0f}%)
                        </div>
                        <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">
                            The speaker's acoustic fingerprint deviates from enrolled customer profile {prof['enrolled_id']}. Step-up authentication required.
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 5: ABOUT PROJECT
# ==============================================================================
elif "About Project" in selected_nav:
    st.markdown("""
        <div>
            <h1 style="margin: 0; font-size: 1.85rem;">About BankVoice AI</h1>
            <p style="color: #94A3B8; margin-top: 4px; font-size: 0.92rem;">
                Institutional speech-to-text, customer sentiment analysis, and risk categorization engine.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    a1, a2 = st.columns(2)

    with a1:
        st.markdown("""
            <div class="bank-card">
                <h4>System Architecture</h4>
                <div style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.7;">
                    BankVoice AI is designed for private on-premise banking analytics with zero external API data transmission:
                    <ul style="margin-top: 8px;">
                        <li><strong>Speech-to-Text:</strong> Local OpenAI Whisper model (CPU-optimized float32 inference).</li>
                        <li><strong>Sentiment Extraction:</strong> Hugging Face Transformers DistilBERT with heuristic fallback.</li>
                        <li><strong>Complaint Classification:</strong> Multi-tiered weighted keyword classifier detecting 6 institutional domains.</li>
                        <li><strong>Analytics Telemetry:</strong> Interactive Plotly visualization engine with persistent CSV storage.</li>
                        <li><strong>Voice Biometrics:</strong> Prototype speaker verification module based on acoustic spectral matching.</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
            <div class="bank-card">
                <h4>Compliance & Privacy Posture</h4>
                <div style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.7;">
                    In accordance with banking regulatory standards (GDPR, GLBA, PCI-DSS):
                    <ul style="margin-top: 8px;">
                        <li>Audio files are decoded locally without transmitting raw voice biometric data to public cloud APIs.</li>
                        <li>Complaints are automatically screened for high-risk Fraud indicators to facilitate regulatory SAR escalation.</li>
                        <li>Data persistence is maintained on local disk (<code>data/interactions.csv</code>) with full audit visibility.</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="bank-card">
            <h4>Technology Stack</h4>
            <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px;">
                <span class="badge badge-low">Python 3.10+</span>
                <span class="badge badge-low">Streamlit 1.30+</span>
                <span class="badge badge-low">OpenAI Whisper</span>
                <span class="badge badge-low">Hugging Face Transformers</span>
                <span class="badge badge-low">PyTorch</span>
                <span class="badge badge-low">Pandas</span>
                <span class="badge badge-low">Plotly Interactive</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

