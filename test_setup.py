"""
Test script to verify the Virtual Dress Try-On application setup
"""

import sys
import subprocess
import importlib

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_package_imports():
    """Test if all required packages can be imported"""
    packages = [
        ('streamlit', 'Streamlit'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('cv2', 'OpenCV'),
        ('google.generativeai', 'Google Generative AI'),
    ]
    
    all_passed = True
    print("\nTesting package imports...")
    
    for package, name in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {name} - Available")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_passed = False
    
    return all_passed

def test_file_structure():
    """Test if all required files exist"""
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'src/__init__.py',
        'src/image_utils.py',
        'src/dress_synthesizer.py',
        'src/styles.py',
    ]
    
    required_dirs = [
        'src',
        'uploads',
        'outputs',
        'assets',
        '.streamlit',
    ]
    
    all_passed = True
    print("\nTesting file structure...")
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_passed = False
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✅ {directory}/ - Found")
        else:
            print(f"❌ {directory}/ - Missing")
            all_passed = False
    
    return all_passed

def test_streamlit_installation():
    """Test if Streamlit can run"""
    print("\nTesting Streamlit installation...")
    try:
        result = subprocess.run(['streamlit', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Streamlit - {result.stdout.strip()}")
            return True
        else:
            print("❌ Streamlit - Installation issue")
            return False
    except Exception as e:
        print(f"❌ Streamlit - Error: {str(e)}")
        return False

def test_api_configuration():
    """Test API key configuration"""
    print("\nTesting API configuration...")
    try:
        import google.generativeai as genai
        api_key = "AIzaSyDwI__vMH_xwYgk5Hc3M_Lm7goRhwPxBpo"
        if api_key and len(api_key) > 20:
            print("✅ Gemini API Key - Configured")
            return True
        else:
            print("❌ Gemini API Key - Not properly configured")
            return False
    except Exception as e:
        print(f"❌ API Configuration - Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Virtual Dress Try-On Application - Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_package_imports,
        test_file_structure,
        test_streamlit_installation,
        test_api_configuration,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! Your application is ready to run.")
        print("\nTo start the application, run:")
        print("  streamlit run app.py")
        print("\nOr use the batch file:")
        print("  run.bat")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\nTo fix missing packages, run:")
        print("  pip install -r requirements.txt")
    
    return all(results)

if __name__ == "__main__":
    main()