import serial
import time
import sys

PORT        = '/dev/ttyACM0'
BAUDRATE    = 115200
TIMEOUT     = 30

def run_test():
    ser = None
    connection_timeout = 180  # 3 minute timeout for connection
    retry_interval = 5       # Retry every 5 seconds
    start_time = time.time()
    
    # Try to connect to serial port with retries
    print("Attempting to connect to serial port...")
    while time.time() - start_time < connection_timeout:
        try:
            ser = serial.Serial(PORT, BAUDRATE, timeout=2)
            print(f"Connected to {PORT} at {BAUDRATE} baud")
            break
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"Connection failed: {e}. Retrying in {retry_interval}s... ({elapsed:.1f}s elapsed)")
            time.sleep(retry_interval)
    
    if ser is None:
        print(f"Failed to connect to {PORT} after {connection_timeout} seconds")
        return False
    
    try:
        print("Opening CLI...")
        ser.write(b"#CLI\r\n")
        
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore')
                print(line, end='')

        print("\nRunning MFG test...")
        ser.write(b"12\r\n")

        with open("mfg_test_results.log", "w") as f:
            start_time = time.time()
            while time.time() - start_time < TIMEOUT:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore')
                    print(line, end='')
                    f.write(line)
        print(f"\nSaving Results to mfg_test_results.log")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if ser is not None:
            ser.close()
if __name__ == "__main__":
    sys.exit(0 if run_test() else 1)