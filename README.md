# 🛡️ AEGIS Automation System

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![DevOps](https://img.shields.io/badge/role-SRE%20%2F%20DevOps-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/system-autonomous-success?style=for-the-badge)

**An Automated Self-Healing Infrastructure & Incident Response Tool for High-Availability Servers.**

Aegis is not just a monitoring script; it is an active protection system designed to ensure **99.9% Uptime** for your critical services. It detects failures in real-time and performs automated recovery actions (Self-Healing) without human intervention.

## ⚡ CORE CAPABILITIES

### 1. Autonomous Self-Healing
If a critical service (e.g., Nginx, MySQL, Game Server) crashes, Aegis detects it instantly and attempts to **automatically restart** the process. This minimizes downtime from minutes to milliseconds.

### 2. Flapping Protection (Anti-Loop)
Intelligent logic prevents "restart loops". If a service keeps crashing (e.g., due to bad configuration), Aegis stops restarting it after `MAX_RETRIES` to prevent CPU overload and alerts the administrator.

### 3. Real-Time Incident Alerting
Integrated with **Discord Webhooks**. Get instant notifications on your phone when:
* A service goes down.
* A service is successfully restored (Self-Healed).
* Disk space reaches critical levels.

### 4. Audit Logging
Every action is recorded in `aegis.log` with precise timestamps, providing a clear audit trail for root cause analysis.

## 🛠️ CONFIGURATION

Open `aegis_core.py` and modify the configuration block:

```python
# List the systemd service names you want to protect
WATCHLIST = ['nginx', 'mysql', 'csgo-server']

# Add your Discord Webhook URL for alerts
WEBHOOK_URL = "[https://discord.com/api/webhooks/](https://discord.com/api/webhooks/)..."
```

## 📥 DEPLOYMENT

### 1. Download
```bash
git clone [https://github.com/aaron-devop/aegis-automation.git](https://github.com/aaron-devop/aegis-automation.git)
cd aegis-automation
```

### 2. Run as Daemon (Background Service)
Since Aegis manages system services, it requires root privileges.

```bash
# Start in background
nohup sudo python3 aegis_core.py &
```

### 3. Verify
Check the logs to confirm Aegis is active:
```bash
tail -f aegis.log
```

## 📊 USAGE SCENARIO

1.  **Incident:** The MySQL database crashes due to memory overload at 03:00 AM.
2.  **Detection:** Aegis detects the `active` state is `failed`.
3.  **Action:** Aegis executes `systemctl restart mysql`.
4.  **Result:** MySQL is back online in 2 seconds.
5.  **Notification:** You wake up to a green notification: *"✅ Service MySQL was successfully restarted."*

## 📜 LICENSE
MIT License
