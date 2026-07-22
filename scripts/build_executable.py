#!/usr/bin/env python3
"""
Build script for creating standalone executable

Usage: python scripts/build_executable.py
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """
    Build standalone executable using PyInstaller
    """
    print("="*80)
    print("TRN Analysis Software - Build Script")
    print("="*80)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller not installed.")
        print("Install with: pip install PyInstaller")
        sys.exit(1)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    spec_file = project_root / "build" / "trn_analysis.spec"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    print(f"\nProject root: {project_root}")
    print(f"Spec file: {spec_file}")
    print(f"Output directory: {dist_dir}")
    
    # Build executable
    print("\n" + "="*80)
    print("Building executable...")
    print("="*80)
    
    cmd = [
        "pyinstaller",
        str(spec_file),
        "--distpath", str(dist_dir),
        "--buildpath", str(build_dir),
        "--clean",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        
        print("\n" + "="*80)
        print("Build completed successfully!")
        print("="*80)
        print(f"\nExecutable location: {dist_dir / 'TRN_Analysis' / 'TRN_Analysis.exe'}")
        print(f"\nTo run the application:")
        print(f"  {dist_dir / 'TRN_Analysis' / 'TRN_Analysis.exe'}")
        print(f"\nOr on Windows:")
        print(f"  .\\dist\\TRN_Analysis\\TRN_Analysis.exe")
        
        return 0
    
    except subprocess.CalledProcessError as e:
        print(f"\nError: Build failed with exit code {e.returncode}")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
