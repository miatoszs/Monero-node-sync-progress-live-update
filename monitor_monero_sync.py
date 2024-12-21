import requests
import time
import os

# Configuration
NODE_URL = "http://192.168.2.124:18081/json_rpc"
CHECK_INTERVAL = 10  # Time in seconds between checks

def get_sync_status():
    """
    Fetch synchronization status from Monero node.
    """
    try:
        response = requests.post(
            NODE_URL,
            json={
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_info"
            },
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                return data["result"]
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def monitor_sync():
    """
    Monitor and display synchronization progress in a single terminal view.
    """
    while True:
        os.system('clear')  # Clear the terminal for updated output
        status = get_sync_status()
        if status:
            height = status.get("height", 0)
            target_height = status.get("target_height", 1)
            busy_syncing = status.get("busy_syncing", False)
            synchronized = status.get("synchronized", False)

            progress = (height / target_height) * 100 if target_height > 0 else 0
            print("Monitoring Monero Node Synchronization Progress...\n")
            print(f"Current Block Height:   {height}")
            print(f"Target Block Height:    {target_height}")
            print(f"Synchronization Progress: {progress:.2f}%")
            print(f"Busy Syncing:           {busy_syncing}")
            print(f"Fully Synchronized:     {synchronized}")

            if synchronized:
                print("\nNode is fully synchronized!")
                break
        else:
            print("Failed to fetch synchronization status. Retrying...\n")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_sync()
