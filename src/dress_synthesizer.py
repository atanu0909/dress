import google.generativeai as genai
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import time
import streamlit as st
import numpy as np

class DressSynthesizer:
    """Handles AI-powered dress try-on synthesis using Google Gemini"""
    
    def __init__(self, model):
        self.model = model
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1000,
        }
    
    def generate_try_on(self, human_image, dress_image):
        """
        Generate virtual try-on using Gemini's advanced image understanding and description,
        then create a realistic composite based on AI analysis
        """
        try:
            # Convert images to format suitable for Gemini
            human_image_data = self._prepare_image_for_gemini(human_image)
            dress_image_data = self._prepare_image_for_gemini(dress_image)
            
            # Step 1: Get detailed body and dress analysis
            analysis_prompt = """
            Analyze these two images for virtual try-on:
            
            IMAGE 1 (Person):
            - Estimate body measurements and proportions
            - Identify pose and body position
            - Note skin tone and facial features
            - Determine body type (slim, average, curvy, etc.)
            
            IMAGE 2 (Dress):
            - Identify dress style, cut, and silhouette
            - Note fabric type and drape characteristics
            - Determine size and fit style (tight, loose, flowing)
            - Analyze colors and patterns
            
            FITTING ANALYSIS:
            - How would this dress fit this person's body?
            - Where would the dress sit (neckline, waist, hem)?
            - How would it drape and flow on their figure?
            - What adjustments would be needed for perfect fit?
            
            Provide specific, technical details for realistic virtual fitting.
            """
            
            # Get AI analysis
            analysis_response = self.model.generate_content([
                analysis_prompt,
                human_image_data,
                dress_image_data
            ])
            
            # Step 2: Generate virtual try-on visualization prompt
            visualization_prompt = f"""
            Based on this analysis: {analysis_response.text}
            
            Now describe EXACTLY how this person would look wearing this dress:
            
            VISUAL COMPOSITION:
            - Person wearing the dress in the same pose as the original photo
            - Dress properly fitted to their body shape and size
            - Natural draping and fabric behavior
            - Proper proportions and positioning
            
            REALISTIC DETAILS:
            - How the dress would look from this viewing angle
            - Shadow and lighting effects on the fabric
            - Natural wrinkles and fabric folds
            - Color interaction with skin tone
            - Overall styling and aesthetic appeal
            
            Describe this as if you're looking at a real photograph of this person wearing this exact dress.
            Be extremely detailed and specific about the visual result.
            """
            
            # Get detailed visualization
            visualization_response = self.model.generate_content([
                visualization_prompt,
                human_image_data,
                dress_image_data
            ])
            
            # Create enhanced virtual try-on using AI insights
            result_image = self._create_ai_guided_try_on(
                human_image, 
                dress_image, 
                visualization_response.text,
                analysis_response.text
            )
            
            return result_image
            
        except Exception as e:
            st.error(f"Error in AI processing: {str(e)}")
            # Return a fallback composite image
            return self._create_advanced_composite(human_image, dress_image)
    
    def _create_advanced_composite(self, human_image, dress_image):
        """
        Create an advanced composite image as fallback
        """
        # Create side-by-side with arrow indicating transformation
        total_width = human_image.width + dress_image.width + 100
        max_height = max(human_image.height, dress_image.height)
        
        # Create canvas
        canvas = Image.new('RGB', (total_width, max_height + 50), (240, 240, 240))
        
        # Paste original human image
        canvas.paste(human_image, (0, 25))
        
        # Create a simple overlay version
        overlay_result = self._create_simple_overlay(human_image, dress_image)
        
        # Paste result
        result_x = human_image.width + 100
        canvas.paste(overlay_result, (result_x, 25))
        
        return canvas
    
    def _create_simple_overlay(self, human_image, dress_image):
        """
        Create a simple overlay effect
        """
        # Resize dress to fit on person
        dress_width = int(human_image.width * 0.5)
        dress_height = int(human_image.height * 0.6)
        
        dress_resized = dress_image.resize(
            (dress_width, dress_height), 
            Image.Resampling.LANCZOS
        )
        
        # Create overlay
        result = human_image.copy()
        overlay = Image.new('RGBA', result.size, (0, 0, 0, 0))
        
        # Position dress
        dress_x = (result.width - dress_width) // 2
        dress_y = int(result.height * 0.2)
        
        # Convert and blend
        if dress_resized.mode != 'RGBA':
            dress_resized = dress_resized.convert('RGBA')
            
        # Make semi-transparent
        alpha = dress_resized.split()[-1]
        alpha = alpha.point(lambda p: p * 0.7)
        dress_resized.putalpha(alpha)
        
        overlay.paste(dress_resized, (dress_x, dress_y), dress_resized)
        
        # Composite
        result_rgba = result.convert('RGBA')
        final = Image.alpha_composite(result_rgba, overlay)
        
        return final.convert('RGB')
    
    def _create_try_on_prompt(self):
        """Create a detailed prompt for virtual try-on"""
        return """
        You are an expert fashion stylist and virtual try-on specialist. 
        I will provide you with two images:
        1. A photo of a person
        2. A photo of a dress or clothing item
        
        Please analyze both images and provide a detailed description of how 
        the person would look wearing the dress. Consider:
        - Body shape and how the dress would fit
        - Color coordination
        - Style compatibility
        - Overall aesthetic appeal
        - Any adjustments that might be needed
        
        Be specific and detailed in your description.
        """
    
    def _prepare_image_for_gemini(self, image):
        """Convert PIL Image to format suitable for Gemini API"""
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create the image data structure for Gemini
        return {
            "mime_type": "image/png",
            "data": img_byte_arr
        }
    
    def _create_ai_guided_try_on(self, human_image, dress_image, visualization_desc, analysis_desc=""):
        """
        Create an enhanced virtual try-on using AI insights about fit and style
        """
        # Parse AI descriptions for detailed fitting information
        fitting_info = self._parse_ai_description(visualization_desc + " " + analysis_desc)
        
        # Create realistic virtual try-on
        result_image = self._create_realistic_try_on(
            human_image, dress_image, fitting_info, visualization_desc
        )
        
        return result_image
    
    def _create_realistic_try_on(self, human_image, dress_image, fitting_info, ai_description):
        """
        Create a more realistic virtual try-on based on AI analysis
        """
        # Start with the human image as base
        result = human_image.copy()
        
        # Create multiple layers for realistic compositing
        dress_layer = self._create_fitted_dress_layer(dress_image, human_image, fitting_info)
        
        # Apply dress to person with intelligent masking
        composite = self._composite_dress_on_body(result, dress_layer, fitting_info)
        
        # Apply post-processing for realism
        final_result = self._apply_realistic_effects(composite, ai_description)
        
        return final_result
    
    def _create_fitted_dress_layer(self, dress_image, human_image, fitting_info):
        """
        Create a dress layer fitted to the human body proportions
        """
        # Estimate body dimensions from human image
        body_width = int(human_image.width * 0.6)  # Approximate torso width
        body_height = int(human_image.height * 0.7)  # Approximate torso height
        
        # Adjust dress size based on fitting analysis
        if fitting_info.get('body_type') == 'slim':
            dress_width = int(body_width * 0.9)
        elif fitting_info.get('body_type') == 'curvy':
            dress_width = int(body_width * 1.1)
        else:
            dress_width = body_width
            
        # Calculate dress height based on style
        if 'short' in fitting_info.get('dress_style', '').lower():
            dress_height = int(body_height * 0.6)
        elif 'long' in fitting_info.get('dress_style', '').lower():
            dress_height = int(body_height * 1.2)
        else:
            dress_height = body_height
        
        # Resize dress to fit body
        fitted_dress = dress_image.resize(
            (dress_width, dress_height), 
            Image.Resampling.LANCZOS
        )
        
        return fitted_dress
    
    def _composite_dress_on_body(self, human_image, dress_layer, fitting_info):
        """
        Composite the dress onto the human body with intelligent positioning
        """
        # Create overlay canvas
        overlay = Image.new('RGBA', human_image.size, (0, 0, 0, 0))
        
        # Calculate positioning based on body landmarks (simplified)
        center_x = human_image.width // 2
        
        # Estimate where dress should sit based on analysis
        if 'shoulders' in fitting_info.get('dress_position', '').lower():
            start_y = int(human_image.height * 0.15)  # Shoulder level
        elif 'chest' in fitting_info.get('dress_position', '').lower():
            start_y = int(human_image.height * 0.25)  # Chest level
        else:
            start_y = int(human_image.height * 0.2)   # Default upper torso
        
        # Position dress
        dress_x = center_x - (dress_layer.width // 2)
        dress_y = start_y
        
        # Ensure dress stays within image bounds
        dress_x = max(0, min(dress_x, human_image.width - dress_layer.width))
        dress_y = max(0, min(dress_y, human_image.height - dress_layer.height))
        
        # Convert dress to RGBA and apply blending
        if dress_layer.mode != 'RGBA':
            dress_layer = dress_layer.convert('RGBA')
        
        # Create more natural blending
        alpha = dress_layer.split()[-1]
        # Variable transparency for more realistic look
        alpha = alpha.point(lambda p: int(p * 0.85) if p > 128 else int(p * 0.7))
        dress_layer.putalpha(alpha)
        
        # Paste dress onto overlay
        overlay.paste(dress_layer, (dress_x, dress_y), dress_layer)
        
        # Composite with human image
        human_rgba = human_image.convert('RGBA')
        result = Image.alpha_composite(human_rgba, overlay)
        
        return result.convert('RGB')
    
    def _apply_realistic_effects(self, image, ai_description):
        """
        Apply post-processing effects for more realistic appearance
        """
        result = image.copy()
        
        # Apply subtle blur to dress edges for natural integration
        # This is a simplified approach - in production, use edge detection
        
        # Enhance based on AI description
        if 'vibrant' in ai_description.lower() or 'bright' in ai_description.lower():
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.15)
        
        if 'soft' in ai_description.lower() or 'flowing' in ai_description.lower():
            # Apply slight blur for softer look
            result = result.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Enhance contrast slightly for better definition
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(1.05)
        
        return result
    
    def _parse_ai_description(self, description):
        """Extract detailed fitting information from AI description"""
        fitting_info = {
            'body_type': 'average',
            'dress_fit': 'regular',
            'dress_style': 'regular',
            'dress_position': 'chest',
            'color_match': 'good',
            'style_compatibility': 'high',
            'fabric_behavior': 'normal',
            'suggested_adjustments': []
        }
        
        # Comprehensive keyword analysis
        description_lower = description.lower()
        
        # Body type analysis
        if any(word in description_lower for word in ['slim', 'slender', 'thin', 'lean']):
            fitting_info['body_type'] = 'slim'
        elif any(word in description_lower for word in ['curvy', 'full', 'plus-size', 'voluptuous']):
            fitting_info['body_type'] = 'curvy'
        elif any(word in description_lower for word in ['athletic', 'muscular', 'toned']):
            fitting_info['body_type'] = 'athletic'
            
        # Dress fit analysis
        if any(word in description_lower for word in ['tight', 'fitted', 'snug', 'form-fitting']):
            fitting_info['dress_fit'] = 'tight'
        elif any(word in description_lower for word in ['loose', 'flowing', 'relaxed', 'baggy']):
            fitting_info['dress_fit'] = 'loose'
            
        # Dress style analysis
        if any(word in description_lower for word in ['short', 'mini', 'above knee']):
            fitting_info['dress_style'] = 'short'
        elif any(word in description_lower for word in ['long', 'maxi', 'floor-length', 'ankle']):
            fitting_info['dress_style'] = 'long'
        elif any(word in description_lower for word in ['midi', 'knee-length', 'below knee']):
            fitting_info['dress_style'] = 'midi'
            
        # Position analysis
        if any(word in description_lower for word in ['shoulder', 'neckline', 'collar']):
            fitting_info['dress_position'] = 'shoulders'
        elif any(word in description_lower for word in ['chest', 'bust', 'breast']):
            fitting_info['dress_position'] = 'chest'
        elif any(word in description_lower for word in ['waist', 'waistline', 'middle']):
            fitting_info['dress_position'] = 'waist'
            
        # Fabric behavior
        if any(word in description_lower for word in ['drape', 'flow', 'cascade', 'fall']):
            fitting_info['fabric_behavior'] = 'flowing'
        elif any(word in description_lower for word in ['structured', 'stiff', 'rigid']):
            fitting_info['fabric_behavior'] = 'structured'
            
        return fitting_info
    
    def _process_dress_for_fitting(self, dress_image, fitting_info):
        """Process dress image for better fitting on the person"""
        # Resize dress based on fitting analysis
        target_width = int(dress_image.width * 0.8)  # Adjust based on fit
        target_height = int(dress_image.height * 0.9)
        
        if fitting_info['dress_fit'] == 'tight':
            target_width = int(target_width * 0.9)
        elif fitting_info['dress_fit'] == 'loose':
            target_width = int(target_width * 1.1)
        
        processed_dress = dress_image.resize(
            (target_width, target_height), 
            Image.Resampling.LANCZOS
        )
        
        return processed_dress
    
    def _create_dress_overlay(self, human_image, processed_dress, fitting_info):
        """Create positioned dress overlay on the human image"""
        # Create transparent overlay
        overlay = Image.new('RGBA', human_image.size, (0, 0, 0, 0))
        
        # Calculate positioning based on human body analysis
        # This is simplified - in production, use body landmark detection
        human_center_x = human_image.width // 2
        human_top_y = int(human_image.height * 0.2)  # Approximate chest area
        
        # Position dress
        dress_x = human_center_x - (processed_dress.width // 2)
        dress_y = human_top_y
        
        # Ensure dress stays within bounds
        dress_x = max(0, min(dress_x, human_image.width - processed_dress.width))
        dress_y = max(0, min(dress_y, human_image.height - processed_dress.height))
        
        # Convert dress to RGBA for transparency
        if processed_dress.mode != 'RGBA':
            processed_dress = processed_dress.convert('RGBA')
        
        # Apply transparency for blending
        alpha = processed_dress.split()[-1]
        alpha = alpha.point(lambda p: p * 0.8)  # Make semi-transparent
        processed_dress.putalpha(alpha)
        
        overlay.paste(processed_dress, (dress_x, dress_y), processed_dress)
        
        return overlay
    
    def _blend_dress_on_person(self, human_image, dress_overlay, fitting_info):
        """Blend dress overlay onto human using advanced compositing"""
        # Convert human image to RGBA
        human_rgba = human_image.convert('RGBA')
        
        # Composite the dress onto the person
        result = Image.alpha_composite(human_rgba, dress_overlay)
        
        # Convert back to RGB
        final_result = result.convert('RGB')
        
        return final_result
    
    def _apply_ai_enhancements(self, image, ai_description):
        """Apply AI-suggested visual enhancements"""
        # Apply subtle enhancements based on AI analysis
        enhanced = image.copy()
        
        # Enhance colors if AI suggests good color compatibility
        if 'complement' in ai_description.lower() or 'match' in ai_description.lower():
            enhancer = ImageEnhance.Color(enhanced)
            enhanced = enhancer.enhance(1.1)  # Slight color boost
        
        # Add slight sharpening for better definition
        enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = enhancer.enhance(1.05)
        
        return enhanced
    
    def _create_simple_composite(self, human_image, dress_image):
        """Create a simple side-by-side composite as fallback"""
        # Calculate dimensions
        max_height = max(human_image.height, dress_image.height)
        total_width = human_image.width + dress_image.width + 40
        
        # Create canvas
        composite = Image.new('RGB', (total_width, max_height + 100), (240, 240, 240))
        
        # Paste human image
        human_y = (max_height - human_image.height) // 2
        composite.paste(human_image, (20, human_y))
        
        # Paste dress image
        dress_y = (max_height - dress_image.height) // 2
        dress_x = human_image.width + 40
        composite.paste(dress_image, (dress_x, dress_y))
        
        return composite
    
    def analyze_compatibility(self, human_image, dress_image):
        """Analyze style compatibility between person and dress"""
        try:
            prompt = """
            Analyze the compatibility between this person and this dress/clothing item.
            Consider:
            1. Color coordination
            2. Style compatibility
            3. Fit predictions
            4. Overall aesthetic appeal
            5. Suggestions for improvement
            
            Provide a detailed analysis with a compatibility score (1-10).
            """
            
            human_data = self._prepare_image_for_gemini(human_image)
            dress_data = self._prepare_image_for_gemini(dress_image)
            
            response = self.model.generate_content([
                prompt,
                human_data,
                dress_data
            ])
            
            return response.text
            
        except Exception as e:
            return f"Analysis unavailable: {str(e)}"
    
    def get_styling_suggestions(self, human_image, dress_image):
        """Get AI-powered styling suggestions"""
        try:
            prompt = """
            Based on this person and dress combination, provide styling suggestions:
            1. Recommended accessories
            2. Shoe suggestions
            3. Hair and makeup recommendations
            4. Color coordination tips
            5. Occasion suitability
            
            Be specific and practical in your suggestions.
            """
            
            human_data = self._prepare_image_for_gemini(human_image)
            dress_data = self._prepare_image_for_gemini(dress_image)
            
            response = self.model.generate_content([
                prompt,
                human_data,
                dress_data
            ])
            
            return response.text
            
        except Exception as e:
            return f"Suggestions unavailable: {str(e)}"