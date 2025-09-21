# Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start (Windows)
1. Run the installation script:
   ```cmd
   install.bat
   ```

2. Start the application:
   ```cmd
   run.bat
   ```

### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and go to: `http://localhost:8501`

## Cloud Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Heroku
1. Create a `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker Deployment
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t dress-tryout .
   docker run -p 8501:8501 dress-tryout
   ```

## Environment Variables
For production deployment, consider setting these environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MAX_UPLOAD_SIZE`: Maximum file upload size
- `DEBUG`: Set to false for production

## Troubleshooting
- If you get import errors, ensure all dependencies are installed
- For memory issues, consider reducing image sizes in `image_utils.py`
- Check the Streamlit logs for detailed error messages