from multiprocessing import Process, Pipe
import time

def f(conn):
    print(conn.recv()) # prints "[31, None, 'send from parent_conn']"
    for i in range(5):
        conn.send([42, None, 'send from child_conn'])
        time.sleep(1)
        # conn.send([45, None, 'send from child_conn'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    parent_conn.send([31, None, 'send from parent_conn'])
    p = Process(target=f, args=(child_conn,))
    p.start()
    # for i in range(15):
    while True:
        test = parent_conn.poll(2)
        print(test)
        # time.sleep(0.5)
        # if :
            # print(parent_conn.readable)
        if test:
            print(parent_conn.recv())   # prints "[42, None, 'send from child_conn']"
        
    p.join()
