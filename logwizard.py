import re

LOG_FILE = "auth.log"

SSH_FAIL_PATTERN = re.compile(
    r"Failed password for .* from (?P<ip>[0-9.]+)"
)

def load_log_file():
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except:
        print("Cannot open log file")
        return []

lines = load_log_file()

failed_attempts = {}

for line in lines:
    match = SSH_FAIL_PATTERN.search(line)
    if match:
        ip = match.group("ip")

        if ip not in failed_attempts:
            failed_attempts[ip] = 0

        failed_attempts[ip] += 1

print("Failed attempts per IP:")
print(failed_attempts)
print("\nChecking for brute-force...")

for ip, count in failed_attempts.items():
    if count >= 5:
        print("🚨 BRUTE FORCE DETECTED from", ip, "- Attempts:", count)
import json

alerts = []

for ip, count in failed_attempts.items():
    if count >= 5:
        alert = {
            "ip": ip,
            "attempts": count
        }
        alerts.append(alert)

with open("alerts.json", "w") as f:
    json.dump(alerts, f, indent=4)

print("Alerts saved to alerts.json")
