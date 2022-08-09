from flask import Flask
import time
from threading import Thread

app = Flask(__name__)

@app.route('/')
def page():
    return "Hello"

def run():
    app.run(debug= True)

def show():
    while True:
        with open('hello.txt', 'a') as f:
            f.write('Hello')
        time.sleep(2)

if __name__ == '__main__':
    #t1 = Thread(target= run)
    t2 = Thread(target= show)
    t2.start()
    run()
    #t1.start()
    
    #t1.join()
    t2.join()

    print("END")
