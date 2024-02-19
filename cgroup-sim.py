import time


def fake_memory():
    memory_list = []
    while True:
        memory_list.append(bytearray(1 * 1024 * 1024))
        time.sleep(0.3)
        print(len(memory_list))


if __name__ == "__main__":
    input("wait")
    fake_memory()
