#!/usr/bin/env python3
"""
Setup script for environment configuration

Usage: python scripts/setup_environment.py
"""

import os
import sys
import subprocess
from pathlib import Path


def create_virtual_environment():
    """
    Create Python virtual environment
    """
    print("Creating virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False


def install_dependencies():
    """
    Install required dependencies
    """
    print("\nInstalling dependencies...")
    
    try:
        # Upgrade pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install from requirements.txt
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def create_directories():
    """
    Create necessary directories
    """
    print("\nCreating directories...")
    
    directories = [
        "data",
        "data/cache",
        "data/logs",
        "plugins",
        "resources/icons",
        "resources/styles",
        "dist",
        "build",
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {path}")
    
    return True


def main():
    """
    Main setup function
    """
    print("="*80)
    print("TRN Analysis Software - Environment Setup")
    print("="*80)
    
    # Create directories
    if not create_directories():
        print("\nError: Failed to create directories")
        return 1
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\nNote: Virtual environment creation failed. Continuing without it.")
    
    # Install dependencies
    if not install_dependencies():
        print("\nError: Failed to install dependencies")
        return 1
    
    print("\n" + "="*80)
    print("Setup completed successfully!")
    print("="*80)
    
    print("\nNext steps:")
    print("  1. Activate virtual environment:")
    print("     - Windows: venv\\Scripts\\activate")
    print("     - Unix/Mac: source venv/bin/activate")
    print("\n  2. Run the application:")
    print("     python src/main.py")
    print("\n  3. Build executable (optional):")
    print("     python scripts/build_executable.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
