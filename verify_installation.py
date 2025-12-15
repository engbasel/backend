"""
Script to verify all required packages are installed correctly.
Run this after installing requirements.txt to ensure everything is working.
"""

import sys

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name:20s} - version {version}")
        return True
    except ImportError:
        print(f"❌ {package_name:20s} - NOT INSTALLED")
        return False

def main():
    print("\n" + "="*60)
    print("NeuroAid Backend - Package Verification")
    print("="*60 + "\n")
    
    packages = [
        # Core Flask
        ("flask", "flask"),
        ("flask-cors", "flask_cors"),
        ("python-dotenv", "dotenv"),
        ("Werkzeug", "werkzeug"),
        
        # API & HTTP
        ("requests", "requests"),
        
        # Authentication
        ("PyJWT", "jwt"),
        ("bcrypt", "bcrypt"),
        
        # Data Science & ML
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        
        # Deep Learning
        ("tensorflow", "tensorflow"),
        
        # Image Processing
        ("Pillow", "PIL"),
    ]
    
    print("Checking Core Packages:")
    print("-" * 60)
    
    all_installed = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_installed = False
    
    print("\n" + "="*60)
    
    if all_installed:
        print("✅ SUCCESS: All packages are installed correctly!")
        print("\nYou can now run the backend services:")
        print("  python run_system.py")
        print("  or")
        print("  python gateway.py")
    else:
        print("❌ ERROR: Some packages are missing!")
        print("\nPlease run:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print("="*60 + "\n")
    
    # Additional system info
    print("System Information:")
    print("-" * 60)
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
