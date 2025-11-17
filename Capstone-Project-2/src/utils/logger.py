"""
Logging utility for Voice to Image application.
Provides color-coded console logging for all pipeline stages.
"""

import logging
import colorlog
from datetime import datetime
from typing import Optional


class AppLogger:
    """
    Centralized logging system with color-coded output.
    Logs all pipeline stages: audio input, transcription, enhancement, generation.
    """

    def __init__(self, name: str = "VoiceToImage", level: str = "INFO"):
        """
        Initialize the logger with color formatting.

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.logger = colorlog.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            ))
            self.logger.addHandler(handler)

    def log_audio_input(self, duration: Optional[float] = None):
        """Log audio input reception."""
        if duration:
            self.logger.info(f"🎤 Audio input received (duration: {duration:.2f}s)")
        else:
            self.logger.info("🎤 Audio input received")

    def log_transcription_start(self):
        """Log start of transcription process."""
        self.logger.info("🎧 Starting Whisper API transcription...")

    def log_transcription_complete(self, transcript: str, model: str = "whisper-1"):
        """Log successful transcription."""
        preview = transcript[:100] + "..." if len(transcript) > 100 else transcript
        self.logger.info(f"✓ Transcription complete (model: {model})")
        self.logger.info(f"  Transcript: \"{preview}\"")

    def log_enhancement_start(self):
        """Log start of prompt enhancement."""
        self.logger.info("✨ Starting GPT-4 prompt enhancement...")

    def log_enhancement_complete(self, enhanced_prompt: str, model: str = "gpt-4-turbo"):
        """Log successful prompt enhancement."""
        preview = enhanced_prompt[:100] + "..." if len(enhanced_prompt) > 100 else enhanced_prompt
        self.logger.info(f"✓ Prompt enhancement complete (model: {model})")
        self.logger.info(f"  Enhanced: \"{preview}\"")

    def log_image_generation_start(self):
        """Log start of image generation."""
        self.logger.info("🖼️  Starting DALL-E 3 image generation...")

    def log_image_generation_complete(self, image_path: str, model: str = "dall-e-3", size: str = "1024x1024"):
        """Log successful image generation."""
        self.logger.info(f"✓ Image generation complete (model: {model}, size: {size})")
        self.logger.info(f"  Saved to: {image_path}")

    def log_pipeline_complete(self, total_time: float):
        """Log completion of entire pipeline."""
        self.logger.info(f"🎉 Pipeline completed successfully in {total_time:.2f}s")

    def log_error(self, stage: str, error: Exception):
        """Log errors with context."""
        self.logger.error(f"❌ Error in {stage}: {str(error)}")

    def log_warning(self, message: str):
        """Log warning messages."""
        self.logger.warning(f"⚠️  {message}")

    def log_info(self, message: str):
        """Log general info messages."""
        self.logger.info(message)

    def log_debug(self, message: str):
        """Log debug messages."""
        self.logger.debug(message)


# Global logger instance
_global_logger = None


def get_logger(name: str = "VoiceToImage", level: str = "INFO") -> AppLogger:
    """
    Get or create the global logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        AppLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = AppLogger(name, level)
    return _global_logger
