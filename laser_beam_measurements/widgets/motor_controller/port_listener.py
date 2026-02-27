import sys
import time

from serial import Serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, qDebug, QTimer, QObject, Slot


class Worker(QObject):
    @Slot()
    def on_timeout(self):
        qDebug(f"on_timeout() called from thread: "
               f"{self.thread()}")

    @Slot()
    def do_work(self):
        qDebug(f"Worker thread: {self.thread()}")
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(1000)


class PortListener(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.serial_port = None

    def set_port(self, port) -> None:
        self.serial_port = port

    @Slot()
    def on_timeout(self):
        if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline()
                print(f'Message received: `{data.decode("utf-8")}`')
                print(f'Message received: `{list(data)}`')
                # self.stop_listen_port()

    @Slot()
    def start_listen_port(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(500)

    @Slot()
    def stop_listen_port(self) -> None:
        self.timer.stop()


class MCUCommunication(QObject):

    @Slot()
    def check_port(self):
        if self.serial_port.in_waiting > 0:
            data = self.serial_port.readline()
            print(f'Message received: `{data.decode("utf-8")}')
            self.timer.stop()

    def check_available_ports(self) -> list:
        return [port.device for port in comports()]

    def connect_to_port(self, port, baud_rate) -> Serial:
        try:
            print(f'Initializing port `{port}` ...')
            serial_port = Serial(port, baud_rate, timeout=0.5)
            serial_port.flushInput()
            serial_port.flushOutput()
            self.active_port = port
            self.serial_port = serial_port
            print(f'Connection to port `{port}` has been established')
            return serial_port
        except SerialException as e:
            print(f'Port `{port}` could not be opened. Check connection')

    def close_connection(self) -> None:
        if self.active_port:
            try:
                self.serial_port.close()
                print(f'Port `{self.active_port}` has been closed')
                self.active_port = None
                self.serial_port = None
            except SerialException as e:
                print(f'Port `{self.active_port}` could not be closed. Check connection')

    @Slot()
    def listen_port(self) -> None:
        while self.listen:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline()
                print(f'Message received: `{data.decode("utf-8")}')

    def get_serial_port(self) -> Serial:
        return self.serial_port

    def write_to_port(self, data) -> None:
        if self.serial_port:
            self.serial_port.write(data)

    def check_state(self)  -> None:
        if self.active_port:
            try:
                self.serial_port.write('!QP%'.encode('utf-8'))
                print('Message was sent')
                # time.sleep(2)
                print(self.serial_port.in_waiting)
                
                # while True:
                #     if self.serial_port.in_waiting > 0:
                #         data = self.serial_port.readline()
                #         # data = self.serial_port.read()
                #         print(f'Message received: `{data.decode("utf-8")}`')
                #         break
            except SerialException as e:
                print(f'Something wrong with {self.active_port}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # worker = Worker()
    # worker_thread = QThread()
    # worker.moveToThread(worker_thread)
    # worker_thread.started.connect(worker.do_work)
    # worker_thread.start()

    # worker2 = Worker()
    # worker_thread2 = QThread()
    # worker2.moveToThread(worker_thread2)
    # worker_thread2.started.connect(worker2.do_work)
    # worker_thread2.start()

    print('This is main method!')
    communication = MCUCommunication()
    ports = communication.check_available_ports()
    print(f'{ports = }')
    communication.connect_to_port('COM9', 9600)
    communication.check_state()
    listener = PortListener()
    listener.set_port(communication.get_serial_port())
    listener_thread = QThread()
    listener.moveToThread(listener_thread)
    listener_thread.started.connect(listener.start_listen_port)
    listener_thread.start()
    time.sleep(2)
    communication.write_to_port(bytes([33,77,15,48,48,49,48,49,48,14,15,0,134,8,66,37]))
    # time.sleep(2)
    # communication.check_state()
    # time.sleep(2)
    # communication.check_state()
    # communication.close_connection()

    qDebug(f"Main thread: {listener_thread.thread()}")
    app.exec()