from time import sleep
import multiprocessing as mp
from multiprocessing.connection import PipeConnection
class ab():
    def __init__(self):
        pass

    def run_a(self, conn: PipeConnection=None):
        # print(mp.current_process())
        # while conn.poll(2):
        while True:
            print(conn.recv())
        # while True:
        #     sleep(0.001)

# def start(conn):
#     p = mp.Process(name="asdf", target=run_a, args=(conn, ), daemon=True)
#     p.start()
#     p.join()

# if __name__ == "__main__":
#     import multiprocessing as mp
#     pipeParent, pipeChild = mp.Pipe()
#     pipeParent.send("ㅎㅇ")
#     start(pipeChild)
#     start(pipeChild)
#     start(pipeChild)
