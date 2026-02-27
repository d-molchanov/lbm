# Current MCU: STM32F103C8T6
from enum import StrEnum
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

from PySide6.QtCore import QObject, Signal, Slot, QTimer, QThread

from .mcu_communication_base import MCUCommunicationBase

class Level(StrEnum):
    INFO = 'INFO'
    ERROR = 'ERROR'

class StmRequest(StrEnum):
    CHECKSTATE = '!QP%'
    SETZERO = '!ZE%'
    STOP = '!ST%'
    # POWEROFF = bytes(
    #     [
    #         33,   # '!'
    #         77,   # 'M'
    #         255,  # 0b1111_1111
    #         48,   # '0'
    #         48,   # '0'
    #         48,   # '0'
    #         48,   # '0'
    #         48,   # '0'
    #         49,   # '1'
    #         0,    # prescaller for 1:16
    #         224,  # prescaller for 1:16
    #         0,    # velocity
    #         128,  # velocity
    #         15,   # crc
    #         154,  # crc
    #         37    # '%'
    #     ]
    # )

class STM32Communication(MCUCommunicationBase):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.serial_port = None
        self.port_name = None
        self.baudrate = None
        self.timer = None
    
    @Slot(str, int)
    def start_communication(
        self,
        port_name: str,
        baudrate: int
    ) -> None:        
        try:
            self.port_name = port_name
            self.baudrate = baudrate
            self.update_logs(
                (
                    f'Trying to connect to `{self.port_name}` '
                    f'with baudrate {self.baudrate}'
                ),
                Level.INFO
            )
            self.serial_port = Serial(
                self.port_name,
                self.baudrate,
                timeout=1
            )
            self.update_logs(
                (
                    f'Connection to `{self.port_name}` '
                    f'with baudrate {self.baudrate} '
                    'has been established'
                ),
                Level.INFO
            )
            self.connection_is_active.emit(True)
        except SerialException as e:
            self.update_logs(
                f'Port `{self.port_name} could not be opened: {e}`',
                Level.ERROR
            )
            return
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.read_data)
        self.timer.start()

    @Slot()
    def close_connection(self) -> None:
        if self.timer:
            self.timer.stop()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.connection_is_active.emit(False)
            self.update_logs(
                (
                    f'Connection to port `{self.port_name}` '
                    'has been closed'
                ),
                Level.INFO
            )

    def read_data(self) -> bytes | None:
        if not self.serial_port:
            return
        if not self.serial_port.is_open:
            return
        try:
            if self.serial_port.in_waiting <= 0:
                return 
            data = self.serial_port.readline()
            try:
                answer = data.decode('utf-8')
            except UnicodeError as e:
                self.update_logs(
                    f'Answer could not be decoded: {e}',
                    Level.ERROR
                )
                return
            self.update_logs(
                f'Answer has been received: `{answer}`',
                Level.INFO
            )
        except SerialException as e:
            self.update_logs(
                f'Reading error at `{self.port_name}`: {e}',
                Level.ERROR
            )

    @Slot(bytes)
    def write_data(self, data: bytes) -> None:
        if not self.serial_port:
            return
        if not self.serial_port.is_open:
            return 
        try:
            self.serial_port.write(data)
        except SerialException as e:
            self.update_logs(
                f'Writing error at `{self.port_name}`: {e}',
                Level.ERROR
            )

    def _create_third_byte(self, data: dict) -> int | None:
        step_divider = {
            '1:1': [0, 0, 0],
            '1:2': [1, 0, 0],
            '1:4': [0, 1, 0],
            '1:8': [1, 1, 0],
            '1:16': [1, 1, 1]
        }
        step_bits = step_divider.get(data['step_type'], None)
        print(f'{step_bits = }')
        if not step_bits:
            return
        result = 0
        for i, bit in enumerate(step_bits[::-1]):
            result += (bit << (i+4))
        result |= 0b1110
        
        directions = {
            'Clockwise': 0,
            'Counterclockwise': 1    
        }
        direction = directions.get(data['direction'], None)
        print(f'{direction = }')
        if direction is None:
            return
        result |= direction
        return result
    
    def _choose_prescaler(self, data: dict) -> list:
        prescaler = {
            '1:1': [0x0e, 0x0f], # 3599: f =  20 kHz
            '1:2': [0x07, 0x07], # 1799: f =  40 kHz
            '1:4': [0x03, 0x83], #  899: f =  80 kHz
            '1:8': [0x01, 0xc1], #  449: f = 160 kHz
            '1:16': [0x00, 0xe0] #  224: f = 320 kHz
        }
        return prescaler.get(data['step_type'], [0x0e, 0x0f])

    def _calculate_crc(self, request: list[int]) -> list[int] | None:
        crc_sum = 0
        result = [0, 0]
        for el in request:
            crc_sum += el
        crc_sum = crc_sum << 1
        result[-1] = crc_sum & 0xff
        crc_sum = crc_sum >> 7
        result[0] = crc_sum & 0xff
        return result
   
    def _create_request(self, data: dict) -> bytes | None:
        request = [
            33, # Start byte '!'
            77  # Byte for movement 'M'
        ]
        third_byte = self._create_third_byte(data)
        if not third_byte:
            return
        request.append(third_byte)
        steps_amount = data.get('steps_amount', 0)
        request += [ord(el) for el in f'{steps_amount:0>6}']
        request += self._choose_prescaler(data)
        velocity = data.get('velocity', 100)
        request.append((velocity >> 8) & 0xff)
        request.append(velocity & 0xff)
        request += self._calculate_crc(request[1:])
        request.append(37) # End byte '%'
        return request
    
    @Slot(dict)
    def start_movement(self, data: dict) -> None:
        request = self._create_request(data)
        print(f'{data = }')
        print(f'{request = }')
        self.update_logs(str(request), Level.INFO)
        if request:
            self.write_data(bytes(request))

    @Slot()
    def poweroff_motor(self) -> None:
        self.update_logs(
            'Request to STM32: `POWEROFF`', Level.INFO
        )
        request = bytes(
            [
                33,   # '!'
                77,   # 'M'
                255,  # 0b1111_1111
                48,   # '0'
                48,   # '0'
                48,   # '0'
                48,   # '0'
                48,   # '0'
                49,   # '1'
                0,    # prescaller for 1:16
                224,  # prescaller for 1:16
                0,    # velocity
                128,  # velocity
                15,   # crc
                154,  # crc
                37    # '%'
            ]
        )
        self.write_data(request)
    
    @Slot()
    def check_state(self) -> None:
        self.update_logs(
            f'Request to STM32: `{StmRequest.CHECKSTATE}`', Level.INFO
        )
        self.write_data(StmRequest.CHECKSTATE.encode('utf-8'))
    
    @Slot()
    def stop_motor(self) -> None:
        self.update_logs(
            f'Request to STM32: `{StmRequest.STOP}`', Level.INFO
        )        
        self.write_data(StmRequest.STOP.encode('utf-8'))
    
    @Slot()
    def set_zero(self) -> None:
        self.update_logs(
            f'Request to STM32: `{StmRequest.SETZERO}`', Level.INFO
        )
        self.write_data(StmRequest.SETZERO.encode('utf-8'))

def main() -> None:
    communication = STM32Communication()
    communication.start_communication('COM9', 9600)
    communication.check_state()
    print('Done!')

if __name__ == '__main__':
    main()