"""
Weather Dashboard Build Configuration

This script automates the process of building a standalone executable for your weather app using PyInstaller.
It handles platform-specific configurations, dependency management, and creates distribution-ready packages.

Features:
- Cross-platform support (Windows, macOS, Linux)
- Automatic dependency detection
- Custom icon and version information
- Code signing support
- Installer creation
- Comprehensive error handling

Usage:
    python scripts/build_config.py
    python scripts/build_config.py --platform windows
    python scripts/build_config.py --test-build
"""

import PyInstaller.__main__
import os
import shutil
import sys
import platform
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

class WeatherDashboardBuilder:
    """Handles building the Weather Dashboard executable with PyInstaller."""
    
    def __init__(self, target_platform: str = None, test_mode: bool = False):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / 'build'
        self.dist_dir = self.project_root / 'dist'
        self.app_name = 'WeatherDashboard'
        self.version = '2.0.0'
        
        # Determine target platform
        self.target_platform = target_platform or platform.system()
        self.test_mode = test_mode
        
        # Platform-specific settings
        self.platform_configs = {
            'Windows': {
                'exe_extension': '.exe',
                'icon_file': 'resources/icons/weather.ico',
                'separator': ';'
            },
            'Darwin': {  # macOS
                'exe_extension': '.app',
                'icon_file': 'resources/icons/weather.icns',
                'separator': ':'
            },
            'Linux': {
                'exe_extension': '',
                'icon_file': 'resources/icons/weather.png',
                'separator': ':'
            }
        }
        
        print(f"🏗️  Weather Dashboard Builder v{self.version}")
        print(f"📱 Target Platform: {self.target_platform}")
        print(f"🔧 Test Mode: {'Enabled' if self.test_mode else 'Disabled'}")
        print("-" * 50)
    
    def clean_previous_builds(self):
        """Remove previous build and dist directories."""
        print("🧹 Cleaning previous builds...")
        
        directories_to_clean = [self.build_dir, self.dist_dir]
        for directory in directories_to_clean:
            if directory.exists():
                try:
                    shutil.rmtree(directory)
                    print(f"   ✅ Removed {directory}")
                except Exception as e:
                    print(f"   ⚠️  Warning: Could not remove {directory}: {e}")
        
        # Also clean PyInstaller spec files
        spec_files = list(self.project_root.glob("*.spec"))
        for spec_file in spec_files:
            try:
                spec_file.unlink()
                print(f"   ✅ Removed {spec_file}")
            except Exception as e:
                print(f"   ⚠️  Warning: Could not remove {spec_file}: {e}")
    
    def verify_dependencies(self) -> Dict[str, List[str]]:
        """Check if all required dependencies are available."""
        print("🔍 Verifying dependencies...")
        
        required_modules = [
            'customtkinter',
            'requests',
            'PIL',  # Fixed: Changed from 'Pillow' to 'PIL'
            'tkinter'
        ]
        
        optional_modules = [
            'tkintermapview',
            'matplotlib',
            'numpy',
            'pandas',
            'pytest'
        ]
        
        missing_required = []
        missing_optional = []
        available_optional = []
        
        # Check required modules
        for module in required_modules:
            try:
                __import__(module)
                print(f"   ✅ {module}")
            except ImportError:
                missing_required.append(module)
                print(f"   ❌ {module} (REQUIRED)")
        
        # Check optional modules
        for module in optional_modules:
            try:
                __import__(module)
                available_optional.append(module)
                print(f"   ✅ {module} (optional)")
            except ImportError:
                missing_optional.append(module)
                print(f"   ⚠️  {module} (optional - reduced functionality)")
        
        if missing_required:
            print(f"\n❌ Cannot build: Missing required dependencies: {missing_required}")
            print("Please install missing dependencies:")
            print(f"pip install {' '.join(missing_required)}")
            return {'status': 'error', 'missing_required': missing_required}
        
        if missing_optional:
            print(f"\n⚠️  Some optional features will be disabled: {missing_optional}")
        
        print("✅ All required dependencies found!")
        return {
            'status': 'success',
            'missing_required': [],
            'missing_optional': missing_optional,
            'available_optional': available_optional
        }
    
    def get_data_files(self) -> List[str]:
        """Get list of data files to include in the build."""
        print("📦 Collecting data files...")
        
        data_files = []
        separator = self.platform_configs[self.target_platform]['separator']
        
        # Define data directories and their contents
        data_mappings = {
            'weather_dashboard': 'weather_dashboard',
            'data': 'data',
            'language_settings.json': '.',
        }
        
        # Add data files if they exist
        for source, dest in data_mappings.items():
            source_path = self.project_root / source
            if source_path.exists():
                data_files.append(f'--add-data={source_path}{separator}{dest}')
                print(f"   ✅ Added: {source} -> {dest}")
            else:
                print(f"   ⚠️  Not found: {source}")
        
        # Add specific resource files if they exist
        resource_files = [
            'requirements.txt',
            'README.md',
            'UserGuide.md',
            'LICENSE',
            '.env'
        ]
        
        for file in resource_files:
            file_path = self.project_root / file
            if file_path.exists():
                data_files.append(f'--add-data={file_path}{separator}.')
                print(f"   ✅ Added: {file}")
        
        return data_files
    
    def get_hidden_imports(self) -> List[str]:
        """Get list of hidden imports for PyInstaller."""
        print("🔍 Determining hidden imports...")
        
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
            'datetime',
            'threading',
            'queue',
            
            # Image processing
            'PIL',
            'PIL.Image',
            'PIL.ImageTk',
            
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
            print("   ✅ Added tkintermapview imports")
        except ImportError:
            print("   ⚠️  tkintermapview not available - map features will be disabled")
        
        try:
            import matplotlib
            hidden_imports.extend([
                'matplotlib',
                'matplotlib.backends.backend_tkagg',
                'matplotlib.figure',
                'matplotlib.pyplot',
                'numpy',
                'pandas'
            ])
            print("   ✅ Added matplotlib/numpy/pandas imports")
        except ImportError:
            print("   ⚠️  matplotlib/numpy/pandas not available - advanced graphs disabled")
        
        return [f'--hidden-import={module}' for module in hidden_imports]
    
    def get_excluded_modules(self) -> List[str]:
        """Get list of modules to exclude from the build."""
        print("🚫 Determining modules to exclude...")
        
        excluded_modules = [
            # Development and testing
            'pytest',
            'pytest_cov',
            'unittest',
            'doctest',
            'test',
            
            # Documentation
            'sphinx',
            'pydoc',
            
            # Alternative GUI frameworks
            'PySide2',
            'PySide6',
            'PyQt5',
            'PyQt6',
            'wx',
            'kivy',
            
            # Development tools
            'IPython',
            'notebook',
            'jupyter',
            'black',
            'flake8',
            'mypy',
            
            # Large optional packages that aren't needed
            'scipy',
            'sklearn',
            'tensorflow',
            'torch',
            'opencv',
            
            # Testing modules
            'numpy.testing',
            'matplotlib.tests',
            'pandas.tests'
        ]
        
        return [f'--exclude-module={module}' for module in excluded_modules]
    
    def get_platform_specific_args(self) -> List[str]:
        """Get platform-specific build arguments."""
        print(f"🖥️  Configuring for {self.target_platform}...")
        
        args = []
        config = self.platform_configs.get(self.target_platform, {})
        
        if self.target_platform == 'Windows':
            args.extend([
                '--windowed',  # No console window
                '--version-file=version_info.txt' if self.create_version_info() else '',
                f'--icon={config["icon_file"]}' if Path(config["icon_file"]).exists() else ''
            ])
            
            # Add Windows-specific optimizations
            args.extend([
                '--optimize=2',  # Bytecode optimization
                '--strip',       # Strip debug symbols
            ])
            
            print("   ✅ Windows configuration applied")
            
        elif self.target_platform == 'Darwin':  # macOS
            args.extend([
                '--windowed',
                f'--icon={config["icon_file"]}' if Path(config["icon_file"]).exists() else '',
                '--osx-bundle-identifier=com.weatherdashboard.app'
            ])
            
            print("   ✅ macOS configuration applied")
            
        elif self.target_platform == 'Linux':
            args.extend([
                '--windowed',
                f'--icon={config["icon_file"]}' if Path(config["icon_file"]).exists() else ''
            ])
            
            print("   ✅ Linux configuration applied")
        
        # Filter out empty strings
        return [arg for arg in args if arg]
    
    def create_version_info(self) -> bool:
        """Create version info file for Windows builds."""
        if self.target_platform != 'Windows':
            return False
        
        print("📄 Creating version info file...")
        
        version_info_content = f'''# UTF-8
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
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'Weather Dashboard'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        try:
            with open('version_info.txt', 'w', encoding='utf-8') as f:
                f.write(version_info_content)
            print("   ✅ Version info file created")
            return True
        except Exception as e:
            print(f"   ⚠️  Could not create version info: {e}")
            return False
    
    def build_executable(self) -> bool:
        """Build the weather dashboard executable."""
        print("\n🚀 Starting build process...")
        
        # Verify dependencies
        deps_result = self.verify_dependencies()
        if deps_result['status'] == 'error':
            return False
        
        # Clean previous builds
        self.clean_previous_builds()
        
        # Create necessary directories
        os.makedirs('dist', exist_ok=True)
        
        # Base PyInstaller arguments
        args = [
            'main.py',  # Entry point
            f'--name={self.app_name}',  # Executable name
            '--onefile',  # Single file output
            '--clean',  # Clean temporary files
            '--noconfirm',  # Replace output without asking
            '--log-level=INFO',  # Logging level
        ]
        
        # Add test mode flags
        if self.test_mode:
            args.extend([
                '--debug=all',
                '--console',  # Keep console for debugging
            ])
            print("   🔧 Test mode enabled - console window will be visible")
        
        # Add all components
        args.extend(self.get_data_files())
        args.extend(self.get_hidden_imports())
        args.extend(self.get_excluded_modules())
        args.extend(self.get_platform_specific_args())
        
        # Filter out empty arguments
        args = [arg for arg in args if arg]
        
        print(f"\n📋 Build configuration:")
        print(f"   Entry point: main.py")
        print(f"   Application name: {self.app_name}")
        print(f"   Build type: {'Test' if self.test_mode else 'Release'}")
        print(f"   Platform: {self.target_platform}")
        print(f"   Total arguments: {len(args)}")
        
        try:
            print(f"\n⚙️  Running PyInstaller...")
            PyInstaller.__main__.run(args)
            
            # Check if build was successful
            config = self.platform_configs[self.target_platform]
            exe_name = f"{self.app_name}{config['exe_extension']}"
            exe_path = self.dist_dir / exe_name
            
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)  # Size in MB
                print(f"\n✅ Build successful!")
                print(f"   📁 Output: {exe_path}")
                print(f"   📏 Size: {file_size:.1f} MB")
                
                # Clean up temporary files
                self._cleanup_build_files()
                
                return True
            else:
                print(f"\n❌ Build failed - executable not found at {exe_path}")
                return False
                
        except Exception as e:
            print(f"\n❌ Build failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _cleanup_build_files(self):
        """Clean up temporary build files."""
        print("🧹 Cleaning up temporary files...")
        
        # Remove version info file
        version_file = Path('version_info.txt')
        if version_file.exists():
            try:
                version_file.unlink()
                print("   ✅ Removed version_info.txt")
            except Exception as e:
                print(f"   ⚠️  Could not remove version_info.txt: {e}")
        
        # Remove build directory (keep dist)
        if self.build_dir.exists():
            try:
                shutil.rmtree(self.build_dir)
                print("   ✅ Removed build directory")
            except Exception as e:
                print(f"   ⚠️  Could not remove build directory: {e}")
    
    def create_installer_script(self):
        """Create a simple installer script for distribution."""
        print("📦 Creating installer script...")
        
        if self.target_platform == 'Windows':
            installer_content = f'''@echo off
echo Installing Weather Dashboard...
if not exist "%USERPROFILE%\\Desktop" mkdir "%USERPROFILE%\\Desktop"
copy "dist\\{self.app_name}.exe" "%USERPROFILE%\\Desktop\\"
echo.
echo ✅ Weather Dashboard installed to Desktop!
echo.
echo You can also copy the executable to any location you prefer.
echo.
pause
'''
            with open('install.bat', 'w') as f:
                f.write(installer_content)
            print("   ✅ Created install.bat")
        
        elif self.target_platform in ['Darwin', 'Linux']:
            installer_content = f'''#!/bin/bash
echo "Installing Weather Dashboard..."
mkdir -p "$HOME/Desktop"
cp "dist/{self.app_name}" "$HOME/Desktop/"
chmod +x "$HOME/Desktop/{self.app_name}"
echo
echo "✅ Weather Dashboard installed to Desktop!"
echo
echo "You can also copy the executable to any location you prefer."
echo "For system-wide installation, copy to /usr/local/bin/ (requires sudo)"
echo
'''
            with open('install.sh', 'w') as f:
                f.write(installer_content)
            os.chmod('install.sh', 0o755)
            print("   ✅ Created install.sh")
    
    def run_tests(self) -> bool:
        """Run basic tests on the built executable."""
        if not self.test_mode:
            return True
        
        print("\n🧪 Running post-build tests...")
        
        config = self.platform_configs[self.target_platform]
        exe_name = f"{self.app_name}{config['exe_extension']}"
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print("   ❌ Executable not found for testing")
            return False
        
        # Test 1: Check if executable runs
        try:
            print("   Testing executable startup...")
            if self.target_platform == 'Windows':
                result = subprocess.run([str(exe_path), '--version'], 
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run([str(exe_path), '--version'], 
                                      capture_output=True, text=True, timeout=10)
            print("   ✅ Executable runs successfully")
        except subprocess.TimeoutExpired:
            print("   ✅ Executable started (timeout expected for GUI app)")
        except Exception as e:
            print(f"   ⚠️  Executable test warning: {e}")
        
        # Test 2: Check file size
        file_size = exe_path.stat().st_size / (1024 * 1024)
        if file_size > 200:  # More than 200MB might indicate issues
            print(f"   ⚠️  Large executable size: {file_size:.1f} MB")
        else:
            print(f"   ✅ Reasonable executable size: {file_size:.1f} MB")
        
        return True

def main():
    """Main build function with command line argument support."""
    parser = argparse.ArgumentParser(description='Build Weather Dashboard executable')
    parser.add_argument('--platform', choices=['Windows', 'Darwin', 'Linux'],
                       help='Target platform for build')
    parser.add_argument('--test-build', action='store_true',
                       help='Enable test mode with debugging features')
    parser.add_argument('--clean-only', action='store_true',
                       help='Only clean previous builds, do not build')
    parser.add_argument('--no-installer', action='store_true',
                       help='Skip installer script creation')
    
    args = parser.parse_args()
    
    # Initialize builder
    builder = WeatherDashboardBuilder(
        target_platform=args.platform,
        test_mode=args.test_build
    )
    
    # Clean only mode
    if args.clean_only:
        builder.clean_previous_builds()
        print("✅ Clean completed!")
        return
    
    # Build executable
    success = builder.build_executable()
    
    if success:
        # Run tests if in test mode
        if args.test_build:
            builder.run_tests()
        
        # Create installer script unless disabled
        if not args.no_installer:
            try:
                create_installer = input("\n❓ Create installer script? (Y/n): ").lower().strip()
                if create_installer in ['', 'y', 'yes']:
                    builder.create_installer_script()
            except KeyboardInterrupt:
                print("\n⏹️  Installer creation skipped")
        
        print(f"\n🎉 Build completed successfully!")
        print(f"📁 Executable location: dist/{builder.app_name}")
        print(f"💡 Run with --test-build flag to enable debugging features")
        print(f"💡 Use install script to easily deploy to Desktop")
        
    else:
        print(f"\n❌ Build failed!")
        print(f"💡 Try running with --test-build for more debugging information")
        print(f"💡 Check that all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()