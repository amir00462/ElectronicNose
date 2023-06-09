import subprocess

def createNetwork():
    subprocess.run(["netsh", "wlan", "set", "hostednetwork", "mode=allow", "ssid=mhshsee", "key=mhshseghe"],capture_output=True)
    subprocess.run(["netsh", "wlan", "start", "hostednetwork"], capture_output=True)

    output = subprocess.run(["netsh", "wlan", "show", "hostednetwork"], capture_output=True, text=True)
    if "Status                 : Started" in output.stdout:
        print("Hosted network started successfully!")
    else:
        print("Error: Hneosted network failed to start.")

if __name__ == '__main__':
    createNetwork()