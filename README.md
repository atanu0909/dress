# Virtual Dress Try-On AI Application

This application uses AI to create virtual dress try-ons by combining human photos with dress images.

## Features

- 🤖 AI-powered virtual dress try-on using Google Gemini
- 📸 Easy image upload interface
- 🎨 Automatic image preprocessing and enhancement
- 💾 Download generated results
- 📱 Responsive web interface built with Streamlit

## Installation

1. Clone or download this project
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided local URL (usually `http://localhost:8501`)

3. Upload your photo and a dress image

4. Click "Generate Try-On" to create your virtual try-on result

5. Download your result image

## Project Structure

```
dress/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── src/
│   ├── image_utils.py       # Image processing utilities
│   └── dress_synthesizer.py # AI-powered dress synthesis
├── uploads/                 # Temporary upload storage
├── outputs/                 # Generated results
└── assets/                  # Static assets
```

## Configuration

The application uses Google Gemini AI for image analysis and processing. The API key is configured directly in the code for this demo version.

For production use, consider:
- Moving the API key to environment variables
- Adding user authentication
- Implementing rate limiting
- Adding more sophisticated image generation capabilities

## Tips for Best Results

- Use high-quality, well-lit photos
- Ensure the person is facing forward in the photo
- Use dress images with clear, visible details
- Images should preferably be in portrait orientation

## Technology Stack

- **Frontend**: Streamlit
- **AI Processing**: Google Gemini AI
- **Image Processing**: PIL (Pillow), OpenCV
- **Backend**: Python

## License

This project is for educational and demonstration purposes.