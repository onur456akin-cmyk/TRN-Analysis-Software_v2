"""Main Application Window"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QSpinBox, QDoubleSpinBox, QComboBox,
    QGroupBox, QTabWidget, QMessageBox, QProgressBar, QStatusBar
)
from PySide6.QtCore import Qt, QTimer
from pathlib import Path
import logging

from src.config import Config
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.current_file = None
        self.audio_data = None
        self.sample_rate = None
        
        logger.info("Initializing Main Window")
        
        self.init_ui()
        self.setWindowTitle(f"{config.app_name} v{config.version}")
        self.setGeometry(100, 100, 1400, 900)
    
    def init_ui(self):
        """Initialize user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout()
        
        # Left panel - Parameters
        left_panel = self.create_left_panel()
        
        # Center panel - Graphics/Analysis area (placeholder)
        center_panel = self.create_center_panel()
        
        # Right panel - Results (placeholder)
        right_panel = self.create_right_panel()
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(center_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        logger.info("UI initialization complete")
    
    def create_left_panel(self) -> QGroupBox:
        """Create left parameter panel"""
        group = QGroupBox("Analysis Parameters")
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Audio File:"))
        self.file_label = QLabel("No file selected")
        file_layout.addWidget(self.file_label)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Hydrophone Sensitivity
        sens_layout = QHBoxLayout()
        sens_layout.addWidget(QLabel("Hydrophone Sensitivity (dB):"))
        self.sensitivity_spinbox = QDoubleSpinBox()
        self.sensitivity_spinbox.setRange(-300, 0)
        self.sensitivity_spinbox.setValue(self.config.default_hydrophone_sensitivity)
        sens_layout.addWidget(self.sensitivity_spinbox)
        layout.addLayout(sens_layout)
        
        # Amplifier Gain
        gain_layout = QHBoxLayout()
        gain_layout.addWidget(QLabel("Amplifier Gain (dB):"))
        self.gain_spinbox = QDoubleSpinBox()
        self.gain_spinbox.setRange(-100, 100)
        self.gain_spinbox.setValue(self.config.default_amplifier_gain)
        gain_layout.addWidget(self.gain_spinbox)
        layout.addLayout(gain_layout)
        
        # Sampling Frequency
        fs_layout = QHBoxLayout()
        fs_layout.addWidget(QLabel("Sampling Frequency (Hz):"))
        self.fs_spinbox = QSpinBox()
        self.fs_spinbox.setRange(8000, 1000000)
        self.fs_spinbox.setValue(self.config.default_sample_rate)
        fs_layout.addWidget(self.fs_spinbox)
        layout.addLayout(fs_layout)
        
        # TRN Algorithm
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("TRN Algorithm:"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(self.config.trn_algorithms)
        algo_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algo_layout)
        
        # Transmission Loss Model
        tl_layout = QHBoxLayout()
        tl_layout.addWidget(QLabel("TL Model:"))
        self.tl_combo = QComboBox()
        self.tl_combo.addItems(self.config.transmission_loss_models)
        tl_layout.addWidget(self.tl_combo)
        layout.addLayout(tl_layout)
        
        # FFT Length
        fft_layout = QHBoxLayout()
        fft_layout.addWidget(QLabel("FFT Length:"))
        self.fft_combo = QComboBox()
        self.fft_combo.addItems([str(l) for l in self.config.fft_lengths])
        self.fft_combo.setCurrentText(str(self.config.default_fft_length))
        fft_layout.addWidget(self.fft_combo)
        layout.addLayout(fft_layout)
        
        # Window Type
        window_layout = QHBoxLayout()
        window_layout.addWidget(QLabel("Window Type:"))
        self.window_combo = QComboBox()
        self.window_combo.addItems(self.config.window_types)
        self.window_combo.setCurrentText("hann")
        window_layout.addWidget(self.window_combo)
        layout.addLayout(window_layout)
        
        # Analyze button
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.run_analysis)
        self.analyze_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        layout.addWidget(self.analyze_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def create_center_panel(self) -> QGroupBox:
        """Create center analysis panel"""
        group = QGroupBox("Analysis Results")
        layout = QVBoxLayout()
        
        # Placeholder for graphics
        self.result_label = QLabel("No analysis performed yet")
        self.result_label.setStyleSheet("background-color: #f0f0f0; padding: 20px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)
        
        group.setLayout(layout)
        return group
    
    def create_right_panel(self) -> QGroupBox:
        """Create right results panel"""
        group = QGroupBox("Results")
        layout = QVBoxLayout()
        
        # Results display
        self.results_label = QLabel("Waiting for analysis...")
        layout.addWidget(self.results_label)
        
        # Export button
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self.export_results)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def browse_file(self):
        """Browse for audio file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            str(Path.home()),
            "Audio Files (*.wav *.bin *.txt);;All Files (*)"
        )
        
        if file_path:
            self.current_file = Path(file_path)
            self.file_label.setText(self.current_file.name)
            self.status_bar.showMessage(f"File selected: {self.current_file.name}")
            logger.info(f"File selected: {self.current_file}")
    
    def run_analysis(self):
        """Run TRN analysis"""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "Please select an audio file first")
            return
        
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_bar.showMessage("Analyzing...")
            self.analyze_btn.setEnabled(False)
            
            # Load audio file
            self.progress_bar.setValue(25)
            from src.core.file_manager import FileManager
            self.audio_data, self.sample_rate = FileManager.load_wav(self.current_file)
            
            self.progress_bar.setValue(50)
            
            # Get parameters
            sensitivity = self.sensitivity_spinbox.value()
            gain = self.gain_spinbox.value()
            algorithm = self.algorithm_combo.currentText()
            
            # Apply calibration
            self.progress_bar.setValue(75)
            from src.core.calibration import CalibrationModule
            pressure_signal = CalibrationModule.apply_full_calibration(
                self.audio_data, sensitivity, gain
            )
            
            # Calculate TRN
            self.progress_bar.setValue(90)
            from src.core.trn_algorithms import TRNCalculator
            
            if algorithm == "ANSI":
                trn_value = TRNCalculator.calculate_trn_ansi(pressure_signal, self.sample_rate)
            elif algorithm == "ISO":
                trn_value = TRNCalculator.calculate_trn_iso(pressure_signal, self.sample_rate)
            elif algorithm == "Welch PSD":
                trn_value, _, _ = TRNCalculator.calculate_trn_welch_psd(pressure_signal, self.sample_rate)
            elif algorithm == "FFT Average":
                trn_value, _, _ = TRNCalculator.calculate_trn_fft_average(pressure_signal, self.sample_rate)
            else:  # RMS
                trn_value = TRNCalculator.calculate_trn_rms(pressure_signal, self.sample_rate)
            
            self.progress_bar.setValue(100)
            
            # Display results
            result_text = f"""
            <b>Analysis Complete</b><br><br>
            <b>File:</b> {self.current_file.name}<br>
            <b>Algorithm:</b> {algorithm}<br>
            <b>Sample Rate:</b> {self.sample_rate} Hz<br>
            <b>Signal Length:</b> {len(self.audio_data)} samples ({len(self.audio_data)/self.sample_rate:.2f}s)<br>
            <b>TRN Value:</b> <span style="color: green; font-size: 14pt;"><b>{trn_value:.2f} dB re 1 µPa</b></span>
            """
            
            self.results_label.setText(result_text)
            self.result_label.setText(f"TRN: {trn_value:.2f} dB")
            self.status_bar.showMessage("Analysis complete")
            logger.info(f"Analysis complete: TRN = {trn_value:.2f} dB")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Analysis failed: {str(e)}")
            self.status_bar.showMessage("Analysis failed")
            logger.error(f"Analysis error: {e}")
        finally:
            self.progress_bar.setVisible(False)
            self.analyze_btn.setEnabled(True)
    
    def export_results(self):
        """Export analysis results"""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No analysis results to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            str(Path.home()),
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            # TODO: Implement export functionality
            QMessageBox.information(self, "Info", "Export functionality coming soon")
            logger.info(f"Export requested to: {file_path}")


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = MainWindow(Config())
    window.show()
    sys.exit(app.exec())
