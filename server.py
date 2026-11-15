 
"""
Main Server Entry Point
-----------------------
Initializes storage, binds the TCP socket, and spawns 
multithreaded worker threads for incoming client connections.
"""

import socket
import threading
from config import HOST, PORT
from storage import init, CONNECTIONS, lock
from handler import handle

def main():
    # Setup directories and metadata
    init()
    
    # Create TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR allows immediate port reuse after restarting the server
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind((HOST, PORT))
    s.listen(10)
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    
    try:
        while True:
            # Accept incoming client connections
            sock, addr = s.accept()
            print(f"[CONNECTION] Accepted connection from {addr[0]}:{addr[1]}")
            
            # Register client in connection pool with default authorization role
            with lock:
                CONNECTIONS[addr] = {"role": "admin"}
                
            # Spawn a new daemon thread to handle this client concurrently
            threading.Thread(target=handle, args=(sock, addr), daemon=True).start()
            
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down gracefully...")
    finally:
        s.close()

if __name__ == "__main__":
    main()