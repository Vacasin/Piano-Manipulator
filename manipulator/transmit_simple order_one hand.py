import time
import serial.tools.list_ports
#import piano.note as note

#Time=1000    #运行时间
Num=1   #同时控制舵机数量
Figure_NUM=1    #控制舵机手指编号
#Angle=1500  #舵机运动角度

if __name__ == '__main__':
    # 读取串口列表
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备")
    else:
        print("可用的串口设备如下: ")
        print("%-10s %-30s %-10s" % ("num", "name", "number"))
        for i in range(len(ports_list)):
            comport = list(ports_list[i])
            comport_number, comport_name = comport[0], comport[1]
            print("%-10s %-30s %-10s" % (i, comport_name, comport_number))

        # 打开串口
        port_num = ports_list[0][0]
        print("默认选择串口: %s" % port_num)
        # 串口号: port_num, 波特率: 115200, 数据位: 8, 停止位: 1, 超时时间: 0.5秒
        ser = serial.Serial(port=port_num, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                            timeout=0.5)
        if not ser.isOpen():
            print("打开串口失败")
        else:
            print("打开串口成功, 串口号: %s" % ser.name)

            # 等待串口返回信息并输出
            t0 = time.time()
            while True:
                com_input = ser.read(10)
                t1 = time.time()
                while Num < 5:
                    # 获得手指编号和角度的函数
                    def get_figure():
                        figure_num_angle = "5-1-900-2-2000-3-2000-4-2000-5-2000"
                        data = "I001-%d-%s" % (500, figure_num_angle)  # 串口发送范例指令给机械手
                        print("发送数据: %s" % data)
                        write_len = ser.write(data.encode('utf-8'))
                        time.sleep(1) #每隔t秒发送一次
                    get_figure()

                break

                # 关闭串口
            ser.close()
            if ser.isOpen():
                print("串口未关闭")
            else:
                print("串口已关闭")
