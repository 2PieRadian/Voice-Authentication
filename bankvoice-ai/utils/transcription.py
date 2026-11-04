"""
Speech-to-Text Transcription Module using OpenAI Whisper.
Features dual audio decoding: native WAV PCM decoding (works without FFmpeg)
and standard FFmpeg pipeline for MP3/other compressed formats.
"""

import os
import wave
import numpy as np
from typing import Dict, Any, Tuple


_WHISPER_MODEL = None
_MODEL_NAME = "base"


def get_audio_duration_wave(file_path: str) -> float:
    """Read duration directly from WAV headers without FFmpeg."""
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate > 0:
                return round(frames / float(rate), 2)
    except Exception:
        pass
    return 0.0


def read_wav_as_np16k(file_path: str) -> np.ndarray:
    """
    Read standard uncompressed WAV file and resample/convert to 16,000 Hz mono float32.
    Enables Whisper to run completely standalone on Windows even without FFmpeg installed!
    """
    with wave.open(file_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        
        raw_bytes = wf.readframes(n_frames)
        
        # Determine dtype
        if sampwidth == 1:
            # 8-bit unsigned
            data = np.frombuffer(raw_bytes, dtype=np.uint8).astype(np.float32) - 128.0
            data /= 128.0
        elif sampwidth == 2:
            # 16-bit signed
            data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        elif sampwidth == 3:
            # 24-bit PCM
            raw_bytes_list = bytearray(raw_bytes)
            # unpack 3-byte chunks
            samples = []
            for i in range(0, len(raw_bytes_list), 3):
                b = raw_bytes_list[i:i+3]
                val = int.from_bytes(b, byteorder='little', signed=True)
                samples.append(val)
            data = np.array(samples, dtype=np.float32) / 8388608.0
        elif sampwidth == 4:
            # 32-bit float or int
            data = np.frombuffer(raw_bytes, dtype=np.float32)
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth} bytes")

        # Convert to mono if stereo
        if n_channels > 1:
            data = data.reshape(-1, n_channels).mean(axis=1)

        # Resample to 16000 Hz if needed
        if framerate != 16000 and len(data) > 0:
            target_len = int(len(data) * 16000 / framerate)
            if target_len > 0:
                indices = np.linspace(0, len(data) - 1, target_len)
                data = np.interp(indices, np.arange(len(data)), data).astype(np.float32)

        return data


def load_whisper_model(model_name: str = "base"):
    """
    Load and cache the OpenAI Whisper model.
    Defaulting to 'base' (approx 74M params) for fast CPU inference.
    """
    global _WHISPER_MODEL, _MODEL_NAME
    if _WHISPER_MODEL is not None and _MODEL_NAME == model_name:
        return _WHISPER_MODEL

    try:
        import whisper
        _WHISPER_MODEL = whisper.load_model(model_name)
        _MODEL_NAME = model_name
        return _WHISPER_MODEL
    except Exception as e:
        raise RuntimeError(f"Failed to initialize OpenAI Whisper ({model_name}): {str(e)}")


def transcribe_audio(file_path: str, model_name: str = "base") -> Dict[str, Any]:
    """
    Transcribe audio file into English text using OpenAI Whisper.
    
    Args:
        file_path (str): Path to WAV or MP3 audio file.
        model_name (str): Whisper model tier ('tiny', 'base', 'small').
        
    Returns:
        dict:
            - status: "success" or "error"
            - transcript: str
            - language: str
            - duration: float
            - word_count: int
            - error_message: Optional[str]
    """
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "transcript": "",
            "language": "en",
            "duration": 0.0,
            "word_count": 0,
            "error_message": f"Audio file not found at path: {file_path}"
        }

    file_size = os.path.getsize(file_path)
    if file_size < 100:
        return {
            "status": "error",
            "transcript": "",
            "language": "en",
            "duration": 0.0,
            "word_count": 0,
            "error_message": "Audio file is empty or corrupted (file size is under 100 bytes)."
        }

    duration = 0.0
    audio_input = file_path
    is_wav = file_path.lower().endswith(".wav")

    # Attempt direct WAV decode first to eliminate Windows FFmpeg dependency
    if is_wav:
        try:
            audio_array = read_wav_as_np16k(file_path)
            duration = round(len(audio_array) / 16000.0, 2)
            if len(audio_array) == 0:
                return {
                    "status": "error",
                    "transcript": "",
                    "language": "en",
                    "duration": 0.0,
                    "word_count": 0,
                    "error_message": "The audio recording contains 0 audio frames."
                }
            audio_input = audio_array
        except Exception:
            # Fall back to Whisper's standard loader
            audio_input = file_path
            duration = get_audio_duration_wave(file_path)

    try:
        model = load_whisper_model(model_name)
        result = model.transcribe(
            audio_input,
            language="en",
            fp16=False,
            temperature=0.0
        )
        
        transcript = result.get("text", "").strip()
        lang = result.get("language", "en")

        if not transcript:
            return {
                "status": "warning",
                "transcript": "[No audible speech detected in this recording]",
                "language": lang,
                "duration": duration,
                "word_count": 0,
                "error_message": "No discernible customer speech detected. The audio may be silent or faint."
            }

        word_count = len(transcript.split())

        return {
            "status": "success",
            "transcript": transcript,
            "language": lang,
            "duration": duration if duration > 0 else round(word_count * 0.4, 2),
            "word_count": word_count,
            "error_message": None
        }

    except FileNotFoundError as fnf_err:
        # Occurs on Windows if MP3 is uploaded and ffmpeg.exe is not in PATH
        return {
            "status": "error",
            "transcript": "",
            "language": "en",
            "duration": duration,
            "word_count": 0,
            "error_message": (
                "FFmpeg is missing from your Windows PATH to decode compressed audio (.mp3). "
                "Please upload an uncompressed .WAV file, or install FFmpeg via PowerShell: "
                "`winget install Gyan.FFmpeg`"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "transcript": "",
            "language": "en",
            "duration": duration,
            "word_count": 0,
            "error_message": f"Transcription error: {str(e)}"
        }

