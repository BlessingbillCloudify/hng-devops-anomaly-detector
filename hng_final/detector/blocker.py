import subprocess

class Blocker:
    def block_ip(self, ip):
        try:
            # Add to iptables
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
            print(f"!!! BLOCKED: {ip}")
            return True
        except:
            return False

    def unblock_ip(self, ip):
        try:
            subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
            print(f"*** UNBLOCKED: {ip}")
            return True
        except:
            return False

