from win32 import win32pipe, win32file
import time

PIPE_NAME = r'\\.\pipe\serverpipe'

# Create named pipe
print(f"Creating named pipe: {PIPE_NAME}")
pipe = win32pipe.CreateNamedPipe(
    PIPE_NAME,
    win32pipe.PIPE_ACCESS_OUTBOUND,  # Write-only
    win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,  # Byte mode, blocking
    1, 65536, 65536,
    0,
    None
)

print("Waiting for a client to connect...")
win32pipe.ConnectNamedPipe(pipe, None)  # Wait for a client

print("Client connected. Sending data...")
for i in range(5):
    message = f"Hello {i}\n".encode()
    win32file.WriteFile(pipe, message)
    time.sleep(1)

print("Closing pipe.")
win32file.CloseHandle(pipe)
