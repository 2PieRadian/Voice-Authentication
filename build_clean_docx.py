"""
Generate pristine, formal, executive docx documents with:
- ZERO colored text (all text strictly black)
- ZERO background fills / shading (all white / transparent)
- ZERO emojis
- Clean, standard professional typography and borders
"""

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

GITHUB_URL = "https://github.com/2PieRadian/Voice-Authentication"

def create_formal_document(filename):
    doc = Document()

    # Page Margins: Standard 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header (Standard Formal)
        section.header.is_linked_to_previous = False
        hp = section.header.paragraphs[0]
        hp.text = "BANKVOICE AI - EXECUTIVE TECHNICAL SPECIFICATION"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Times New Roman"
        hp.style.font.size = Pt(8.5)
        hp.style.font.bold = False

        # Footer (Standard Page number)
        section.footer.is_linked_to_previous = False
        fp = section.footer.paragraphs[0]
        fp.text = "CONFIDENTIAL & PROPRIETARY - BANKING ANALYTICS & VOICE INTELLIGENCE"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.style.font.name = "Times New Roman"
        fp.style.font.size = Pt(8)

    BLACK = RGBColor(0, 0, 0)

    def style_p(p, space_after=4, space_before=0, line_spacing=1.15):
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing

    # Title
    p_title = doc.add_paragraph()
    style_p(p_title, space_after=2, space_before=12)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BANKVOICE AI")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = BLACK

    # Subtitle
    p_sub = doc.add_paragraph()
    style_p(p_sub, space_after=12, space_before=0)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Customer Voice Authentication & Banking Analytics Platform\nExecutive Project Synopsis & Technical Architecture Specification")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = BLACK

    # GitHub Repository Link Box (Clean Black Border, NO background color)
    table_gh = doc.add_table(rows=1, cols=1)
    table_gh.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_gh = table_gh.cell(0, 0)
    cell_gh.width = Inches(6.5)
    tcPr = cell_gh._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        r'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        r'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p_gh = cell_gh.paragraphs[0]
    p_gh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_p(p_gh, space_after=4, space_before=4)
    r_gh1 = p_gh.add_run("Project Repository: ")
    r_gh1.font.name = "Times New Roman"
    r_gh1.font.size = Pt(10.5)
    r_gh1.font.bold = True
    r_gh1.font.color.rgb = BLACK

    r_gh2 = p_gh.add_run(GITHUB_URL)
    r_gh2.font.name = "Times New Roman"
    r_gh2.font.size = Pt(10.5)
    r_gh2.font.bold = True
    r_gh2.font.underline = True
    r_gh2.font.color.rgb = BLACK

    p_space = doc.add_paragraph()
    style_p(p_space, space_after=10, space_before=0)

    def add_h1(text):
        p = doc.add_paragraph()
        style_p(p, space_after=6, space_before=14)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = BLACK
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        style_p(p, space_after=4, space_before=10)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = BLACK
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        style_p(p, space_after=5, space_before=0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            b = p.add_run(bold_prefix)
            b.font.name = "Times New Roman"
            b.font.size = Pt(10.5)
            b.font.bold = True
            b.font.color.rgb = BLACK
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.color.rgb = BLACK
        return p

    def add_bullet(text, bold_title=None):
        p = doc.add_paragraph(style='List Bullet')
        style_p(p, space_after=3, space_before=0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_title:
            b = p.add_run(bold_title + " ")
            b.font.name = "Times New Roman"
            b.font.size = Pt(10.5)
            b.font.bold = True
            b.font.color.rgb = BLACK
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.color.rgb = BLACK
        return p

    # SECTION 1
    add_h1("1. Executive Summary & Problem Formulation")
    add_body(
        "Commercial banking institutions process tens of thousands of inbound audio customer calls each business day. "
        "These voice streams contain urgent operational intelligence: unauthorized transactions, account compromise reports, "
        "card hardware failures, payment settlement delays, and customer dissatisfaction indicators. However, because raw telephony audio "
        "is unstructured and transient, banking contact centers face a critical bottleneck: less than three percent of calls are ever audited "
        "due to the resource constraints of manual sampling."
    )
    add_body(
        "BankVoice AI resolves this operational blind spot by providing an automated, on-premise analytics pipeline that converts "
        "spoken customer interactions into structured, auditable banking data in real time. The entire application runs locally on CPU "
        "without transmitting audio recordings to external public cloud APIs, ensuring strict compliance with financial data residency "
        "and privacy mandates, including GDPR, GLBA, and PCI-DSS."
    )

    # SECTION 2
    add_h1("2. Technology Stack & Architectural Roles")
    table = doc.add_table(rows=7, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["System Layer", "Technology Utilized", "Operational Responsibility"]
    
    # Header Row
    for i, title in enumerate(hdrs):
        cell = table.rows[0].cells[i]
        cell.text = title
        p = cell.paragraphs[0]
        style_p(p, space_after=3, space_before=3)
        run = p.runs[0]
        run.font.name = "Times New Roman"
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = BLACK

    tech_data = [
        ("User Interface", "Streamlit", "Executive banking dashboard, interactive controls, and visual telemetry"),
        ("Speech-to-Text", "OpenAI Whisper (base/tiny)", "On-premise neural acoustic transcription via log-mel spectrograms"),
        ("Sentiment Engine", "Hugging Face Transformers (DistilBERT)", "Contextual polarity classification and calibrated probability calculation"),
        ("Complaint Classifier", "Multi-Keyword Weighted Matrix", "Automated sorting into 6 statutory banking complaint domains"),
        ("Voice Biometrics", "Acoustic Spectral Centroid Vectors", "Speaker verification demonstration evaluating cosine similarity"),
        ("Data Persistence", "Pandas & Local CSV Storage", "Stateful transaction logging, audit tracking, and metric aggregation")
    ]

    for r_idx, r_val in enumerate(tech_data):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            style_p(p, space_after=2, space_before=2)
            run = p.runs[0]
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.color.rgb = BLACK
            if c_idx == 0:
                run.font.bold = True

    # Apply simple standard black borders to table
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        r'<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        r'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'<w:left w:val="none"/>'
        r'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        r'<w:right w:val="none"/>'
        r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        r'<w:insideV w:val="none"/>'
        r'</w:tblBorders>'
    )
    tblPr.append(borders)

    p_sp = doc.add_paragraph()
    style_p(p_sp, space_after=6, space_before=4)

    # SECTION 3
    add_h1("3. End-to-End Processing Pipeline")
    add_bullet(
        "Standardizes inbound audio (WAV, MP3, M4A) into uncompressed 16 kHz mono 32-bit floating-point linear streams. A custom native wave PCM decoder processes uncompressed WAV files directly in software, removing the external OS-level FFmpeg requirement.",
        "Stage 1: Signal Ingestion & Decoding:"
    )
    add_bullet(
        "Decomposes sound waves into 80-channel log-mel frequency spectrograms. Passes the spectrogram into an encoder-decoder transformer architecture to produce an accurate English textual transcript, robust against regional accents and ambient line noise.",
        "Stage 2: Neural Speech-to-Text:"
    )
    add_bullet(
        "Applies bidirectional self-attention across the transcript to evaluate caller emotional state (Positive vs. Negative). Outputs Softmax-calibrated probability percentages (e.g., Negative: 99.2%) and activates a deterministic lexicon failover if models are offline.",
        "Stage 3: Contextual Sentiment Scoring:"
    )
    add_bullet(
        "Maps transcripts into 6 regulated banking domains: Fraud Complaints (Critical), Transaction Issues (High), Card Issues (High), Loan Issues (Medium), Account Issues (Medium), or General Enquiries (Low). Any detected fraud indicators automatically take legal precedence.",
        "Stage 4: Complaint Taxonomy & Priority Triage:"
    )
    add_bullet(
        "Extracts 64-band spectral centroid and energy distribution vectors from the caller's acoustic waveform, computing the cosine angle against enrolled profiles to demonstrate speaker verification concepts.",
        "Stage 5: Voice Biometrics Demonstration:"
    )
    add_bullet(
        "Permanently records interactions into a local CSV ledger (data/interactions.csv) and computes real-time executive KPIs (total interactions, positive ratio, primary complaint vector, and urgent fraud escalations).",
        "Stage 6: Persistent Ledger & Executive Telemetry:"
    )

    # SECTION 4
    add_h1("4. Technical Mechanics & Concepts (Detailed Formulation)")
    
    add_h2("4.1 Digital Audio Normalization")
    add_body(
        "Human voice frequencies typically lie between 80 Hz and 7,500 Hz. Following the Nyquist-Shannon sampling theorem, "
        "a sampling rate of 16,000 samples per second (16 kHz) fully reconstructs the acoustic speech signal without loss. "
        "Incoming multi-channel telephony audio is collapsed into a single mono channel, and sample amplitudes are normalized "
        "into the floating-point range [-1.0, 1.0] to standardize audio energy across varying recording volumes."
    )

    add_h2("4.2 The Log-Mel Spectrogram and Attention Transformers")
    add_body(
        "Human pitch perception is non-linear; the ear discriminates lower frequencies with far greater sensitivity than high frequencies. "
        "The speech pipeline computes Short-Time Fourier Transforms (STFT) across overlapping 25-millisecond windows and filters the resulting "
        "frequencies through an 80-channel Mel filter bank. Taking the logarithm of energy levels creates a Log-Mel Spectrogram—a two-dimensional "
        "frequency-time representation of speech."
    )
    add_body(
        "The OpenAI Whisper model passes this representation through an acoustic encoder to capture phonetic and temporal context. "
        "The autoregressive decoder then applies cross-attention over the encoder states and causal self-attention over preceding tokens, "
        "predicting words in sequential order while respecting grammatical and conversational probabilities."
    )

    add_h2("4.3 Bidirectional Natural Language Understanding")
    add_body(
        "Unlike legacy lexicon counters that fail when encountering negation or complex banking phrasing, DistilBERT uses bidirectional "
        "self-attention. Every token attends to all preceding and subsequent tokens simultaneously, allowing the network to distinguish "
        "context-dependent meanings (e.g., 'dispute the unauthorized charge' vs. 'charge my mobile device'). "
        "The output logits are normalized through a Softmax function, yielding a calibrated confidence score."
    )

    add_h2("4.4 Statutory Complaint Precedence Arbitration")
    add_body(
        "When an interaction contains keywords from multiple domains (e.g., 'My debit card had an unauthorized withdrawal'), "
        "the classifier applies weighted keyword density scoring where multi-word technical phrases receive higher mathematical priority. "
        "Furthermore, to support regulatory compliance regarding Suspicious Activity Reports (SAR), any detection of fraudulent keywords "
        "strictly overrides operational categories and escalates the interaction to 'Fraud Complaints' at 'Critical' urgency."
    )

    add_h2("4.5 Acoustic Feature Vectors and Cosine Similarity")
    add_body(
        "Human voices are shaped by physiological vocal tract geometry, nasal cavity volume, and vocal cord vibration rates (glottal pulses). "
        "These structures generate distinct resonant frequency bands known as formants. The biometric demonstration module decomposes "
        "the speaker's audio into 64 discrete frequency bands to compute a normalized spectral centroid vector."
    )
    add_body(
        "Verification is conducted by calculating the Cosine Similarity—the cosine of the angle between the caller's acoustic vector and "
        "the enrolled customer profile. If the angle is near zero (cosine approaching 1.0), the acoustic characteristics match the enrolled "
        "profile. A score below the decision threshold (e.g., 0.75) flags a voiceprint mismatch, requiring step-up identity authentication."
    )

    # SECTION 5
    add_h1("5. Regulatory Demarcation & Security Disclaimers")
    add_body(
        "It is critical to establish the architectural demarcation between speech processing and identity authentication. "
        "Neither speech recognition (transcription) nor sentiment analysis authenticates a customer's identity; transcribing what was said "
        "provides no proof of who is speaking. The speaker verification module represents an educational proof-of-concept demonstrating "
        "acoustic spectral matching. In production commercial banking, voice biometrics must be integrated with anti-spoofing liveness "
        "detection (to defend against synthetic AI voice clones), secure hardware enclaves, and FIDO2 cryptographic tokens."
    )

    # SECTION 6
    add_h1("6. Execution and Verification Guide")
    add_body(
        "The application is entirely self-contained and operates locally using the following commands:",
        bold_prefix="Standard Execution: "
    )
    add_bullet("1. Clone Repository: git clone https://github.com/2PieRadian/Voice-Authentication.git")
    add_bullet("2. Install Dependencies: pip install -r requirements.txt")
    add_bullet("3. Launch Dashboard: streamlit run app.py (accessible locally at http://localhost:8501)")

    doc.save(filename)
    return filename

if __name__ == "__main__":
    import os
    f1 = create_formal_document("Project_Synopsis.docx")
    print(f"Generated clean formal document: {f1}")
    f2 = create_formal_document("BankVoice_AI_Technical_Architecture_Document.docx")
    print(f"Generated clean formal document: {f2}")
    
    bv_dir = "bankvoice-ai"
    if os.path.exists(bv_dir):
        f3 = create_formal_document(os.path.join(bv_dir, "Project_Synopsis.docx"))
        print(f"Generated clean formal document: {f3}")
        f4 = create_formal_document(os.path.join(bv_dir, "BankVoice_AI_Technical_Architecture_Document.docx"))
        print(f"Generated clean formal document: {f4}")
