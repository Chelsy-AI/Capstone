# build_config.py
"""
Weather Dashboard Build Configuration

This script automates the process of building a standalone executable for your weather app using PyInstaller.
It does this in a clean, customizable, and cross-platform-friendly way.
"""

import PyInstaller.__main__
import os
import shutil
import sys
import platform
from pathlib import Path

class WeatherDashboardBuilder:
    """Handles building the Weather Dashboard executable with PyInstaller."""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / 'build'
        self.dist_dir = self.project_root / 'dist'
        self.app_name = 'WeatherDashboard'
        
    def clean_previous_builds(self):
        """Remove previous build and dist directories."""
        for directory in [self.build_dir, self.dist_dir]:
            if directory.exists():
                shutil.rmtree(directory)
    
    def verify_dependencies(self):
        """Check if all required dependencies are available."""
        
        required_modules = [
            'customtkinter',
            'requests',
            'Pillow',
            'tkinter'
        ]
        
        optional_modules = [
            'tkintermapview',
            'matplotlib',
            'pytest'
        ]
        
        missing_required = []
        missing_optional = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_required.append(module)
        
        for module in optional_modules:
            try:
                __import__(module)
            except ImportError:
                missing_optional.append(module)
        
        if missing_required:
            return False
        
        if missing_optional:
            return True
    
    def get_data_files(self):
        """Get list of data files to include in the build."""
        data_files = []
        
        # Define data directories and their contents
        data_mappings = {
            'weather_dashboard': 'weather_dashboard',
            'data': 'data',
            'resources': 'resources'
        }
        
        # Add data files if they exist
        for source, dest in data_mappings.items():
            source_path = self.project_root / source
            if source_path.exists():
                data_files.append(f'--add-data={source_path}{os.pathsep}{dest}')
        
        # Add specific resource files
        resource_files = [
            'requirements.txt',
            'README.md',
            'UserGuide.md'
        ]
        
        for file in resource_files:
            file_path = self.project_root / file
            if file_path.exists():
                data_files.append(f'--add-data={file_path}{os.pathsep}.')
        
        return data_files
    
    def get_hidden_imports(self):
        """Get list of hidden imports for PyInstaller."""
        hidden_imports = [
            # Core GUI components
            'tkinter',
            'tkinter.ttk',
            'tkinter.messagebox',
            'tkinter.filedialog',
            
            # CustomTkinter and related
            'customtkinter',
            'customtkinter.windows',
            'customtkinter.widgets',
            
            # Weather API and networking
            'requests',
            'urllib3',
            'json',
            'csv',
            
            # Image processing
            'PIL',
            'PIL.Image',
            'PIL.ImageTk',
            
            # Data handling
            'datetime',
            'threading',
            'queue',
            
            # Weather app specific modules
            'weather_dashboard.config.animations',
            'weather_dashboard.config.api',
            'weather_dashboard.config.error_handler',
            'weather_dashboard.config.storage',
            'weather_dashboard.config.themes',
            'weather_dashboard.config.utils',
            'weather_dashboard.config.weather_app',
            
            # Features modules
            'weather_dashboard.features.city_comparison',
            'weather_dashboard.features.graphs',
            'weather_dashboard.features.history_tracker',
            'weather_dashboard.features.interactive_map',
            'weather_dashboard.features.sun_moon_phases',
            'weather_dashboard.features.theme_switcher',
            'weather_dashboard.features.tomorrows_guess',
            'weather_dashboard.features.weather_icons',
            'weather_dashboard.features.weather_quiz',
            
            # GUI modules
            'weather_dashboard.gui.animation_controller',
            'weather_dashboard.gui.main_gui',
            'weather_dashboard.gui.weather_display',
            
            # Language modules
            'weather_dashboard.language.controller',
            'weather_dashboard.language.translations',
            'weather_dashboard.language.utils'
        ]
        
        # Add optional imports if available
        try:
            import tkintermapview
            hidden_imports.extend([
                'tkintermapview',
                'tkintermapview.map_widget',
                'tkintermapview.canvas_position_marker'
            ])
        except ImportError:
            pass
        
        try:
            import matplotlib
            hidden_imports.extend([
                'matplotlib',
                'matplotlib.backends.backend_tkagg',
                'matplotlib.figure',
                'matplotlib.pyplot'
            ])
        except ImportError:
            pass
        
        return [f'--hidden-import={module}' for module in hidden_imports]
    
    def get_excluded_modules(self):
        """Get list of modules to exclude from the build."""
        excluded_modules = [
            # Development and testing
            'pytest',
            'unittest',
            'doctest',
            
            # Documentation
            'sphinx',
            'pydoc',
            
            # Alternative GUI frameworks
            'PySide2',
            'PySide6',
            'PyQt5',
            'PyQt6',
            'wx',
            
            # Development tools
            'IPython',
            'notebook',
            'jupyter',
            
            # Large optional packages
            'numpy.testing',
            'scipy.tests',
            'matplotlib.tests'
        ]
        
        return [f'--exclude-module={module}' for module in excluded_modules]
    
    def get_platform_specific_args(self):
        """Get platform-specific build arguments."""
        args = []
        system = platform.system()
        
        if system == 'Windows':
            args.extend([
                '--version-file=version_info.txt' if os.path.exists('version_info.txt') else '',
                '--windowed',  # No console window
                '--icon=resources/icons/icon.ico' if os.path.exists('resources/icons/icon.ico') else ''
            ])
            
            # Add Windows-specific DLLs if needed
            vcruntime_paths = [
                'C:\\Windows\\System32\\vcruntime140.dll',
                'C:\\Windows\\System32\\msvcp140.dll'
            ]
            
            for dll_path in vcruntime_paths:
                if os.path.exists(dll_path):
                    args.append(f'--add-binary={dll_path}{os.pathsep}.')
        
        elif system == 'Darwin':  # macOS
            args.extend([
                '--windowed',
                '--icon=resources/icons/icon.icns' if os.path.exists('resources/icons/icon.icns') else '',
                '--osx-bundle-identifier=com.weatherdashboard.app'
            ])
        
        elif system == 'Linux':
            args.extend([
                '--windowed',
                '--icon=resources/icons/icon.png' if os.path.exists('resources/icons/icon.png') else ''
            ])
        
        # Filter out empty strings
        return [arg for arg in args if arg]
    
    def create_version_info(self):
        """Create version info file for Windows builds."""
        if platform.system() != 'Windows':
            return
        
        version_info_content = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Weather Dashboard Team'),
        StringStruct(u'FileDescription', u'Weather Dashboard Application'),
        StringStruct(u'FileVersion', u'2.0.0'),
        StringStruct(u'InternalName', u'WeatherDashboard'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'WeatherDashboard.exe'),
        StringStruct(u'ProductName', u'Weather Dashboard'),
        StringStruct(u'ProductVersion', u'2.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        with open('version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info_content)
    
    def build_executable(self):
        """Build the weather dashboard executable."""
        
        # Verify dependencies
        if not self.verify_dependencies():
            return False
        
        # Clean previous builds
        self.clean_previous_builds()
        
        # Create version info for Windows
        self.create_version_info()
                
        # Base PyInstaller arguments
        args = [
            'main.py',  # Entry point
            f'--name={self.app_name}',  # Executable name
            '--onefile',  # Single file output
            '--clean',  # Clean temporary files
            '--noconfirm',  # Replace output without asking
            '--log-level=INFO',  # Logging level
        ]
        
        # Add data files
        args.extend(self.get_data_files())
        
        # Add hidden imports
        args.extend(self.get_hidden_imports())
        
        # Add excluded modules
        args.extend(self.get_excluded_modules())
        
        # Add platform-specific arguments
        args.extend(self.get_platform_specific_args())
        
        # Filter out empty arguments
        args = [arg for arg in args if arg]
                
        try:
            # Run PyInstaller
            PyInstaller.__main__.run(args)
            
            # Check if build was successful
            exe_name = f"{self.app_name}.exe" if platform.system() == 'Windows' else self.app_name
            exe_path = self.dist_dir / exe_name
            
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)  # Size in MB
                
                # Clean up temporary files
                if os.path.exists('version_info.txt'):
                    os.remove('version_info.txt')
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def create_installer_script(self):
        """Create a simple installer script for distribution."""
        if platform.system() == 'Windows':
            installer_content = f'''@echo off
echo Installing Weather Dashboard...
copy "dist\\{self.app_name}.exe" "%USERPROFILE%\\Desktop\\"
echo Weather Dashboard installed to Desktop!
pause
'''
            with open('install.bat', 'w') as f:
                f.write(installer_content)
        
        elif platform.system() in ['Darwin', 'Linux']:
            installer_content = f'''#!/bin/bash
echo "Installing Weather Dashboard..."
cp "dist/{self.app_name}" "$HOME/Desktop/"
chmod +x "$HOME/Desktop/{self.app_name}"
echo "Weather Dashboard installed to Desktop!"
'''
            with open('install.sh', 'w') as f:
                f.write(installer_content)
            os.chmod('install.sh', 0o755)

def main():
    """Main build function."""
    
    builder = WeatherDashboardBuilder()
    
    if builder.build_executable():
        
        # Ask if user wants to create installer
        try:
            create_installer = input("\n❓ Create installer script? (y/N): ").lower().strip()
            if create_installer in ['y', 'yes']:
                builder.create_installer_script()
        except KeyboardInterrupt:
            pass
        
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()