import time
import serial.tools.list_ports
from datetime import datetime, timedelta

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

if __name__ == '__main__':
    commands = read_commands_from_file('/home/pi/Desktop/leftCmd.txt')

    if not commands:
        print("未找到任何指令")
    else:
        port_num = '/dev/ttyUSB0'  # 固定使用 /dev/ttyUSB0 串口

        ser = serial.Serial(port=port_num, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=0.5)

        if not ser.isOpen():
            print("打开串口失败")
        else:
            print("成功打开串口：%s" % ser.name)

            # 等待30秒钟
            time.sleep(0)

            for command in commands:
                data = command
                print("发送数据：%s" % data)

                # 在此处发送指令给串口设备
                # 例如：ser.write(new_command.encode('utf-8'))

                write_len = ser.write(data.encode('utf-8'))
                time.sleep(0.5)  # 发送下一条指令之前的延迟

            ser.close()
            if ser.isOpen():
                print("串口仍然打开")
            else:
                print("串口已关闭")
