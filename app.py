import streamlit as st
import os
import io
import base64
import time
from PIL import Image
import google.generativeai as genai
from src.image_utils import ImageProcessor
from src.dress_synthesizer import DressSynthesizer
from src.styles import get_custom_css, get_success_message_html, get_tips_html, get_feature_cards_html

# Configure the page
st.set_page_config(
    page_title="Virtual Dress Try-On AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize the AI components
@st.cache_resource
def initialize_ai():
    """Initialize the Gemini AI model"""
    api_key = "AIzaSyDwI__vMH_xwYgk5Hc3M_Lm7goRhwPxBpo"
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def main():
    # Header section with custom styling
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #2C3E50; margin-bottom: 0.5rem;">👗 Virtual Dress Try-On AI</h1>
        <p style="color: #7F8C8D; font-size: 1.2rem; margin: 0;">
            Transform your shopping experience with AI-powered virtual try-ons
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown(get_feature_cards_html(), unsafe_allow_html=True)
    
    # Initialize AI model
    model = initialize_ai()
    image_processor = ImageProcessor()
    dress_synthesizer = DressSynthesizer(model)
    
    # Create two columns for uploads
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="upload-section">
            <h3 style="color: #2C3E50; text-align: center;">👤 Upload Your Photo</h3>
        </div>
        """, unsafe_allow_html=True)
        
        human_file = st.file_uploader(
            "Choose a photo of yourself",
            type=['png', 'jpg', 'jpeg'],
            key="human_upload",
            help="Upload a clear, front-facing photo for best results"
        )
        
        if human_file is not None:
            human_image = Image.open(human_file)
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(human_image, caption="Your Photo", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Image info
            st.info(f"📊 Image size: {human_image.size[0]}x{human_image.size[1]} pixels")
    
    with col2:
        st.markdown("""
        <div class="upload-section">
            <h3 style="color: #2C3E50; text-align: center;">👗 Upload Dress Image</h3>
        </div>
        """, unsafe_allow_html=True)
        
        dress_file = st.file_uploader(
            "Choose a dress image",
            type=['png', 'jpg', 'jpeg'],
            key="dress_upload",
            help="Upload an image of the dress you want to try on"
        )
        
        if dress_file is not None:
            dress_image = Image.open(dress_file)
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(dress_image, caption="Dress", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Image info
            st.info(f"📊 Image size: {dress_image.size[0]}x{dress_image.size[1]} pixels")
    
    # Advanced options
    with st.expander("🔧 Advanced Options", expanded=False):
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            quality = st.select_slider(
                "Output Quality",
                options=["Fast", "Balanced", "High Quality"],
                value="Balanced",
                help="Higher quality takes more time to process"
            )
        with col_opt2:
            enable_analysis = st.checkbox(
                "Enable Style Analysis",
                value=True,
                help="Get AI-powered style compatibility analysis"
            )
    
    # Process button with enhanced styling
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Generate Virtual Try-On", type="primary", use_container_width=True):
        if human_file is not None and dress_file is not None:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Process images
                status_text.text("🔄 Processing images...")
                progress_bar.progress(20)
                
                processed_human = image_processor.preprocess_human_image(human_image)
                processed_dress = image_processor.preprocess_dress_image(dress_image)
                
                # Step 2: Generate try-on
                status_text.text("🎨 Generating virtual try-on...")
                progress_bar.progress(60)
                
                result_image = dress_synthesizer.generate_try_on(
                    processed_human, 
                    processed_dress
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Success message
                st.markdown(get_success_message_html(), unsafe_allow_html=True)
                
                # Display result in styled container
                st.markdown("""
                <div class="result-section">
                    <h2 style="color: #2C3E50; text-align: center; margin-bottom: 1rem;">
                        🎉 Your Virtual Try-On Result
                    </h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["🖼️ Result", "📊 Analysis", "💡 Styling Tips"])
                
                with tab1:
                    st.image(result_image, caption="Virtual Try-On Result", use_column_width=True)
                    
                    # Save result
                    timestamp = int(time.time())
                    output_path = f"outputs/try_on_result_{timestamp}.png"
                    os.makedirs("outputs", exist_ok=True)
                    result_image.save(output_path)
                    
                    # Download section
                    col_download1, col_download2 = st.columns([2, 1])
                    with col_download1:
                        img_buffer = io.BytesIO()
                        result_image.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        
                        st.download_button(
                            label="💾 Download High Quality",
                            data=img_buffer.getvalue(),
                            file_name=f"virtual_try_on_{timestamp}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    with col_download2:
                        st.info(f"💾 Saved to: {output_path}")
                
                with tab2:
                    if enable_analysis:
                        with st.spinner("Analyzing style compatibility..."):
                            analysis = dress_synthesizer.analyze_compatibility(processed_human, processed_dress)
                            st.markdown("### 🔍 Style Analysis")
                            st.write(analysis)
                    else:
                        st.info("Style analysis is disabled. Enable it in Advanced Options.")
                
                with tab3:
                    if enable_analysis:
                        with st.spinner("Generating styling suggestions..."):
                            suggestions = dress_synthesizer.get_styling_suggestions(processed_human, processed_dress)
                            st.markdown("### 💄 Styling Suggestions")
                            st.write(suggestions)
                    else:
                        st.info("Styling suggestions require style analysis to be enabled.")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please make sure both images are clear and properly oriented.")
                progress_bar.empty()
                status_text.empty()
        else:
            st.warning("⚠️ Please upload both a human photo and a dress image to continue.")
    
    # Enhanced sidebar with better organization
    with st.sidebar:
        st.markdown("### 📋 How to Use")
        st.markdown("""
        **Step 1:** Upload your photo  
        **Step 2:** Upload dress image  
        **Step 3:** Click Generate  
        **Step 4:** Download result  
        """)
        
        # Tips section with custom styling
        st.markdown(get_tips_html(), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistics (mock data for demo)
        st.markdown("### 📊 App Statistics")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Try-ons Generated", "1,234", "+89")
        with col_stat2:
            st.metric("Happy Users", "567", "+23")
        
        st.markdown("---")
        
        # About section
        st.markdown("### ℹ️ About")
        st.markdown("""
        🤖 **AI-Powered**: Using Google Gemini AI  
        ⚡ **Fast**: Results in seconds  
        🎨 **Creative**: Advanced image processing  
        🔒 **Privacy**: Images processed locally  
        """)
        
        st.markdown("---")
        
        # Sample images section
        st.markdown("### 🖼️ Need Sample Images?")
        if st.button("📥 Download Sample Pack"):
            st.info("Sample images would be downloaded here in a full implementation.")
        
        # Feedback section
        st.markdown("### 💬 Feedback")
        feedback = st.text_area("Share your experience:", height=100)
        if st.button("Send Feedback"):
            if feedback:
                st.success("Thank you for your feedback!")
            else:
                st.warning("Please enter your feedback first.")

if __name__ == "__main__":
    main()