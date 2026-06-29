# RPi IoT Pipeline

Streams sensor data from a Raspberry Pi to a second server, with automatic fallback to AWS IoT Core + CSV if the second server goes offline.

```
RpiSend.py  →  main_receiver.py  →  second_server.py
                               ↘  (fallback)  AWS IoT + CSV
```

---

## Project Structure

```
rpi-iot-project/
├── config.py             ← All settings in ONE place (IPs, ports, paths)
├── main_receiver.py      ← Run on Raspberry Pi – main server script
├── RpiSend.py            ← Run on sender device – sends data every 5s
├── second_server.py      ← Run on second server – receives forwarded data
├── certs/                ← Put your AWS certificates here (NOT on GitHub)
│   ├── AmazonRootCA1.pem
│   ├── certificate.pem.crt
│   └── private.pem.key
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rpi-iot-project.git
cd rpi-iot-project
```

---

## Step 2 — Install Dependencies

Run this on the Raspberry Pi (and any machine running the scripts):

```bash
pip install -r requirements.txt
```

---

## Step 3 — Add Your AWS Certificates

Go to your downloaded AWS certificate files and rename them to match exactly:

| Your downloaded file                        | Rename to                  |
|---------------------------------------------|----------------------------|
| `AmazonRootCA1.pem`                         | `AmazonRootCA1.pem` (same) |
| `certificate` (the Security Certificate)    | `certificate.pem.crt`      |
| `private.pem.key`                           | `private.pem.key` (same)   |

Then copy all 3 files into the `certs/` folder:

```bash
cp /path/to/AmazonRootCA1.pem    ~/rpi-iot-project/certs/
cp /path/to/certificate.pem.crt  ~/rpi-iot-project/certs/
cp /path/to/private.pem.key      ~/rpi-iot-project/certs/
```

> **Note:** The `certs/` folder is excluded from GitHub via `.gitignore` — your keys will never be pushed accidentally.

---

## Step 4 — Edit config.py

Open `config.py` — this is the **only file you need to change**. Update these values:

### Network IPs & Ports

```python
RPI_HOST    = "192.168.1.107"   # ← IP of your Raspberry Pi  (run: hostname -I)
RPI_PORT    = 12345             # ← Port Pi listens on (change only if port is in use)

TARGET_HOST = "192.168.2.100"   # ← IP of your second / receiving server
TARGET_PORT = 5000              # ← Port of second server
```

### AWS IoT Settings

```python
AWS_HOST  = "a2coc9n67c4b7d-ats.iot.eu-north-1.amazonaws.com"  # ← Your AWS IoT endpoint
AWS_TOPIC = "test/topic"                                         # ← Your MQTT topic name
```

> To find your AWS endpoint: Go to **AWS Console → IoT Core → Settings → Device data endpoint**

### Certificate Paths (already set — no changes needed)

```python
ROOT_CA_PATH     = os.path.join(CERTS_DIR, "AmazonRootCA1.pem")
CERTIFICATE_PATH = os.path.join(CERTS_DIR, "certificate.pem.crt")
PRIVATE_KEY_PATH = os.path.join(CERTS_DIR, "private.pem.key")
```

These auto-resolve relative to the project folder — no hardcoded paths needed.

---

## Step 5 — Run the Scripts (in this order)

### 1. Start the second server
Run on the machine at `TARGET_HOST`:

```bash
python second_server.py
```

### 2. Start the main receiver on the Raspberry Pi

```bash
python main_receiver.py
```

### 3. Start the sender

```bash
python RpiSend.py
```

You should see output like:
```
Sent: 2026-06-30 10:00:00: Hello, Server! - Random Number: 342
```

---

## Step 6 — Push to GitHub (First Time Only)

```bash
cd ~/rpi-iot-project
git init
git remote add origin https://github.com/YOUR_USERNAME/rpi-iot-project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

> The `.gitignore` will automatically exclude `certs/` and `*.csv` files.

---

## How the Fallback Works

| Situation | What happens |
|-----------|-------------|
| Second server is online | Data is forwarded directly via socket |
| Second server goes offline | Data is saved to `socket_data.csv` + published to AWS IoT |
| Second server comes back | Forwarding resumes automatically |

---

## Quick Settings Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `RPI_HOST` | `192.168.1.107` | IP of your Raspberry Pi |
| `RPI_PORT` | `12345` | Port the Pi listens on |
| `TARGET_HOST` | `192.168.2.100` | IP of second server |
| `TARGET_PORT` | `5000` | Port of second server |
| `AWS_HOST` | `…iot.eu-north-1…` | Your AWS IoT endpoint URL |
| `AWS_TOPIC` | `test/topic` | MQTT topic name |
| `CSV_FILE_PATH` | `socket_data.csv` | Saved beside config.py |
