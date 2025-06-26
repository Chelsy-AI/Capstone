import requests
from PIL import Image, ImageTk
import io

def display_weather(data, temp_label, desc_label, update_label, icon_label, app):
    try:
        temp_c = data["main"]["temp"]
        temp_f = temp_c * 9 / 5 + 32
        temp = f"{round(temp_c)} °C" if app.unit == "C" else f"{round(temp_f)} °F"

        temp_label.configure(text=temp)

        weather = data["weather"][0]
        desc = weather["description"].capitalize()
        desc_label.configure(text=desc)

        from datetime import datetime
        update_time = datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M UTC")
        update_label.configure(text=f"Updated at: {update_time}")

        # Weather Icon
        icon_code = weather["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(icon_url)
        image = Image.open(io.BytesIO(response.content)).convert("RGBA")
        app.original_icon = image  # Store original for rotation
        rotated = image.rotate(app.icon_angle)
        app.icon_image = ImageTk.PhotoImage(rotated)
        icon_label.configure(image=app.icon_image)
        icon_label.image = app.icon_image  # Keep reference
        animate_icon(app)

    except Exception as e:
        temp_label.configure(text="N/A")
        desc_label.configure(text="No description")
        update_label.configure(text="Updated at: Unknown")
        print("Error displaying weather:", e)

def animate_icon(app):
    try:
        app.icon_angle = (app.icon_angle + 10) % 360
        rotated = app.original_icon.rotate(app.icon_angle)
        app.icon_image = ImageTk.PhotoImage(rotated)
        app.icon_label.configure(image=app.icon_image)
        app.root.after(50, lambda: animate_icon(app) if app.icon_angle != 0 else None)
    except Exception as e:
        print("Icon animation error:", e)
