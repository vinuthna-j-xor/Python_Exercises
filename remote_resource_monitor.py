import paramiko
import time

HOST = "10.81.1.116"
USERNAME = "interns"
PASSWORD = "123123"
INTERVAL = 5
ALERT_LOG = "alerts.log"



def run_cmd(shell, cmd):
    shell.send(cmd + "\n")
    time.sleep(0.8) 

    output = shell.recv(20000).decode(errors="ignore")

    lines = output.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line == cmd:
            continue

        
        if line.endswith("$") or line.endswith("#"):
            continue

        cleaned.append(line)

    return "\n".join(cleaned).strip()



def monitor_remote():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connecting...")
    client.connect(HOST, username=USERNAME, password=PASSWORD)

    shell = client.invoke_shell()
    time.sleep(1)
    shell.recv(10000)  

    print("Connected. Starting monitoring...\n")

    while True:
        print("----------")

        cpu_output = run_cmd(shell, "top -bn1 | head -5")
        print(cpu_output)

        cpu_line = ""
        for line in cpu_output.splitlines():
            if "%Cpu" in line or "Cpu(s)" in line:
                cpu_line = line
                break

        cpu_usage = 0
        if cpu_line:
            try:
                parts = cpu_line.replace(",", "").split()
                us = float(parts[1])  
                sy = float(parts[3]) 
                cpu_usage = us + sy
            except:
                cpu_usage = 0

       
        mem_output = run_cmd(shell, "free -m")
        print(mem_output)

       
        disk_output = run_cmd(shell, "df -h | tail -1")
        print(disk_output)

        disk_percent = 0

        for ln in disk_output.splitlines():
            ln = ln.strip()
            if not ln or not ln.startswith("/"):
                continue

            parts = ln.split()
            if len(parts) >= 5:
                try:
                    disk_percent = int(parts[4].replace("%", ""))
                except:
                    disk_percent = 0

        print("----------")

        if cpu_usage > 80 or disk_percent > 90:
            with open(ALERT_LOG, "a") as log:
                log.write(
                    f"ALERT: CPU={cpu_usage:.1f}% Disk={disk_percent}%\n"
                )
            print("⚠️ ALERT WRITTEN TO LOG")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    monitor_remote()
