import eel
import sys
import socket
import time
import os

# Initialize eel with your web folder
eel.init('web')  # Change 'web' to your actual folder name containing index.html


class ChatBot:
    started = False
    userinput = []

    @staticmethod
    def start():
        """Start the eel server with automatic port selection"""

        # Try multiple ports automatically
        ports_to_try = [27005, 8000, 8080, 8888, 9000, 0]  # 0 = auto-select

        for port in ports_to_try:
            try:
                if port == 0:
                    print("Letting OS choose an available port...")
                else:
                    print(f"Trying to start Eel server on port {port}...")

                ChatBot.started = True

                # Start eel server
                eel.start(
                    'index.html',
                    mode='default',
                    host='localhost',
                    port=port,
                    block=True,
                    size=(1000, 600),
                    position=(100, 100),
                    close_callback=ChatBot.on_close
                )

                # If we get here, server started successfully
                print(f"✅ Server started successfully on port {port}")
                break

            except OSError as e:
                if "10048" in str(e) or "address already in use" in str(e).lower():
                    if port == 0:
                        print("❌ Failed to start server even with auto port selection")
                        print("Please close other Python processes and try again")
                        ChatBot.started = False
                        break
                    else:
                        print(f"⚠️ Port {port} is busy, trying next port...")
                        continue
                else:
                    print(f"❌ Error: {str(e)}")
                    ChatBot.started = False
                    raise

            except (SystemExit, KeyboardInterrupt):
                print("Server stopped by user")
                ChatBot.started = False
                break

            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                ChatBot.started = False
                if port == ports_to_try[-1]:  # Last port in list
                    raise
                continue

    @staticmethod
    def on_close(page, sockets):
        """Called when browser window is closed"""
        print("Browser window closed")
        ChatBot.started = False

    @staticmethod
    @eel.expose
    def addUserInput(text):
        """Called from JavaScript to add user input"""
        ChatBot.userinput.append(text)
        print(f"User input added: {text}")

    @staticmethod
    def isUserInput():
        """Check if there's user input"""
        return len(ChatBot.userinput) > 0

    @staticmethod
    def popUserInput():
        """Get and remove the first user input"""
        if len(ChatBot.userinput) > 0:
            return ChatBot.userinput.pop(0)
        return None

    @staticmethod
    def close():
        """Close the chatbot"""
        print("Closing ChatBot...")
        ChatBot.started = False
        try:
            eel.sleep(1.0)
            sys.exit(0)
        except:
            pass

    @staticmethod
    def addAppMsg(msg):
        """Send message from app to UI"""
        try:
            eel.addAppMsg(msg)
        except Exception as e:
            print(f"Message (UI not available): {msg}")
            print(f"Error: {str(e)}")


# Expose Python functions to JavaScript
@eel.expose
def addUserMsg(msg):
    """Called from JavaScript when user sends a message"""
    print(f"User message: {msg}")
    ChatBot.addUserInput(msg)


# Helper function to kill processes on port (Windows only)
def kill_process_on_port(port):
    """Kill process using specified port (Windows)"""
    try:
        import subprocess
        # Find process using the port
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}")
                    subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                    time.sleep(1)
                    return True
        return False
    except Exception as e:
        print(f"Error killing process: {str(e)}")
        return False


# For testing
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Proton ChatBot Server...")
    print("=" * 60)

    # Optional: Try to kill existing processes on port 27005
    # Uncomment if you want automatic cleanup:
    # kill_process_on_port(27005)

    ChatBot.start()