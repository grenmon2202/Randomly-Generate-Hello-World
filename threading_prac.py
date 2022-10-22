import time
import threading

def process(str):
    for i in range(10):
        time.sleep(0.2)

        print(str)

def main():
    process('h')


    t1 = threading.Thread(target=process, args=('t1', ))
    t2 = threading.Thread(target=process, args=('t2', ))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    print('here')

if __name__ == '__main__':
    main()