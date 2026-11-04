"""
Generator script for the BankVoice AI Comprehensive Technical Architecture Whitepaper (.docx)
Creates a beautifully formatted, executive-level technical document explaining
the full concept and mechanics without code snippets.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_whitepaper(filename="BankVoice_AI_Technical_Architecture_Document.docx"):
    doc = Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header.is_linked_to_previous = False
        # Add subtle header
        hp = section.header.paragraphs[0]
        hp.text = "BankVoice AI — Institutional Technical Architecture & Concepts"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Calibri"
        hp.style.font.size = Pt(8.5)
        hp.style.font.color.rgb = RGBColor(148, 163, 184)

    # Color Palette Definitions
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    BLUE = RGBColor(37, 99, 235)      # #2563EB
    DARK_BLUE = RGBColor(30, 58, 138) # #1E3A8A
    BODY_COLOR = RGBColor(30, 41, 59) # #1E293B
    MUTED = RGBColor(100, 116, 139)   # #64748B
    CRIMSON = RGBColor(220, 38, 38)   # #DC2626
    EMERALD = RGBColor(16, 185, 129)  # #10B981

    def style_paragraph(p, space_after=6, space_before=0, line_spacing=1.15):
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_paragraph(p, space_after=4, space_before=24)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_paragraph(p, space_after=18, space_before=0)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.color.rgb = BLUE
        run.font.bold = True
        return p

    def add_meta_block():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_paragraph(p, space_after=28, space_before=0)
        run = p.add_run("Executive Technical Whitepaper & Architectural Specification\nVersion 1.0  |  Enterprise Banking Analytics & Voice Intelligence")
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = MUTED
        
        # Horizontal Rule
        p_hr = doc.add_paragraph()
        style_paragraph(p_hr, space_after=20, space_before=0)
        p_hr_border = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:bottom w:val="single" w:sz="12" w:space="1" w:color="2563EB"/></w:pBdr>')
        p_hr._p.get_or_add_pPr().append(p_hr_border)

    def add_h1(text):
        p = doc.add_paragraph()
        style_paragraph(p, space_after=8, space_before=18)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        style_paragraph(p, space_after=6, space_before=12)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = DARK_BLUE
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        style_paragraph(p, space_after=6, space_before=0)
        if bold_prefix:
            b_run = p.add_run(bold_prefix)
            b_run.font.name = "Calibri"
            b_run.font.size = Pt(11)
            b_run.font.bold = True
            b_run.font.color.rgb = NAVY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = BODY_COLOR
        return p

    def add_bullet(text, bold_title=None):
        p = doc.add_paragraph(style='List Bullet')
        style_paragraph(p, space_after=4, space_before=0)
        if bold_title:
            b_run = p.add_run(bold_title + " ")
            b_run.font.name = "Calibri"
            b_run.font.size = Pt(11)
            b_run.font.bold = True
            b_run.font.color.rgb = NAVY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = BODY_COLOR
        return p

    def add_callout(title, text, is_warning=False):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        
        # Border & background xml
        border_color = "DC2626" if is_warning else "2563EB"
        bg_color = "FEF2F2" if is_warning else "F8FAFC"
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                              f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
                              f'<w:top w:val="none"/>'
                              f'<w:right w:val="none"/>'
                              f'<w:bottom w:val="none"/>'
                              f'</w:tcBorders>')
        tcShd = parse_xml(f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:color="auto" w:fill="{bg_color}"/>')
        tcPr.append(tcBorders)
        tcPr.append(tcShd)

        cp = cell.paragraphs[0]
        style_paragraph(cp, space_after=3, space_before=4)
        run_title = cp.add_run(title)
        run_title.font.name = "Arial"
        run_title.font.size = Pt(10.5)
        run_title.font.bold = True
        run_title.font.color.rgb = CRIMSON if is_warning else DARK_BLUE

        cp_body = cell.add_paragraph()
        style_paragraph(cp_body, space_after=4, space_before=0)
        run_text = cp_body.add_run(text)
        run_text.font.name = "Calibri"
        run_text.font.size = Pt(10)
        run_text.font.color.rgb = BODY_COLOR

        p_space = doc.add_paragraph()
        style_paragraph(p_space, space_after=6, space_before=0)

    # --- DOCUMENT GENERATION ---

    add_title("BankVoice AI")
    add_subtitle("Architectural Blueprint & Conceptual Foundations of Voice-Driven Banking Intelligence")
    add_meta_block()

    # SECTION 1
    add_h1("1. Executive Overview & The Banking Operational Challenge")
    add_body(
        "Commercial banking institutions process tens of thousands of inbound audio telephony interactions every business day. "
        "These audio recordings encapsulate high-stakes operational signals: identity claims, urgent fraud reports, card terminal failures, "
        "wire transfer disputes, loan restructuring queries, and customer satisfaction levels. However, because raw audio is unstructured, "
        "transient, and dense, traditional banking contact centers face a structural operational blind spot."
    )
    add_body(
        "Ordinarily, compliance supervisors and risk officers are forced to perform manual, retrospective sampling—auditing fewer than "
        "three percent of recorded phone calls days or weeks after the conversation occurred. In critical scenarios, such as unauthorized card cloning "
        "or identity theft, this audit latency results in irreversible capital loss and regulatory compliance penalties under financial protection mandates."
    )
    add_body(
        "BankVoice AI solves this systemic latency by introducing an automated, multi-stage analytical pipeline that converts raw spoken interactions "
        "into structured, categorized, and auditable operational intelligence in real time. The solution integrates five foundational disciplines: "
        "digital audio stream reconstruction, neural acoustic transcription, contextual sentiment classification, regulated complaint taxonomy mapping, "
        "and acoustic voiceprint verification."
    )

    # SECTION 2
    add_h1("2. End-to-End System Architecture: The Five-Stage Intelligence Pipeline")
    add_body(
        "The system operates through five tightly orchestrated sequential stages, transforming chaotic acoustic waves into structured risk metrics:"
    )
    add_bullet(
        "Converts uploaded recordings (.wav, .mp3, .m4a) into standardized pulse-code modulation (PCM) linear float arrays, resampled to exactly 16,000 Hz in mono format.",
        "Stage 1: Audio Signal Conditioning & Ingestion —"
    )
    add_bullet(
        "Converts conditioned audio frames into an auditory time-frequency log-mel spectrogram, passing it through deep encoder-decoder attention blocks to transcribe exact human speech into text.",
        "Stage 2: Neural Speech-to-Text Transcription (Whisper) —"
    )
    add_bullet(
        "Processes the textual transcript through bidirectional transformer attention heads to evaluate emotional intensity, customer agitation, and sentiment polarity with calibrated probability scores.",
        "Stage 3: Contextual Natural Language Sentiment Analysis (DistilBERT) —"
    )
    add_bullet(
        "Applies multi-keyword semantic matrices across the transcript to categorize the call into one of six statutory banking complaint domains and assign operational urgency (Critical, High, Medium, Low).",
        "Stage 4: Domain Classification & Regulatory Triage —"
    )
    add_bullet(
        "Extracts acoustic spectral centroid and frequency distribution vectors from the caller's voice, measuring cosine similarity against pre-enrolled profiles to provide an architectural demonstration of biometric matching.",
        "Stage 5: Voiceprint Biometrics Verification Sandbox —"
    )

    add_callout(
        "Architectural Principle: Absolute Local Privacy Boundary",
        "BankVoice AI operates strictly on-premise. All neural inference—including Whisper speech recognition and transformer sentiment modeling—runs locally on host compute without transmitting customer audio streams to public multi-tenant cloud APIs. This architecture satisfies stringent banking compliance standards, including GDPR, GLBA, and PCI-DSS data residency regulations."
    )

    # SECTION 3
    add_h1("3. The Speech-to-Text Pipeline: From Sound Waves to Textual Representation")
    add_h2("3.1 The Physics of Digital Audio and Normalization")
    add_body(
        "Sound is fundamentally a mechanical pressure wave propagating through air. When recorded by a microphone, this continuous physical vibration "
        "is digitized through two fundamental variables: sampling frequency (temporal resolution) and bit depth (amplitude quantization). "
        "In telephony environments, recordings often arrive in diverse sample rates (8 kHz, 22.05 kHz, 44.1 kHz) and compressions (stereo, joint-stereo, 16-bit, 24-bit)."
    )
    add_body(
        "To enable consistent machine interpretation, BankVoice AI first performs channel summing (collapsing stereo audio into a single mono channel) "
        "and normalizes amplitude into 32-bit floating-point numbers spanning [-1.0, 1.0]. A custom native PCM decoder reads uncompressed wave headers "
        "directly in software, eliminating the brittle external operating system dependencies typically associated with telephony decoders."
    )

    add_h2("3.2 The Log-Mel Spectrogram Transformation")
    add_body(
        "Raw audio arrays are difficult for neural networks to process directly because human auditory perception does not perceive frequency "
        "linearly. For instance, the pitch difference between 100 Hz and 200 Hz is perceived as vast, whereas the difference between 7,000 Hz and 7,100 Hz is virtually indistinguishable."
    )
    add_body(
        "To mirror biological human hearing, the pipeline decomposes audio into overlapping short-time Fourier transform (STFT) windows, "
        "mapping linear acoustic frequencies into an 80-channel Mel filter bank. The resulting Log-Mel Spectrogram functions as a high-density "
        "'visual heat map' of speech: the horizontal axis represents time, the vertical axis represents acoustic frequency bands, and the color intensity "
        "represents acoustic energy."
    )

    add_h2("3.3 Transformer Sequence-to-Sequence Modeling (Whisper Mechanics)")
    add_body(
        "The log-mel spectrogram is passed directly to the OpenAI Whisper model architecture, structured around an encoder-decoder Transformer:"
    )
    add_bullet(
        "Processes the spectrogram through one-dimensional convolutional layers with a stride of two, compressing acoustic frames before passing them into multi-head self-attention layers. This extracts phonetic and temporal context across the entire spoken utterance.",
        "The Acoustic Encoder:"
    )
    add_bullet(
        "Employs cross-attention over the encoder's acoustic representations alongside causal self-attention over previously generated words. It predicts word tokens autoregressively, resolving phonetic ambiguities using learned grammatical and conversational priors.",
        "The Autoregressive Decoder:"
    )
    add_body(
        "Because the model is trained on hundreds of thousands of hours of diverse, multi-accented audio, it demonstrates exceptional resilience against "
        "contact center background noise, phone line crackles, and regional dialect variations."
    )

    # SECTION 4
    add_h1("4. Sentiment Analysis: Quantifying Emotional Polarity and Customer Distress")
    add_h2("4.1 Why Binary Polarity Matters in Financial Contact Centers")
    add_body(
        "In enterprise banking, customer sentiment is not merely a marketing metric—it is a leading indicator of account churn, supervisory escalation risk, "
        "and potential regulatory grievances. A caller reporting an unauthorized withdrawal with high emotional agitation requires immediate automated triage, "
        "whereas a customer expressing gratitude for a swift card unblock represents positive service health."
    )

    add_h2("4.2 Bidirectional Transformers (DistilBERT Context Modeling)")
    add_body(
        "Traditional sentiment algorithms relied on simplistic keyword counting, which routinely failed when encountering sarcasm, negation, or complex financial phrasing "
        "(e.g., 'I am not unhappy with the loan officer, but the unexpected fees are unacceptable')."
    )
    add_body(
        "BankVoice AI uses a fine-tuned DistilBERT transformer. Unlike unidirectional language models that read text left-to-right, DistilBERT utilizes "
        "bidirectional self-attention: every word token attends to every other word token simultaneously. This allows the model to compute context-aware "
        "embeddings where the meaning of 'charge' in 'unauthorized charge' is distinctly separated from 'charge' in 'charge my electric vehicle'."
    )
    add_body(
        "The final classification head produces two raw output values (logits) for Positive and Negative sentiment. These logits are normalized through "
        "a Softmax mathematical function into a calibrated confidence score between 0.00% and 100.00%, giving risk supervisors precise insight into model certainty."
    )

    add_h2("4.3 Resilient Heuristic Arbitration")
    add_body(
        "To guarantee zero application crashes in high-security air-gapped financial networks where model download repositories may be blocked, "
        "the sentiment module implements a weighted financial lexicon arbitrator as an automatic secondary failover. If the neural model is unreachable, "
        "the deterministic heuristic engine seamlessly handles inference without disrupting end-user analytics."
    )

    # SECTION 5
    add_h1("5. Complaint Taxonomy & Regulatory Priority Triage")
    add_body(
        "To provide operational utility to bank branch managers and compliance officers, unstructured transcripts must be systematically routed to specialized "
        "operational desks. BankVoice AI implements an institutional classification matrix mapping interactions into six regulated domains:"
    )

    # Table of Categories
    table = doc.add_table(rows=7, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Complaint Domain", "Statutory Scope", "Urgency Rating", "Operational Dispatch Desk"]
    col_widths = [Inches(1.5), Inches(2.3), Inches(1.1), Inches(1.6)]

    # Header row formatting
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        shd = parse_xml(r'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:color="auto" w:fill="0F172A"/>')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)

    data = [
        ("Fraud Complaints", "Account takeover, cloned cards, phishing scams, unauthorized transactions", "CRITICAL", "Fraud Ops & SAR Filing"),
        ("Transaction Issues", "Duplicate charges, failed wire transfers, ATM cash dispensing discrepancies", "HIGH", "Payment Reconciliation Desk"),
        ("Card Issues", "Terminal decline, physical card damage, contactless failure, PIN resets", "HIGH", "Card Operations & Issuance"),
        ("Loan Issues", "Mortgage refinancing, EMI calculation disputes, repayment queries", "MEDIUM", "Lending & Asset Management"),
        ("Account Issues", "Portal lockouts, password resets, KYC document updates, dormant accounts", "MEDIUM", "Branch & Identity Services"),
        ("General Enquiries", "Branch working hours, notary services, account opening queries, compliments", "LOW", "Standard Customer Support")
    ]

    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].text = val
            p = row_cells[col_idx].paragraphs[0]
            style_paragraph(p, space_after=2, space_before=2)
            run = p.runs[0]
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            if col_idx == 2:
                run.font.bold = True
                run.font.color.rgb = CRIMSON if val == "CRITICAL" else (BLUE if val == "HIGH" else MUTED)
            # Alternating row background
            if row_idx % 2 == 1:
                shd = parse_xml(r'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:color="auto" w:fill="F8FAFC"/>')
                row_cells[col_idx]._tc.get_or_add_tcPr().append(shd)

    p_post_table = doc.add_paragraph()
    style_paragraph(p_post_table, space_after=8, space_before=6)

    add_h2("5.1 Multi-Keyword Weighted Density & Precedence Arbitration")
    add_body(
        "A single interaction might mention cards and money transfers simultaneously (e.g., 'My debit card was debited twice for the same transfer'). "
        "The classifier resolves this through weighted keyword scoring: multi-word phrases (such as 'unauthorized charge' or 'duplicate debit') carry higher "
        "mathematical weight than generic standalone terms. Crucially, the rule engine enforces regulatory precedence: if any high-risk fraud keywords are detected, "
        "the interaction is elevated to 'Fraud Complaints' with 'Critical' urgency to trigger mandatory anti-money laundering (AML) and Suspicious Activity Report (SAR) reviews."
    )

    # SECTION 6
    add_h1("6. Voice Biometrics & Speaker Verification: Concepts vs. Reality")
    add_h2("6.1 The Biological Foundation of Voiceprints")
    add_body(
        "Just as human fingerprints are shaped by unique physical friction ridges, a human voice is shaped by individual biological anatomy: "
        "the physical length and geometry of the vocal tract, the shape of the nasal cavity, and the vibration dynamics of the vocal cords (glottal pulses). "
        "When an individual speaks, these anatomical structures impart distinct resonant frequency peaks, known as formants."
    )

    add_h2("6.2 Acoustic Feature Vectors & Cosine Similarity")
    add_body(
        "In BankVoice AI's biometric verification sandbox, incoming audio is transformed via Fast Fourier Transform (FFT) into its underlying frequency spectrum. "
        "By analyzing the acoustic spectral centroid (the center of gravity of voice frequencies) and distribution energy across 64 discrete spectral bins, "
        "the system constructs a high-dimensional mathematical vector representing the caller's acoustic fingerprint."
    )
    add_body(
        "When verifying an identity, the system compares the vector of the current call against the customer's enrolled baseline profile using "
        "Cosine Similarity. Rather than comparing raw volume or spoken words, Cosine Similarity calculates the cosine of the angle between two multi-dimensional vectors. "
        "If the angle is near zero (cosine value approaching 1.0), the acoustic distribution matches the enrolled speaker's vocal characteristics."
    )

    add_callout(
        "Regulatory & Security Clarification: Prototype vs. Enterprise Biometrics",
        "It is vital to distinguish between speech recognition and biometric authentication. Transcribing speech or analyzing sentiment does not prove customer identity. BankVoice AI's biometric module serves as an architectural demonstration of acoustic similarity. In production enterprise banking, voice biometrics must be paired with anti-spoofing liveness detection (to defeat synthetic AI deepfakes), encrypted key enclaves, and multi-factor FIDO2 cryptographic tokens.",
        is_warning=True
    )

    # SECTION 7
    add_h1("7. Telemetry, Data Persistence & Visual Analytics")
    add_h2("7.1 Persistent Audit Ledger (CSV Architecture)")
    add_body(
        "Every interaction analyzed in BankVoice AI is permanently appended to a local audit repository (data/interactions.csv). "
        "The schema captures interaction identifiers, ISO-8601 timestamps, caller identity, raw audio references, the complete transcript, "
        "sentiment polarity and confidence, detected complaint domain, urgency tier, biometric verification status, and a boolean flag "
        "distinguishing pre-loaded historical baseline data from live uploaded recordings."
    )

    add_h2("7.2 Real-Time Analytical Aggregation")
    add_body(
        "The Executive Dashboard computes continuous aggregate metrics across all historical and incoming calls: total interaction volumes, "
        "positive-to-negative sentiment ratios, dominant complaint vectors, and critical fraud escalations. Interactive Plotly visualization engines "
        "render dynamic donut distributions and horizontal frequency bar charts styled in an institutional dark navy theme, providing bank executives "
        "with immediate visual command over their contact center's health."
    )

    # SECTION 8
    add_h1("8. Future Roadmap & Enterprise Expansion")
    add_body(
        "While this implementation delivers a fully functional, self-contained MVP, future commercial expansions include:"
    )
    add_bullet(
        "Integrating low-latency WebSockets and WebRTC to transcribe and flag disputes while the phone call is active, empowering live agents with real-time recommendations.",
        "Live Audio Stream Ingestion —"
    )
    add_bullet(
        "Deploying deep neural bispectral artifact detectors to differentiate between genuine human vocal tract resonance and text-to-speech AI deepfake clones.",
        "Synthetic Voice & Anti-Spoofing Defense —"
    )
    add_bullet(
        "Expanding vocabulary models to handle seamless code-switching across multilingual banking contact centers in diverse global markets.",
        "Multilingual Code-Switching —"
    )

    doc.save(filename)
    return filename

if __name__ == "__main__":
    out = create_whitepaper()
    print(f"Generated: {out}")
