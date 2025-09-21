# Deployment Guide for Virtual Dress Try-On AI

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd "c:\Users\Atanu Ghosh\OneDrive\Desktop\dress"
   ```

2. **Install dependencies (Option 1 - Automatic):**
   ```bash
   # Windows
   install.bat
   
   # Or manually:
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Windows
   run.bat
   
   # Or manually:
   streamlit run app.py
   ```

4. **Open in browser:**
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

### Manual Installation Steps

1. **Install Python packages:**
   ```bash
   pip install streamlit==1.29.0
   pip install google-generativeai==0.3.2
   pip install Pillow==10.1.0
   pip install numpy==1.24.3
   pip install opencv-python==4.8.1.78
   pip install requests==2.31.0
   pip install python-dotenv==1.0.0
   ```

2. **Verify installation:**
   ```bash
   python -c "import streamlit; import google.generativeai; print('All packages installed successfully!')"
   ```

## Cloud Deployment Options

### 1. Streamlit Cloud (Recommended)

1. **Prepare for deployment:**
   - Ensure all files are in a GitHub repository
   - Make sure `requirements.txt` is up to date
   - Add secrets management for API keys

2. **Deploy steps:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure secrets in the Streamlit Cloud dashboard
   - Deploy!

3. **Environment variables:**
   Add this to your Streamlit Cloud secrets:
   ```toml
   [secrets]
   GEMINI_API_KEY = "AIzaSyDwI__vMH_xwYgk5Hc3M_Lm7goRhwPxBpo"
   ```

### 2. Heroku Deployment

1. **Create additional files:**
   ```bash
   # Procfile
   echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   
   # runtime.txt
   echo "python-3.9.16" > runtime.txt
   ```

2. **Deploy to Heroku:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY="AIzaSyDwI__vMH_xwYgk5Hc3M_Lm7goRhwPxBpo"
   git push heroku main
   ```

### 3. Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t dress-tryon .
   docker run -p 8501:8501 dress-tryon
   ```

## Production Considerations

### Security
- [ ] Move API keys to environment variables
- [ ] Add rate limiting
- [ ] Implement user authentication
- [ ] Add input validation and sanitization

### Performance
- [ ] Add image caching
- [ ] Implement request queuing
- [ ] Add CDN for static assets
- [ ] Monitor memory usage

### Monitoring
- [ ] Add logging
- [ ] Set up error tracking
- [ ] Monitor API usage
- [ ] Track user metrics

### Scalability
- [ ] Add Redis for session management
- [ ] Implement horizontal scaling
- [ ] Add load balancing
- [ ] Database integration for user data

## Troubleshooting

### Common Issues

1. **Module not found errors:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **Port already in use:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **API key errors:**
   - Verify the Gemini API key is correct
   - Check API quotas and limits
   - Ensure internet connection is stable

4. **Memory issues:**
   - Reduce image sizes before processing
   - Clear browser cache
   - Restart the application

### Performance Optimization

1. **Image optimization:**
   ```python
   # In image_utils.py, adjust target_size for faster processing
   self.target_size = (256, 384)  # Smaller size for faster processing
   ```

2. **Caching:**
   ```python
   # Add to app.py
   @st.cache_data
   def process_image(image):
       # Image processing logic
       pass
   ```

## Support

For issues and support:
1. Check the troubleshooting section above
2. Review the application logs
3. Verify all dependencies are correctly installed
4. Ensure the Gemini API key is valid and has sufficient quota

## License

This project is for educational and demonstration purposes.