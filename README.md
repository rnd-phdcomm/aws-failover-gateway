# RPi IoT Pipeline

Streams sensor data from a Raspberry Pi → second server, with AWS IoT + CSV fallback.

## Quick Start

1. Clone this repo
2. Copy your 3 AWS cert files into `certs/`
3. Edit **`config.py`** (IPs, AWS endpoint, topic)
4. `pip install -r requirements.txt`
5. Run `second_server.py` on the target machine
6. Run `main_receiver.py` on the Pi
7. Run `RpiSend.py` on the sender

See the full setup guide: `RPi_IoT_Setup_Guide.docx`

## Files

| File | Purpose |
|------|---------|
| `config.py` | All settings — **only file you need to edit** |
| `main_receiver.py` | Main Pi server with fallback logic |
| `RpiSend.py` | Sender / client |
| `second_server.py` | Target server that receives forwarded data |
| `certs/` | AWS certificates — **never pushed to GitHub** |
