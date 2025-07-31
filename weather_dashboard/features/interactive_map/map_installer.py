"""
Map Components Installer
=======================

Utility to install and check map dependencies for the weather dashboard.
"""

import subprocess
import sys
import importlib
import tkinter as tk
from tkinter import ttk, messagebox

def check_dependency(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Installation timed out"
    except Exception as e:
        return False, "", str(e)

def check_all_dependencies():
    """Check status of all required dependencies"""
    dependencies = {
        "tkintermapview": {
            "package": "tkintermapview",
            "import": "tkintermapview",
            "description": "Interactive map widget",
            "required": True
        },
        "requests": {
            "package": "requests", 
            "import": "requests",
            "description": "HTTP requests for geocoding",
            "required": True
        },
        "PIL": {
            "package": "Pillow",
            "import": "PIL",
            "description": "Image processing for weather overlays",
            "required": False
        },
        "flask": {
            "package": "Flask",
            "import": "flask", 
            "description": "Weather tile server",
            "required": False
        }
    }
    
    status = {}
    for name, info in dependencies.items():
        status[name] = {
            **info,
            "installed": check_dependency(info["package"], info["import"])
        }
    
    return status

class MapInstallerGUI:
    def __init__(self, parent=None):
        if parent:
            self.window = tk.Toplevel(parent)
        else:
            self.window = tk.Tk()
        
        self.window.title("Map Components Installer")
        self.window.geometry("600x500")
        self.window.transient(parent)
        
        self.setup_ui()
        self.check_dependencies()

    def setup_ui(self):
        """Setup the installer UI"""
        # Title
        title_label = ttk.Label(self.window, text="Map Components Installer", 
                               font=("TkDefaultFont", 16, "bold"))
        title_label.pack(pady=20)

        # Description
        desc_text = (
            "This tool will install the required components for interactive map functionality.\n"
            "Click 'Check Dependencies' to see what's installed, then 'Install Missing' to install."
        )
        desc_label = ttk.Label(self.window, text=desc_text, justify="center")
        desc_label.pack(pady=10)

        # Buttons frame
        buttons_frame = ttk.Frame(self.window)
        buttons_frame.pack(pady=20)

        self.check_btn = ttk.Button(buttons_frame, text="Check Dependencies", 
                                   command=self.check_dependencies)
        self.check_btn.pack(side="left", padx=10)

        self.install_btn = ttk.Button(buttons_frame, text="Install Missing", 
                                     command=self.install_missing, state="disabled")
        self.install_btn.pack(side="left", padx=10)

        # Status frame
        self.status_frame = ttk.LabelFrame(self.window, text="Dependency Status")
        self.status_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self.window, mode='indeterminate')
        self.progress.pack(fill="x", padx=20, pady=10)

        # Log text area
        log_frame = ttk.LabelFrame(self.window, text="Installation Log")
        log_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.log_text = tk.Text(log_frame, height=8, wrap="word")
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        log_scroll.pack(side="right", fill="y", pady=5)

    def check_dependencies(self):
        """Check and display dependency status"""
        # Clear status frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        self.log("Checking dependencies...")
        
        status = check_all_dependencies()
        
        missing_required = []
        missing_optional = []
        
        for name, info in status.items():
            # Create status row
            row_frame = ttk.Frame(self.status_frame)
            row_frame.pack(fill="x", padx=10, pady=2)
            
            # Status icon
            if info["installed"]:
                icon = "✓"
                color = "green"
            else:
                icon = "✗"
                color = "red"
                if info["required"]:
                    missing_required.append(info)
                else:
                    missing_optional.append(info)
            
            icon_label = ttk.Label(row_frame, text=icon, foreground=color, 
                                  font=("TkDefaultFont", 12, "bold"))
            icon_label.pack(side="left", padx=(0, 10))
            
            # Package info
            info_text = f"{info['package']} - {info['description']}"
            if not info["required"]:
                info_text += " (optional)"
            
            info_label = ttk.Label(row_frame, text=info_text)
            info_label.pack(side="left")

        # Enable install button if there are missing dependencies
        if missing_required or missing_optional:
            self.install_btn.config(state="normal")
            self.log(f"Found {len(missing_required)} missing required and {len(missing_optional)} missing optional packages")
        else:
            self.install_btn.config(state="disabled")
            self.log("All dependencies are installed!")

        self.missing_required = missing_required
        self.missing_optional = missing_optional

    def install_missing(self):
        """Install missing dependencies"""
        self.install_btn.config(state="disabled")
        self.progress.start()
        
        def install_worker():
            try:
                all_packages = self.missing_required + self.missing_optional
                
                for package_info in all_packages:
                    package_name = package_info["package"]
                    self.log(f"Installing {package_name}...")
                    
                    success, stdout, stderr = install_package(package_name)
                    
                    if success:
                        self.log(f"✓ {package_name} installed successfully")
                    else:
                        self.log(f"✗ Failed to install {package_name}: {stderr}")
                
                self.log("Installation complete!")
                
                # Re-check dependencies
                self.window.after(1000, self.check_dependencies)
                
            except Exception as e:
                self.log(f"Installation error: {str(e)}")
            finally:
                self.window.after(0, lambda: [
                    self.progress.stop(),
                    self.install_btn.config(state="normal")
                ])
        
        import threading
        threading.Thread(target=install_worker, daemon=True).start()

    def log(self, message):
        """Add message to log"""
        def update_log():
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.update()
        
        self.window.after(0, update_log)

def show_installer(parent=None):
    """Show the installer GUI"""
    installer = MapInstallerGUI(parent)
    return installer.window

def quick_install():
    """Quick command-line installation"""
    print("Map Components Quick Installer")
    print("=" * 40)
    
    status = check_all_dependencies()
    
    missing = []
    for name, info in status.items():
        if not info["installed"] and info["required"]:
            missing.append(info["package"])
    
    if not missing:
        print("All required dependencies are installed!")
        return True
    
    print(f"Missing required packages: {', '.join(missing)}")
    
    try:
        for package in missing:
            print(f"Installing {package}...")
            success, stdout, stderr = install_package(package)
            
            if success:
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}: {stderr}")
                return False
        
        print("Installation complete!")
        return True
        
    except Exception as e:
        print(f"Installation error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_install()
    else:
        # Show GUI installer
        app = MapInstallerGUI()
        app.window.mainloop()