from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import cv2

class ImageProcessor:
    """Handles image preprocessing for the virtual try-on application"""
    
    def __init__(self):
        self.target_size = (512, 768)  # Width x Height for consistent processing
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
    
    def preprocess_human_image(self, image):
        """
        Preprocess human image for virtual try-on
        - Resize to standard dimensions
        - Enhance quality
        - Ensure proper orientation
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = image.size
        
        # Calculate new dimensions maintaining aspect ratio
        if original_height > original_width:
            # Portrait orientation (preferred)
            new_height = self.target_size[1]
            new_width = int((original_width / original_height) * new_height)
        else:
            # Landscape orientation - adjust accordingly
            new_width = self.target_size[0]
            new_height = int((original_height / original_width) * new_width)
        
        # Resize image
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a canvas with target size and paste the image centered
        canvas = Image.new('RGB', self.target_size, (255, 255, 255))
        paste_x = (self.target_size[0] - new_width) // 2
        paste_y = (self.target_size[1] - new_height) // 2
        canvas.paste(image, (paste_x, paste_y))
        
        # Enhance image quality
        canvas = self._enhance_image(canvas)
        
        return canvas
    
    def preprocess_dress_image(self, image):
        """
        Preprocess dress image for virtual try-on
        - Resize appropriately
        - Remove background if possible
        - Enhance details
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize maintaining aspect ratio
        image.thumbnail((400, 600), Image.Resampling.LANCZOS)
        
        # Enhance image quality
        image = self._enhance_image(image)
        
        return image
    
    def _enhance_image(self, image):
        """Enhance image quality with brightness, contrast, and sharpness adjustments"""
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        # Enhance color saturation slightly
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.05)
        
        return image
    
    def validate_image(self, image_file):
        """Validate uploaded image file"""
        if image_file is None:
            return False, "No image file provided"
        
        # Check file size
        if hasattr(image_file, 'size') and image_file.size > self.max_file_size:
            return False, f"File size too large. Maximum allowed: {self.max_file_size // (1024*1024)}MB"
        
        try:
            # Try to open and verify the image
            image = Image.open(image_file)
            image.verify()  # Verify it's a valid image
            return True, "Valid image"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def create_side_by_side_comparison(self, original, result):
        """Create a side-by-side comparison image"""
        # Resize both images to same height
        height = min(original.height, result.height, 600)
        
        original_resized = original.resize(
            (int(original.width * height / original.height), height),
            Image.Resampling.LANCZOS
        )
        result_resized = result.resize(
            (int(result.width * height / result.height), height),
            Image.Resampling.LANCZOS
        )
        
        # Create comparison canvas
        total_width = original_resized.width + result_resized.width + 20
        comparison = Image.new('RGB', (total_width, height), (255, 255, 255))
        
        # Paste images
        comparison.paste(original_resized, (0, 0))
        comparison.paste(result_resized, (original_resized.width + 20, 0))
        
        return comparison
    
    def convert_to_base64(self, image):
        """Convert PIL Image to base64 string for AI processing"""
        import io
        import base64
        
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        return image_base64
    
    def resize_for_display(self, image, max_width=800):
        """Resize image for display in Streamlit while maintaining aspect ratio"""
        if image.width <= max_width:
            return image
        
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        return image.resize((max_width, new_height), Image.Resampling.LANCZOS)