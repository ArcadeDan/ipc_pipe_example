import psutil
import subprocess
import requests
import time
import os
import select
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer

exit_flag = threading.Event()

def get_message(fifo):
    return os.read(fifo, 24)
    
def process_message(msg):
    return msg

def ipc_handler():
    IPC_FIFO_NAME_A = "pipe_a"
    IPC_FIFO_NAME_B = "pipe_b"

    os.mkfifo(IPC_FIFO_NAME_A)

    try:
        fifo_a = os.open(IPC_FIFO_NAME_A, os.O_RDONLY | os.O_NONBLOCK)
        print("Pipe A ready")

        while not exit_flag.is_set():
            try:
                fifo_b = os.open(IPC_FIFO_NAME_B, os.O_WRONLY)
                print("Pipe B ready")
                break
            except:
                pass

        try:
            poll = select.poll()
            poll.register(fifo_a, select.POLLIN)

            try:
                while not exit_flag.is_set():
                    if (fifo_a, select.POLLIN) in poll.poll(1000):
                        msg = get_message(fifo_a)
                        msg = process_message(msg)
                        os.write(fifo_b, msg)

                        print("------ Received from JS ------")
                        print("     " + msg.decode("utf-8"))
                        print("-------------------------------")
            finally:
                poll.unregister(fifo_a)
        finally:
            os.close(fifo_b)
    finally:
        os.remove(IPC_FIFO_NAME_A)
        os.remove(IPC_FIFO_NAME_B) 

if __name__ == "__main__":
    def cleanup():
        print("========== Stopping Node Server ==========")
        for p in psutil.process_iter():
            if p.name() == "node":
                p.terminate()
                p.wait()

        njs.terminate()
        njs.wait()

    njs = subprocess.Popen(["npm", "run", "start"])

    ipc_thread = threading.Thread(target=ipc_handler)
    ipc_thread.start()


    while True:
        if input() == ":q":
            break

    exit_flag.set()
    ipc_thread.join()
    cleanup()
    exit(0)