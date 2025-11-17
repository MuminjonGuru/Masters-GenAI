"""
Voice transcription module using OpenAI Whisper API.
Converts audio files to text transcripts.
"""

import os
from typing import Optional
from openai import OpenAI
from src.utils.logger import get_logger


class VoiceTranscriber:
    """
    Handles voice-to-text transcription using OpenAI Whisper API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "whisper-1",
        language: str = "en"
    ):
        """
        Initialize the Whisper API client.

        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model: Whisper model to use (default: whisper-1)
            language: Language code for optimization (default: en)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.language = language
        self.logger = get_logger()

        self.logger.log_info(f"VoiceTranscriber initialized (model: {model}, language: {language})")

    def transcribe(self, audio_data: bytes, filename: str = "audio.wav") -> str:
        """
        Transcribe audio bytes to text using Whisper API.

        Args:
            audio_data: Audio file bytes
            filename: Filename for the audio (helps API determine format)

        Returns:
            Transcript text

        Raises:
            Exception: If transcription fails
        """
        try:
            self.logger.log_transcription_start()

            # Create a file-like object from bytes
            from io import BytesIO
            audio_file = BytesIO(audio_data)
            audio_file.name = filename

            # Call Whisper API
            response = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=self.language,
                response_format="text"
            )

            transcript = response.strip() if isinstance(response, str) else response.text.strip()

            self.logger.log_transcription_complete(transcript, self.model)

            return transcript

        except Exception as e:
            self.logger.log_error("transcription", e)
            raise

    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe audio file from path.

        Args:
            file_path: Path to audio file

        Returns:
            Transcript text

        Raises:
            Exception: If transcription fails
        """
        try:
            self.logger.log_transcription_start()

            with open(file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=self.language,
                    response_format="text"
                )

            transcript = response.strip() if isinstance(response, str) else response.text.strip()

            self.logger.log_transcription_complete(transcript, self.model)

            return transcript

        except Exception as e:
            self.logger.log_error("transcription", e)
            raise
