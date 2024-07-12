import threading
import time
from panda_dr import panda_drAPI, initial_panda
import logging

loophun_thread = None

def startloopuber():
    # global loophun_thread
    # loophun_thread = threading.Thread(target=looppdt, daemon=True)
    # loophun_thread.start()
    looppdt()
    # loophun_thread.join()  # 等待子线程执行完成

def looppdt():
    print("looppdt thread started")
    try:
        temp = panda_drAPI()
        time.sleep(2)  # 假设这里是线程需要执行的任务
        # 继续进行其他操作
    except Exception as e:
        print(f"Exception in panda_drAPI(): {e}")
        # 可以在这里记录日志或者采取其他适当的错误处理措施

# 主程序入口
if __name__ == "__main__":
    startloopuber()