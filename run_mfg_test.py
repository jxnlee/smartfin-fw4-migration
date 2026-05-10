import serial
import time
import sys

PORT        = '/dev/ttyACM0'
BAUDRATE    = 115200
TIMEOUT     = 30

def run_test():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=2)

        print("Opening CLI...")
        ser.write(b"#CLI\r\n")
        
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore')
                print(line, end='')

        print("Running MFG test...")
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
if __name__ == "__main__":
    sys.exit(0 if run_test() else 1)