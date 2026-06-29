import os

# ─────────────────────────────────────────────
#  Project-relative paths  (edit ONLY this block)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERTS_DIR = os.path.join(BASE_DIR, "certs")

# AWS IoT credentials  ← put your 3 files inside the certs/ folder
ROOT_CA_PATH        = os.path.join(CERTS_DIR, "AmazonRootCA1.pem")
CERTIFICATE_PATH    = os.path.join(CERTS_DIR, "certificate.pem.crt")
PRIVATE_KEY_PATH    = os.path.join(CERTS_DIR, "private.pem.key")

# AWS IoT endpoint
AWS_HOST  = "a2coc9n67c4b7d-ats.iot.eu-north-1.amazonaws.com"  # ← change to your endpoint
AWS_PORT  = 8883
AWS_TOPIC = "test/topic"                                         # ← change to your topic

# ─────────────────────────────────────────────
#  Network addresses  (change to match your setup)
# ─────────────────────────────────────────────
# Raspberry Pi (this device) – listens here for incoming sensor data
RPI_HOST = "192.168.1.107"
RPI_PORT = 12345

# Second server – receives forwarded data
TARGET_HOST = "192.168.2.100"
TARGET_PORT = 5000

# CSV output file (saved beside this config)
CSV_FILE_PATH = os.path.join(BASE_DIR, "socket_data.csv")
