import dtlpy as dl
import subprocess
import sys
import os


port = 3000


class Runner(dl.BaseServiceRunner):
    def __init__(self):
        # Run uvicorn as background subprocess to avoid blocking
        cmd = ["uvicorn", "scripts.app:app", "--host", "0.0.0.0", "--port", str(port), "--timeout-keep-alive", "60"]
        
        print(f"Starting uvicorn server on port {port}...")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"Server started with PID: {self.process.pid}")
        print(f"Server running at http://0.0.0.0:{port}")
                
    def __del__(self):
        # Clean up process on exit
        if hasattr(self, 'process') and self.process:
            print("Terminating uvicorn server...")
            self.process.terminate()
    def run(self):
        pass


if __name__ == "__main__":
    run = Runner()