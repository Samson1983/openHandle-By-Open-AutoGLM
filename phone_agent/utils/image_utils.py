"""Image utilities for base64 conversion and image manipulation."""

import base64
import os
from io import BytesIO
from typing import Optional
from PIL import Image


class Base64ImageConverter:
    """Utility class for converting base64 strings to images and saving them."""

    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """
        Convert a base64 string to a PIL Image object.

        Args:
            base64_string: The base64 encoded image string.

        Returns:
            PIL Image object.

        Raises:
            ValueError: If the base64 string is invalid or cannot be decoded.
        """
        try:
            # Remove data URL prefix if present (e.g., "data:image/png;base64,")
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]

            # Decode base64 string
            image_data = base64.b64decode(base64_string)
            
            # Create PIL Image from bytes
            image = Image.open(BytesIO(image_data))
            return image

        except Exception as e:
            raise ValueError(f"Failed to decode base64 string: {e}")

    @staticmethod
    def save_base64_as_image(
        base64_string: str,
        output_path: str,
        format: Optional[str] = None,
        quality: int = 95
    ) -> str:
        """
        Convert a base64 string to an image and save it to a file.

        Args:
            base64_string: The base64 encoded image string.
            output_path: The path where the image will be saved.
            format: The image format (e.g., "PNG", "JPEG"). If None, uses file extension.
            quality: The image quality for JPEG format (1-100, default: 95).

        Returns:
            The absolute path of the saved image.

        Raises:
            ValueError: If the base64 string is invalid or cannot be decoded.
            IOError: If the file cannot be saved.
        """
        # Convert base64 to image
        image = Base64ImageConverter.base64_to_image(base64_string)

        # Determine format from file extension if not specified
        if format is None:
            file_ext = os.path.splitext(output_path)[1].lower()
            format_map = {
                ".png": "PNG",
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".gif": "GIF",
                ".bmp": "BMP",
                ".webp": "WEBP",
            }
            format = format_map.get(file_ext, "PNG")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Save the image
        save_kwargs = {}
        if format == "JPEG":
            save_kwargs["quality"] = quality

        image.save(output_path, format=format, **save_kwargs)

        return os.path.abspath(output_path)

    @staticmethod
    def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
        """
        Convert a PIL Image object to a base64 string.

        Args:
            image: PIL Image object.
            format: The image format (e.g., "PNG", "JPEG").

        Returns:
            Base64 encoded string of the image.
        """
        buffered = BytesIO()
        image.save(buffered, format=format)
        base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return base64_string

    @staticmethod
    def load_image_as_base64(image_path: str, format: str = "PNG") -> str:
        """
        Load an image file and convert it to a base64 string.

        Args:
            image_path: Path to the image file.
            format: The image format (e.g., "PNG", "JPEG").

        Returns:
            Base64 encoded string of the image.

        Raises:
            FileNotFoundError: If the image file doesn't exist.
            ValueError: If the image cannot be loaded.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        image = Image.open(image_path)
        return Base64ImageConverter.image_to_base64(image, format)

    @staticmethod
    def resize_image(
        image: Image.Image,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        maintain_aspect_ratio: bool = True
    ) -> Image.Image:
        """
        Resize an image while optionally maintaining aspect ratio.

        Args:
            image: PIL Image object.
            max_width: Maximum width (None if no limit).
            max_height: Maximum height (None if no limit).
            maintain_aspect_ratio: Whether to maintain aspect ratio.

        Returns:
            Resized PIL Image object.
        """
        if max_width is None and max_height is None:
            return image

        original_width, original_height = image.size

        if maintain_aspect_ratio:
            # Calculate new dimensions maintaining aspect ratio
            if max_width and max_height:
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            elif max_width:
                ratio = max_width / original_width
                new_width = max_width
                new_height = int(original_height * ratio)
            else:  # max_height
                ratio = max_height / original_height
                new_width = int(original_width * ratio)
                new_height = max_height
        else:
            # Use specified dimensions directly
            new_width = max_width or original_width
            new_height = max_height or original_height

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    @staticmethod
    def save_base64_as_resized_image(
        base64_string: str,
        output_path: str,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        maintain_aspect_ratio: bool = True,
        format: Optional[str] = None,
        quality: int = 95
    ) -> str:
        """
        Convert a base64 string to an image, resize it, and save to a file.

        Args:
            base64_string: The base64 encoded image string.
            output_path: The path where the image will be saved.
            max_width: Maximum width (None if no limit).
            max_height: Maximum height (None if no limit).
            maintain_aspect_ratio: Whether to maintain aspect ratio.
            format: The image format (e.g., "PNG", "JPEG"). If None, uses file extension.
            quality: The image quality for JPEG format (1-100, default: 95).

        Returns:
            The absolute path of the saved image.
        """
        # Convert base64 to image
        image = Base64ImageConverter.base64_to_image(base64_string)

        # Resize image
        image = Base64ImageConverter.resize_image(
            image, max_width, max_height, maintain_aspect_ratio
        )

        # Determine format from file extension if not specified
        if format is None:
            file_ext = os.path.splitext(output_path)[1].lower()
            format_map = {
                ".png": "PNG",
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".gif": "GIF",
                ".bmp": "BMP",
                ".webp": "WEBP",
            }
            format = format_map.get(file_ext, "PNG")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Save the image
        save_kwargs = {}
        if format == "JPEG":
            save_kwargs["quality"] = quality

        image.save(output_path, format=format, **save_kwargs)

        return os.path.abspath(output_path)


def base64_to_image(base64_string: str) -> Image.Image:
    """
    Convenience function to convert base64 string to PIL Image.

    Args:
        base64_string: The base64 encoded image string.

    Returns:
        PIL Image object.
    """
    return Base64ImageConverter.base64_to_image(base64_string)


def save_base64_as_image(
    base64_string: str,
    output_path: str,
    format: Optional[str] = None,
    quality: int = 95
) -> str:
    """
    Convenience function to save base64 string as image file.

    Args:
        base64_string: The base64 encoded image string.
        output_path: The path where the image will be saved.
        format: The image format (e.g., "PNG", "JPEG"). If None, uses file extension.
        quality: The image quality for JPEG format (1-100, default: 95).

    Returns:
        The absolute path of the saved image.
    """
    return Base64ImageConverter.save_base64_as_image(
        base64_string, output_path, format, quality
    )
