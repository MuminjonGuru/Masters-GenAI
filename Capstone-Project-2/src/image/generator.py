"""
Image generation module using OpenAI DALL-E 3.
Generates images from text prompts.
"""

import os
import requests
from datetime import datetime
from typing import Optional, Literal
from pathlib import Path
from openai import OpenAI
from PIL import Image
from io import BytesIO
from src.utils.logger import get_logger


class ImageGenerator:
    """
    Generates images from text prompts using OpenAI DALL-E 3.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "dall-e-3",
        size: Literal["1024x1024", "1024x1792", "1792x1024"] = "1024x1024",
        quality: Literal["standard", "hd"] = "standard",
        style: Literal["vivid", "natural"] = "vivid",
        output_dir: str = "outputs"
    ):
        """
        Initialize the DALL-E 3 client.

        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model: DALL-E model (default: dall-e-3)
            size: Image size (1024x1024, 1024x1792, 1792x1024)
            quality: Image quality (standard or hd)
            style: Image style (vivid or natural)
            output_dir: Directory to save generated images
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.size = size
        self.quality = quality
        self.style = style
        self.output_dir = Path(output_dir)
        self.logger = get_logger()

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.logger.log_info(
            f"ImageGenerator initialized (model: {model}, size: {size}, "
            f"quality: {quality}, style: {style})"
        )

    def generate(self, prompt: str, filename: Optional[str] = None) -> tuple[str, str]:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description for image generation
            filename: Optional custom filename (auto-generated if not provided)

        Returns:
            Tuple of (image_file_path, image_url)

        Raises:
            Exception: If generation fails
        """
        try:
            self.logger.log_image_generation_start()

            # Call DALL-E 3 API
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=self.size,
                quality=self.quality,
                style=self.style,
                n=1  # DALL-E 3 only supports n=1
            )

            # Get the image URL
            image_url = response.data[0].url

            # Download and save the image
            image_path = self._download_image(image_url, filename)

            self.logger.log_image_generation_complete(str(image_path), self.model, self.size)

            return str(image_path), image_url

        except Exception as e:
            self.logger.log_error("image generation", e)
            raise

    def _download_image(self, url: str, filename: Optional[str] = None) -> Path:
        """
        Download image from URL and save to disk.

        Args:
            url: Image URL
            filename: Optional custom filename

        Returns:
            Path to saved image
        """
        try:
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_{timestamp}.png"

            # Ensure .png extension
            if not filename.endswith('.png'):
                filename += '.png'

            filepath = self.output_dir / filename

            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Save image
            image = Image.open(BytesIO(response.content))
            image.save(filepath, format="PNG")

            self.logger.log_info(f"Image downloaded and saved to: {filepath}")

            return filepath

        except Exception as e:
            self.logger.log_error("image download", e)
            raise

    def generate_variations(
        self,
        prompt: str,
        num_variations: int = 3,
        base_filename: Optional[str] = None
    ) -> list[tuple[str, str]]:
        """
        Generate multiple variations by calling the API multiple times.
        Note: DALL-E 3 doesn't support n>1, so we make multiple calls.

        Args:
            prompt: Text description for image generation
            num_variations: Number of variations to generate (max 5)
            base_filename: Base filename for variations

        Returns:
            List of tuples (image_file_path, image_url)
        """
        if num_variations > 5:
            self.logger.log_warning("Maximum 5 variations allowed, using 5")
            num_variations = 5

        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for i in range(num_variations):
            try:
                if base_filename:
                    filename = f"{base_filename}_v{i+1}.png"
                else:
                    filename = f"generated_{timestamp}_v{i+1}.png"

                image_path, image_url = self.generate(prompt, filename)
                results.append((image_path, image_url))

            except Exception as e:
                self.logger.log_error(f"variation {i+1}", e)
                continue

        return results

    def get_output_files(self) -> list[Path]:
        """
        Get list of all generated images in output directory.

        Returns:
            List of image file paths
        """
        return sorted(self.output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
