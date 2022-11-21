# 文件和异常
import time


def main():
    with open('/tmp/test.txt') as f:
        print(f.read())

    with open('/tmp/test.txt') as f:
        for line in f:
            print(line, end='')
            time.sleep(0.5)
    print()

    with open('/tmp/test.txt') as f:
        lines = f.readlines()
    for line in lines:
        print(line)

if __name__ == '__main__':
    main()
