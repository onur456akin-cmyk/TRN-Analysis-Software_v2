#!/usr/bin/env python3
"""
Target Radiated Noise (TRN) Analysis Software
Main Application Entry Point
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.config import Config
from src.utilities.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


def main():
    """Main application entry point"""
    try:
        logger.info("Starting TRN Analysis Software")
        
        # Initialize configuration
        config = Config()
        logger.info(f"Configuration loaded: {config.app_name} v{config.version}")
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName(config.app_name)
        app.setApplicationVersion(config.version)
        
        # Import main window after Qt app is created
        from src.gui.main_window import MainWindow
        
        # Create and show main window
        window = MainWindow(config)
        window.show()
        
        logger.info("Main window displayed")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
