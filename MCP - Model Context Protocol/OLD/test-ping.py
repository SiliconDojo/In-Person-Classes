import subprocess

def get_cpu_usage():
    result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True)
    return result 

health = get_cpu_usage()
print(health.stdout)