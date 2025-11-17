"""
Prompt enhancement module using OpenAI GPT-4.
Transforms simple voice transcripts into detailed image generation prompts.
"""

import os
from typing import Optional
from openai import OpenAI
from src.utils.logger import get_logger


class PromptEnhancer:
    """
    Enhances voice transcripts into detailed image generation prompts using GPT-4.
    """

    SYSTEM_PROMPT = """You are an expert at creating detailed, vivid image generation prompts.

Your task is to transform simple user descriptions into rich, detailed prompts for DALL-E 3 image generation.

Guidelines:
- Enhance the description with artistic details (lighting, composition, style, mood)
- Add specific visual elements that would make the image more compelling
- Keep the core intent of the user's request
- Use descriptive adjectives and artistic terminology
- Specify art style, medium, or photographic technique when appropriate
- Keep the enhanced prompt focused and under 400 characters for optimal results
- Do NOT add content that contradicts the user's request
- If the request is already detailed, refine it rather than completely rewriting

Examples:
User: "a cat on a couch"
Enhanced: "A fluffy orange tabby cat sitting elegantly on a modern gray velvet couch, natural window lighting, cozy living room setting, photorealistic style, high detail"

User: "sunset over mountains"
Enhanced: "Breathtaking sunset over majestic mountain peaks, golden and orange hues painting the sky, dramatic clouds, silhouetted mountain range, vibrant colors, landscape photography style, 8k quality"

User: "futuristic city"
Enhanced: "Futuristic cyberpunk cityscape at night, neon lights reflecting on wet streets, towering skyscrapers with holographic advertisements, flying vehicles, bustling streets, cinematic lighting, ultra detailed digital art"

Now enhance the user's description while keeping their core vision intact."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7
    ):
        """
        Initialize the GPT-4 client for prompt enhancement.

        Args:
            api_key: OpenAI API key (uses env var if not provided)
            model: GPT model to use (default: gpt-4-turbo)
            temperature: Creativity level (0.0-1.0, default: 0.7)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.logger = get_logger()

        self.logger.log_info(f"PromptEnhancer initialized (model: {model}, temperature: {temperature})")

    def enhance(self, transcript: str) -> str:
        """
        Enhance a voice transcript into a detailed image generation prompt.

        Args:
            transcript: Original voice transcript

        Returns:
            Enhanced image generation prompt

        Raises:
            Exception: If enhancement fails
        """
        try:
            self.logger.log_enhancement_start()

            # Call GPT-4 for prompt enhancement
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": f"Enhance this image description: {transcript}"}
                ],
                temperature=self.temperature,
                max_tokens=200  # Keep prompts concise
            )

            enhanced_prompt = response.choices[0].message.content.strip()

            self.logger.log_enhancement_complete(enhanced_prompt, self.model)

            return enhanced_prompt

        except Exception as e:
            self.logger.log_error("prompt enhancement", e)
            raise

    def enhance_with_style(self, transcript: str, style: str = "photorealistic") -> str:
        """
        Enhance transcript with a specific artistic style.

        Args:
            transcript: Original voice transcript
            style: Desired art style (photorealistic, oil painting, digital art, etc.)

        Returns:
            Enhanced image generation prompt with style

        Raises:
            Exception: If enhancement fails
        """
        try:
            self.logger.log_enhancement_start()

            style_instruction = f"Enhance this image description in {style} style: {transcript}"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": style_instruction}
                ],
                temperature=self.temperature,
                max_tokens=200
            )

            enhanced_prompt = response.choices[0].message.content.strip()

            self.logger.log_enhancement_complete(enhanced_prompt, self.model)

            return enhanced_prompt

        except Exception as e:
            self.logger.log_error("prompt enhancement", e)
            raise
