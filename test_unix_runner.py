import os
from dotenv import load_dotenv
import paramiko

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_USER = os.getenv('SSH_USER')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')
REMOTE_SCRIPT_PATH = os.getenv('REMOTE_SCRIPT_PATH', '/home/kiranmote/job_status_example.sh')

def run_remote_script():
    try:
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_HOST, username=SSH_USER, pkey=key)
        print(f"Connected to {SSH_HOST}")
        stdin, stdout, stderr = ssh.exec_command(f"bash {REMOTE_SCRIPT_PATH}")
        output = stdout.read().decode()
        error = stderr.read().decode()
        print("--- Job Status Output ---")
        print(output)
        if error:
            print("--- Errors ---")
            print(error)
        ssh.close()
        # Check for 'Success' in all job statuses
        if 'Success' in output:
            print("All jobs succeeded. Proceeding to SQL tests.")
            return True
        else:
            print("Some jobs failed. SQL tests will not run.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    run_remote_script()
