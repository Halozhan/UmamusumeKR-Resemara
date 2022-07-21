import threading
import time

def waiter():
    while not event.is_set():
        print("시작함")
        time.sleep(0.5)
    print("자식 스레드 종료")

event = threading.Event()
worker = threading.Thread(target=waiter, daemon=True)
worker.start()
time.sleep(0.001)

print(worker.is_alive())
time.sleep(2)
event.set()
time.sleep(0.2)
# worker.join()
print(worker.is_alive())

print("메인 스레드 종료")