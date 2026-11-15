
"""
Handler:
---------------------------------
Parses and executes commands sent by client.py:
UPLOAD, DOWNLOAD, DIR, SUBFOLDER, and DELETE.
"""

import os
import shutil
from storage import load_meta, save_meta, get_logical, CONNECTIONS, lock
from config import SERVER_STORAGE

def handle(sock, addr):
    """Handles an individual client connection loop in its own thread."""
    try:
        while data := sock.recv(1024):
            msg = data.decode('utf-8').strip()
            
            # ----------------------------------
            # 1. UPLOAD PROTOCOL
            # ----------------------------------
            if msg.startswith("UPLOAD:"):
                _, orig, size_str = msg.split(":")
                size = int(size_str)
                lname = get_logical(orig)
                path = os.path.join(STORAGE, lname)
                
                # Check if file already exists on server
                if os.path.exists(path):
                    sock.sendall(b"EXISTS")
                    if sock.recv(1024).decode('utf-8').strip().lower() != 'y':
                        continue
                else:
                    sock.sendall(b"OK")
                
                # Receive file binary stream in chunks (4KB buffer)
                received = 0
                with open(path, "wb") as f:
                    while received < size:
                        chunk = sock.recv(min(4096, size - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                        
                sock.sendall(f"Saved as {lname}".encode('utf-8'))

            # ----------------------------------
            # 2. DOWNLOAD PROTOCOL
            # ----------------------------------
            elif msg.startswith("DOWNLOAD:"):
                fname = msg.split(":")[1]
                path = os.path.join(STORAGE, fname)
                
                # Fallback check if requested via original filename
                if not os.path.exists(path):
                    meta = load_meta()
                    path = next((os.path.join(STORAGE, l) for l, i in meta.items() if i["orig"] == fname), path)
                    
                if not os.path.exists(path):
                    sock.sendall(b"ERROR: Not found")
                    continue
                
                # Send file size and wait for client acknowledgment
                size = os.path.getsize(path)
                sock.sendall(f"SIZE:{size}".encode('utf-8'))
                
                if "ACK" not in sock.recv(1024).decode('utf-8'):
                    continue
                    
                # Stream file data back in chunks
                with open(path, "rb") as f:
                    while chunk := f.read(4096):
                        sock.sendall(chunk)

            # ----------------------------------
            # 3. DIRECTORY LISTING
            # ----------------------------------
            elif msg == "DIR":
                meta = load_meta()
                files = os.listdir(STORAGE)
                listing = "\n".join([f"{f} -> Original: {meta.get(f, {}).get('orig', f)}" for f in files])
                sock.sendall(listing.encode('utf-8') or b"Directory is empty.")

            # ----------------------------------
            # 4. Authorization
            # ----------------------------------
            elif msg.startswith("SUBFOLDER:"):
                # Authorization: ensure client has admin role
                if CONNECTIONS.get(addr, {}).get("role") != "admin":
                    sock.sendall(b"ERROR: Unauthorized access.")
                    continue
                    
                _, action, sub = msg.split(":", 2)
                p = os.path.join(STORAGE, sub)
                
                if action == "create":
                    os.makedirs(p, exist_ok=True)
                    sock.sendall(b"Subfolder created successfully.")
                elif action == "delete":
                    shutil.rmtree(p, ignore_errors=True)
                    sock.sendall(b"Subfolder deleted successfully.")

            # ----------------------------------
            # 5. FILE DELETION (authorization)
            # ----------------------------------
            elif msg.startswith("DELETE:"):
                # Authorization: ensure client has admin role
                if CONNECTIONS.get(addr, {}).get("role") != "admin":
                    sock.sendall(b"ERROR: Unauthorized access.")
                    continue
                    
                fname = msg.split(":")[1]
                path = os.path.join(STORAGE, fname)
                
                if os.path.exists(path):
                    os.remove(path)
                    # Clean up metadata record
                    meta = load_meta()
                    meta = {k: v for k, v in meta.items() if v["orig"] != fname and k != fname}
                    save_meta(meta)
                    sock.sendall(b"File deleted successfully.")
                else:
                    sock.sendall(b"ERROR: File not found.")
                    
    except Exception as e:
        print(f"[ERROR] Session error with {addr}: {e}")
    finally:
        # Cleanup connection pool and close socket on disconnect
        with lock:
            CONNECTIONS.pop(addr, None)
        sock.close()