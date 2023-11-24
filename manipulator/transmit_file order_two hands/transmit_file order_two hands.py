import time
import serial
import threading

# 从文本文件中读取指令
def read_commands_from_file(file_path):
    commands = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                command = line.strip()
                commands.append(command)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    return commands

# 发送数据的线程函数
def send_data(ser, port_name, commands):
    for command in commands:
        data = command
        print(f"发送数据至 {port_name}: {data}")
        write_len = ser.write(data.encode('utf-8'))
        time.sleep(0.5)

if __name__ == '__main__':
    commands1 = read_commands_from_file('/home/pi/Desktop/leftCmd.txt')
    commands2 = read_commands_from_file('/home/pi/Desktop/rightCmd.txt')

    if not commands1 or not commands2:
        print("未找到任何指令")
    else:
        port_num1 = '/dev/ttyUSB0'
        port_num2 = '/dev/ttyUSB1'

        ser1 = serial.Serial(port=port_num1, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=0.5)
        ser2 = serial.Serial(port=port_num2, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=0.5)

        if not ser1.isOpen() or not ser2.isOpen():
            print("打开串口失败")
        else:
            print("成功打开串口：%s" % ser1.name)
            print("成功打开串口：%s" % ser2.name)

            # 启动两个线程，分别发送数据
            thread1 = threading.Thread(target=send_data, args=(ser1, port_num1, commands1))
            thread2 = threading.Thread(target=send_data, args=(ser2, port_num2, commands2))

            thread1.start()
            thread2.start()

            # 等待两个线程完成
            thread1.join()
            thread2.join()

            ser1.close()
            ser2.close()

            print("程序退出。")
