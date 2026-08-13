print("App Started")

from flask import Flask, render_template, request
import pandas as pd
import os
import smtplib
from datetime import date
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import screen_tracker
from fatigue_camera import detect_fatigue
import activity_monitor

app = Flask(__name__)

# ---------- START TRACKING ----------
threading.Thread(target=screen_tracker.start_tracking, daemon=True).start()

# ---------- LOAD DATA ----------
df = pd.read_csv("burnout_history.csv")

df['burnout_risk'] = df['burnout_risk'].map({
    'Low': 0,
    'Medium': 1,
    'High': 2
})

df = pd.get_dummies(df, columns=['day_type'], drop_first=True)
df = df.drop('user_id', axis=1)

X = df.drop('burnout_risk', axis=1)
y = df['burnout_risk']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(max_iter=500)
model.fit(X_scaled, y)

# ---------- PREDICT FUNCTION ----------
def predict_burnout(work, sleep):

    new_data = pd.DataFrame([{
        "work_hours": work,
        "screen_time_hours": 8,
        "meetings_count": 3,
        "breaks_taken": 2,
        "after_hours_work": 1,
        "sleep_hours": sleep,
        "task_completion_rate": 80,
        "burnout_score": 20,
        "day_type_Weekend": 0
    }])

    new_scaled = scaler.transform(new_data)
    pred = model.predict(new_scaled)[0]

    if pred == 0:
        return 20
    elif pred == 1:
        return 50
    else:
        return 80


# ---------- FINAL LEVEL ----------
def final_level(score):
    if score > 70:
        return "HIGH"
    elif score > 40:
        return "MEDIUM"
    else:
        return "LOW"


# ---------- EMAIL ----------
# ---------- EMAIL ----------

def send_final_email(receiver, burnout, fatigue, final_score, level):

    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver
    msg["Subject"] = "Final Stress Report"

    text = f"""
Burnout Risk: {burnout}%
Fatigue Detected: {"Yes" if fatigue else "No"}
Final Stress Score: {final_score}%
Stress Level: {level}

Suggestions:
Take regular breaks
Maintain proper sleep
Reduce screen usage
Stay hydrated
"""

    msg.attach(MIMEText(text, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, password)

    server.sendmail(
        sender_email,
        receiver,
        msg.as_string()
    )

    server.quit()
# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


# 🔥 SINGLE BUTTON ROUTE
@app.route("/analyze_all", methods=["POST"])
def analyze_all():
    email = request.form["email"]
    work = int(request.form["work"])
    sleep = int(request.form["sleep"])

    print("Starting Full Analysis...")

    # 1. Burnout Prediction
    burnout_risk = predict_burnout(work, sleep)

    # 2. Fatigue Detection (Face Scan)
    fatigue = detect_fatigue()

    # 3. Combine
    fatigue_score = 20 if fatigue else 0
    final_score = min(burnout_risk + fatigue_score, 100)

    # 4. Final Level
    level = final_level(final_score)

    # 5. Send ONE mail
    send_final_email(email, burnout_risk, fatigue, final_score, level)

    return render_template(
        "result.html",
        burnout=burnout_risk,
        fatigue=fatigue,
        final_score=final_score,
        level=level
    )


# ---------- MAIN ----------
if __name__ == "__main__":
    activity_monitor.start_monitor()
    app.run(debug=True)
