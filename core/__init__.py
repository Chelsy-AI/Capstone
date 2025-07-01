from .app import WeatherApp, run_app

# Entry point function to launch the weather app
def run_app():
    app = WeatherApp()
    app.mainloop()
