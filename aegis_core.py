import time
import subprocess
import requests
import logging
import shutil
import os
from datetime import datetime

# --- ⚙️ CONFIGURATION (EDIT THIS) ---

# Services to monitor (Systemd service names)
# Example: 'nginx', 'mysql', 'docker', 'csgo-server'
WATCHLIST = ['nginx', 'mysql', 'ssh', 'cron']

# Disk usage threshold (Percent)
DISK_THRESHOLD = 90

# Discord Webhook URL (Get this from Discord Channel Settings -> Integrations)
# Leave empty string "" to disable alerts.
WEBHOOK_URL = "" 

# How often to check (Seconds)
CHECK_INTERVAL = 10

# Max restarts allowed in a short period before giving up (Flapping protection)
MAX_RETRIES = 3

# --- 🛡️ AEGIS CORE LOGIC ---

# Setup Logging
logging.basicConfig(
    filename='aegis.log',
    level=logging.INFO,
    format='%(asctime)s - [AEGIS] - %(levelname)s - %(message)s'
)

# Retry counter memory
retry_counts = {service: 0 for service in WATCHLIST}

def send_alert(title, message, color=16711680):
    """Sends a professional embed alert to Discord."""
    if not WEBHOOK_URL: return
    
    data = {
        "embeds": [{
            "title": f"🛡️ AEGIS ALERT: {title}",
            "description": message,
            "color": color,
            "footer": {"text": f"Server: {os.uname().nodename}"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

def check_service_status(service):
    """Returns True if service is active, False otherwise."""
    try:
        stat = subprocess.call(["systemctl", "is-active", "--quiet", service])
        return stat == 0
    except Exception as e:
        logging.error(f"Error checking {service}: {e}")
        return False

def restart_service(service):
    """Attempts to restart a systemd service."""
    try:
        logging.warning(f"Attempting to restart {service}...")
        subprocess.run(["systemctl", "restart", service], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def audit_disk():
    """Checks disk space and alerts if critical."""
    total, used, free = shutil.disk_usage("/")
    percent = (used / total) * 100
    if percent > DISK_THRESHOLD:
        msg = f"CRITICAL DISK USAGE: {percent:.2f}% used! System stability at risk."
        logging.critical(msg)
        send_alert("DISK SPACE CRITICAL", msg, color=15548997) # Red

def main():
    print("🛡️ AEGIS AUTOMATION SYSTEM STARTED...")
    print(f"[*] Watching services: {', '.join(WATCHLIST)}")
    send_alert("System Startup", "Aegis Protection Protocol Initiated.", color=3066993) # Green

    while True:
        # 1. Check Services
        for service in WATCHLIST:
            if not check_service_status(service):
                logging.warning(f"Service DOWN: {service}")
                
                if retry_counts[service] < MAX_RETRIES:
                    send_alert("Service Down", f"⚠️ Service **{service}** stopped unexpectedly. Attempting restart...", color=15105570) # Orange
                    success = restart_service(service)
                    
                    if success:
                        logging.info(f"Service {service} successfully restarted.")
                        send_alert("Service Restored", f"✅ Service **{service}** was successfully restarted.", color=3066993) # Green
                        retry_counts[service] += 1
                    else:
                        logging.error(f"Failed to restart {service}.")
                        send_alert("Restart Failed", f"❌ Could not restart **{service}**. Manual intervention required!", color=16711680) # Red
                else:
                    logging.error(f"Service {service} is flapping. Max retries reached.")
                    # Only alert once for flapping
                    if retry_counts[service] == MAX_RETRIES:
                        send_alert("Flapping Detected", f"⛔ Service **{service}** keeps crashing. Auto-restart disabled to protect system.", color=0) # Black
                        retry_counts[service] += 1 # Increment to stop spamming
            else:
                # Reset counter if service is stable
                if retry_counts[service] > 0 and retry_counts[service] <= MAX_RETRIES:
                    retry_counts[service] = 0

        # 2. Check Disk
        audit_disk()

        # 3. Sleep
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("❌ AEGIS must be run as ROOT (sudo) to manage system services.")
        exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping Aegis...")
        
