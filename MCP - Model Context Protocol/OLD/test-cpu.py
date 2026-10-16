import subprocess

def get_cpu_usage():
    result = subprocess.run(['top', '-l', '1', '-n', '0'], capture_output=True, text=True)
    return result #round(100 - idle, 1)

health = get_cpu_usage()
print(health.stdout)