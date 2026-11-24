# CalmPath – setup
1. https://console.firebase.google.com → Add project.
2. Build → Authentication → Get started → enable **Email/Password**.
3. Build → Firestore Database → Create database (production mode). Open the **Rules** tab, paste `firestore.rules`, Publish.
4. Project settings → Your apps → Web (</>) → register → copy the config values into `cfg` near the top of the script in `index.html`.
5. Authentication → Settings → Authorized domains: `localhost` is allowed by default.
6. Run (Firebase auth needs http, not file://):  `python -m http.server 8000` in this folder → open http://localhost:8000
7. Deploy (optional): `npm i -g firebase-tools && firebase login && firebase init hosting && firebase deploy`

Notes
- The recommendation engine is rule-based. It runs in the browser (index.html) so the app works end to end; `recommender.py` is the same logic in Python, ready to be moved behind a Cloud Function / Flask API or swapped for an ML model once you have labelled data.
- Durations are stored in seconds. Charts use saved Firestore data only; no sample activity is inserted.
- Stress % is self-reported, not a diagnosis.

## Arduino sensors (MPU6050 + heart-rate sensor)
- Wiring: MPU6050 VCC/GND/SDA/SCL to the board's 3.3V-5V/GND/SDA/SCL (A4/A5 on Uno/Nano); pulse sensor signal to A0.
- Upload `arduino_sensor/arduino_sensor.ino`, close the Arduino Serial Monitor, then in the app open Start Exercise, click **Connect Arduino sensors** and choose the board's port (Chrome or Edge, on localhost or https).
- While the timer runs, the app records heart-rate samples (average/max saved with the session) and counts movement peaks from the MPU6050; the count pre-fills the repetitions box and you can edit it. Without sensors, manual mode still works.
- If you use a MAX30102 or another heart sensor, change the beat-detection part of the sketch; the app only needs lines of `bpm,ax,ay,az`.
