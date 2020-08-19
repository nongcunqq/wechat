from concurrent.futures import ProcessPoolExecutor
import  time
def task(name,age):
    print("name",name)
    print('age',age)
    time.sleep(1)

if __name__ == "__main__":
    start = time.time()
    ex = ProcessPoolExecutor(2) # 写入需要开的进程程数，适当即可，开多了，销毁进程也消耗资源

    for m,n in zip(range(50),range(50)):
        ex.submit(task,"safly%d"%m, n) #多参数传入
    ex.shutdown(wait=True)

    print("main")
    end = time.time()
    print(end - start)
