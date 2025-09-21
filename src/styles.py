"""
Custom CSS styles for the Virtual Dress Try-On application
"""

def get_custom_css():
    return """
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    /* Upload sections */
    .upload-section {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 0 15px 15px 0;
    }
    
    /* Image containers */
    .image-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-left: 4px solid #FF6B6B;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Result section */
    .result-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        
        .upload-section {
            padding: 1rem;
        }
    }
    </style>
    """

def get_success_message_html():
    return """
    <div style="
        background: linear-gradient(45deg, #4CAF50, #8BC34A);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
    ">
        🎉 <strong>Success!</strong> Your virtual try-on has been generated!
    </div>
    """

def get_tips_html():
    return """
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #2196F3;
    ">
        <h4 style="color: #2196F3; margin-bottom: 1rem;">💡 Pro Tips</h4>
        <ul style="list-style-type: none; padding: 0;">
            <li style="margin-bottom: 0.5rem;">✨ Use well-lit, high-resolution images</li>
            <li style="margin-bottom: 0.5rem;">👤 Face the camera directly for best results</li>
            <li style="margin-bottom: 0.5rem;">👗 Choose dresses with clear, visible details</li>
            <li style="margin-bottom: 0.5rem;">📱 Portrait orientation works best</li>
        </ul>
    </div>
    """

def get_feature_cards_html():
    return """
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    ">
        <div style="
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #FF6B6B;">🤖 AI-Powered</h3>
            <p>Advanced AI technology for realistic try-on results</p>
        </div>
        
        <div style="
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #4ECDC4;">⚡ Fast Processing</h3>
            <p>Quick results in just a few seconds</p>
        </div>
        
        <div style="
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #9B59B6;">📱 Easy to Use</h3>
            <p>Simple interface, no technical knowledge required</p>
        </div>
    </div>
    """