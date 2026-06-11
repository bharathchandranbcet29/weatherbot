import os
import requests
import smtplib
from email.message import EmailMessage

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Thiruvananthapuram"

EMAIL = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")
# Weather API
url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}"
    f"&appid={API_KEY}"
    f"&units=metric"
)

data = requests.get(url).json()

if "main" not in data:
    print("Weather API Error")
    print(data)
    exit()

temp = data["main"]["temp"]
condition = data["weather"][0]["main"]

print("Temperature:", temp)
print("Condition:", condition)

# Alert Logic
if temp > 35 or condition.lower() == "rain":

    msg = EmailMessage()

    msg["Subject"] = "Weather Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content(
        f"""
Weather Alert!

City: {CITY}
Temperature: {temp}°C
Condition: {condition}

Take necessary precautions.
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

    print("Alert email sent!")

else:

    print("Weather is normal. No email sent.")