from datetime import datetime

from typing import Optional
from serial import Serial
from serial.tools.list_ports import comports

from PySide6.QtCore import Signal, Slot, QTime, QDateTime, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QIcon
from .ui_stepper_motor_controller_widget import Ui_Form
from laser_beam_measurements.widgets.motor_controller.stm32_communication import STM32Communication

from laser_beam_measurements.icons import Icon

class Icons:
    check_state = Icon('motor_check_state.svg')
    clear_logs = Icon('motor_clear_logs.svg')
    connect = Icon('motor_connect.svg')
    disconnect = Icon('motor_disconnect.svg')
    measure = Icon('motor_measure.svg')
    poweroff = Icon('motor_poweroff.svg')
    refresh = Icon('motor_refresh.svg')
    send = Icon('motor_send.svg')
    set_zero = Icon('motor_set_zero.svg')
    start = Icon('motor_start.svg')
    stop = Icon('motor_stop.svg')

# class StepperMotorControllerWidget(QWidget):
class StepperMotorControllerWidget(QWidget, Ui_Form):
    logs_updated = Signal(str)
    connection_established = Signal(bool)
    com_port_chosen = Signal(str)
    baudrate_chosen = Signal(int)
    connection_requested = Signal(str, int)
    disconnection_requested = Signal()
    movement_request_created = Signal(dict)
    measuring_requested = Signal()

    def __init__(self, parent=None) -> None:
        super(StepperMotorControllerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Motor')
        self._icons = Icons()
        self._set_icons()
        # self.setupUi(self)
        self.serial_port = None
        self.port_name = None
        self.baudrate = 0
        self._communication = STM32Communication()
        # self.connect_icon = QIcon('./icons/connect.svg')
        # self.disconnect_icon = QIcon('./icons/disconnect.svg')
        self.ui.pushButtonDisconnect.setVisible(False)
        self.active_connection = False
        comports = self.check_available_comports()
        self.ui.comboBoxCOMPorts.addItems(comports)
        self.ui.comboBoxBaudRate.addItems(
            [
                '9600',
                '19200',
                '38400',
                '57600',
                '115200'
            ]
        )
        self.ui.pushButtonConnect.clicked.connect(self.connect_to_port)
        self.ui.pushButtonDisconnect.clicked.connect(self.disconnect_from_port)
        self.logs_updated.connect(self.update_logs)
        # self.connection_established.connect(self.unable_button)
        self.ui.pushButtonRefresh.clicked.connect(self.update_ports_list)
        self.ui.pushButtonClearLogs.clicked.connect(self.ui.textEditLogs.clear)
        self.ui.pushButtonMeasure.clicked.connect(self.on_measuring_requested)
        self.ui.comboBoxDirection.addItems(
            [
                'Clockwise', 
                'Counterclockwise'
            ]
        )
        step_values = ['1:1', '1:2', '1:4', '1:8', '1:16']
        self.ui.comboBoxStep.addItems(step_values)
        self.ui.comboBoxStep.setCurrentIndex(len(step_values)-1)
        self.ui.spinBoxVelocity.setMinimum(10)
        self.ui.pushButtonStartMotor.clicked.connect(self.create_request)
        units_values = ['um', 'mm', 'cm']
        self.ui.comboBoxMovementUnits.addItems(units_values)
        self.ui.comboBoxMovementUnits.setCurrentIndex(1)
        velocity_values = ['um/s', 'mm/s', 'cm/s', 'm/s']
        self.ui.comboBoxVelocityUnits.addItems(velocity_values)
        self.ui.comboBoxStep.currentTextChanged.connect(
            self.onStepDividerChanged
        )
        self.ui.textEditProgram.setPlainText('10 mm +\n-20 mm +\n5 mm -\n5 mm +')
        # self.logs_updated.emit('hello!')
        self._programs = []
        self._program_index = 0
        self._m2 = []
        self.ui.pushButtonMeasure.setEnabled(True)
        self._timer = QTimer()
        self._timer.setInterval(500)
        self._timer.timeout.connect(self.slot_measure_beam)
        self._measured_amount = 0
        self._measured_amount_max = 10
        self._measured_pars = {
            'global_x': [],
            'global_y': [],
            'local_x': [],
            'local_y': [],
            'level135_x': [],
            'level135_y': [],
            '4sigma_x': [],
            '4sigma_y': [],
            'gauss_x': [],
            'gauss_y': [],
            'power86': []
        }

    @property
    def stm32_communication(self) -> Optional[STM32Communication]:
        return self._communication
    
    @stm32_communication.setter
    def stm32_communication(self, communication: STM32Communication) -> None:
        self._communication = communication
        self._set_signals()
        print(f'Communication from stepper motor controller widget was set.')


    def _set_icons(self):
        self.ui.pushButtonCheckState.setIcon(self._icons.check_state)
        self.ui.pushButtonClearLogs.setIcon(self._icons.clear_logs)
        self.ui.pushButtonConnect.setIcon(self._icons.connect)
        self.ui.pushButtonMeasure.setIcon(self._icons.measure)
        self.ui.pushButtonPoweroffMotor.setIcon(self._icons.poweroff)
        self.ui.pushButtonRefresh.setIcon(self._icons.refresh)
        self.ui.pushButtonSend.setIcon(self._icons.send)
        self.ui.pushButtonSetZero.setIcon(self._icons.set_zero)
        self.ui.pushButtonStartMotor.setIcon(self._icons.start)
        self.ui.pushButtonStopMotor.setIcon(self._icons.stop)


    def _set_signals(self):
        self.connection_requested.connect(
            self._communication.start_communication
        )
        self.disconnection_requested.connect(
            self._communication.close_connection
        )
        self.ui.pushButtonCheckState.clicked.connect(
            self._communication.check_state
        )
        self.ui.pushButtonStopMotor.clicked.connect(
            self._communication.stop_motor
        )
        self.ui.pushButtonSetZero.clicked.connect(
            self._communication.set_zero
        )
        self.movement_request_created.connect(
            self._communication.start_movement
        )

        self.ui.pushButtonPoweroffMotor.clicked.connect(
            self._communication.poweroff_motor
        )

        self._communication.logs_updated.connect(self.update_logs)
        self._communication.connection_is_active.connect(
            self.connection_is_active
        )
        self._communication.answer_sent.connect(
            self.slot_move_to_next_point
        )
        self.measuring_requested.connect(self._communication.slot_measure_beams)
        print('Signals were set.')

    @Slot()
    def on_measuring_requested(self):
        self.measuring_requested.emit()
        self._communication.adjust_exposure.emit()
        # self._m2.append(self._communication._current_data)
        self._measured_amount = 0
        self._timer.start()
        print('')
        print(*self._m2, sep='\n')

    @Slot()
    def slot_measure_beam(self) -> None:
        if self._measured_amount > self._measured_amount_max:
            self._timer.stop()
            self._measured_amount = 0
            result = {}
            for key, value in self._measured_pars.items():
                result[key] = self._calculate_average(value)
            print(
                '\t'.join(
                    [
                        f'{key}: {value:.2f}' for key, value in result.items()
                    ]
                )
            )
            result['number'] = self._program_index
            # result['coordinate'] = self._programs[self._program_index]['coordinate']
            self._m2.append(result)
            print(self._m2)

            return
        bp = self._parse_beam_parameters(self._communication._current_data)
        self._measured_pars['global_x'].append(bp['global_x'])
        self._measured_pars['global_y'].append(bp['global_y'])
        self._measured_pars['local_x'].append(bp['local_x'])
        self._measured_pars['local_y'].append(bp['local_y'])
        self._measured_pars['level135_x'].append(bp['level135_x'])
        self._measured_pars['level135_y'].append(bp['level135_y'])
        self._measured_pars['4sigma_x'].append(bp['4sigma_x'])
        self._measured_pars['4sigma_y'].append(bp['4sigma_y'])
        self._measured_pars['gauss_x'].append(bp['gauss_x'])
        self._measured_pars['gauss_y'].append(bp['gauss_y'])
        self._measured_pars['power86'].append(bp['power86'])

        self._measured_amount += 1

    def _calculate_average(self, data: list) -> Optional[float]:
        filtered_data = [d for d in data if d]
        if filtered_data:
            return sum(filtered_data) / len(filtered_data)
        return None
    
    def _parse_beam_parameters(self, parameters: dict) -> Optional[dict]:
        if not parameters:
            return
        result = {
            'global_x': None,
            'global_y': None,
            'local_x': None,
            'local_y': None,
            'level135_x': None,
            'level135_y': None,
            '4sigma_x': None,
            '4sigma_y': None,
            'gauss_x': None,
            'gauss_y': None,
            'power86': None
        }
        pos = parameters.get('Beam Position And Orientation', None)
        if pos:
            global_pos = pos.get('Global position', None)
            # print(f'{global_pos = }')
            if global_pos and isinstance(global_pos, (list, tuple)) and len(global_pos) > 1:
                result['global_x'] = global_pos[0]
                result['global_y'] = global_pos[1]
            local_pos = pos.get('Local position', None)
            # print(f'{local_pos = }')
            if local_pos and isinstance(local_pos, (list, tuple)) and len(local_pos) > 1:
                result['local_x'] = local_pos[0]
                result['local_y'] = local_pos[1]
        beam_width = parameters.get('Beam Width', None)
        # print(f'{beam_width = }')
        if beam_width:
            level_135 = beam_width.get('13.5% level', None)
            if level_135 and isinstance(level_135, (list, tuple)) and len(level_135) > 1:
                result['level135_x'] = level_135[0]
                result['level135_y'] = level_135[1]
            _4sigma = beam_width.get('4 Sigma', None)
            if _4sigma and isinstance(_4sigma, (list, tuple)) and len(_4sigma) > 1:
                result['4sigma_x'] = _4sigma[0]
                result['4sigma_y'] = _4sigma[1]
            gauss = beam_width.get('Gauss approximation', None)
            if gauss and isinstance(gauss, (list, tuple)) and len(gauss) > 1:
                result['gauss_x'] = gauss[0]
                result['gauss_y'] = gauss[1]
            result['power86'] = beam_width.get('86% Power', None)
        return result

    @Slot(str)
    def onStepDividerChanged(self, step_divider):
        if step_divider == '1:16':
            self.ui.spinBoxVelocity.setMinimum(10)
        else:
            self.ui.spinBoxVelocity.setMinimum(1)


    def create_request(self) -> dict:
        self.update_logs(f'{self.ui.tabWidget.currentIndex() = }')
        if self.ui.tabWidget.currentIndex() == 0:
            result = {
                'request_type': 'Movement',
                'step_type': self.ui.comboBoxStep.currentText(),
                'steps_amount': self.ui.spinBoxSteps.value(),
                'direction': self.ui.comboBoxDirection.currentText(),
                'velocity': self.ui.spinBoxVelocity.value()
            }
            self.movement_request_created.emit(result)
        elif self.ui.tabWidget.currentIndex() == 1:
            self.update_logs(
                f'Move to {self.ui.doubleSpinBoxMoveTo.value()}'
                f' {self.ui.comboBoxMovementUnits.currentText()}'
            )
            coordinate = self.ui.doubleSpinBoxMoveTo.value()
            if coordinate >= 0:
                direction = 'Clockwise'
            else:
                direction = 'Counterclockwise'
                coordinate = abs(coordinate)
            units = self.ui.comboBoxMovementUnits.currentText()
            factor_dict = {
                'um': 1.0,
                'mm': 1e3,
                'cm': 1e4
            }
            factor = factor_dict.get(units, None)
            if factor:
                scale = self.ui.doubleSpinBoxScale.value()
                steps_amount = round(coordinate * factor / scale)
            else:
                steps_amount = None
            result = {
                'request_type': 'Movement',
                'step_type': '1:16',
                'steps_amount': steps_amount,
                'direction': direction,
                'velocity': self.ui.spinBoxVelocity.value()
            }
            self.update_logs(f'{result = }')
            self.movement_request_created.emit(result)
        elif self.ui.tabWidget.currentIndex() == 2:
            self._programs = []
            # self.update_logs('Hello!')
            self._programs = self._parse_program(
                self.ui.textEditProgram.toPlainText()
            )
            self.update_logs(f'{self._programs = }')
            if self._programs:
                request = self._create_movement_request(self._programs[0])
                self.movement_request_created.emit(request)
                self._program_index = 1
            # for d in text_program:
            #     self._programs.append(d)
                # coordinate = float(d['coordinate'])
                # units = d['units']
                # command = d['command']
                # self.update_logs(
                #     f'Move to {coordinate}'
                #     f' {units}'
                # )
                # request = self._create_movement_request(d)
                # self.update_logs(f'{request = }')
                # self._programs.append(request)
                # self.movement_request_created.emit(request)
                # if command == '+':
                    # self.measuring_requested.emit()

    def _create_movement_request(self, parameters: dict) -> dict:
        coordinate = parameters['coordinate']
        units = parameters['units']
        if coordinate >= 0:
            direction = 'Clockwise'
        else:
            direction = 'Counterclockwise'
            coordinate = abs(coordinate)
        factor_dict = {
            'um': 1.0,
            'mm': 1e3,
            'cm': 1e4
        }
        factor = factor_dict.get(units, None)
        if factor:
            scale = self.ui.doubleSpinBoxScale.value()
            steps_amount = round(coordinate * factor / scale)
        else:
            steps_amount = None
        velocity = self.ui.spinBoxVelocity.value()
        result = {
            'request_type': 'Movement',
            'step_type': '1:16',
            'steps_amount': steps_amount,
            'direction': direction,
            'velocity': velocity
        }
        return result

    def _parse_program(self, program_text: str) -> list:
        result = []
        lines = program_text.split('\n')
        for line in lines:
            x, units, c = line.split()
            result.append(
                {
                    'coordinate': float(x),
                    'units': units,
                    'command': c})
        return result

    @Slot(str)
    def slot_move_to_next_point(self, answer):
        if self._program_index > (len(self._programs) - 1):
            self._program_index = 0
            # self._programs = []
            # return
        print(answer[-7:-1])
        request = self._create_movement_request(
            self._programs[self._program_index]
        )
        data = self._communication._current_data
        self._m2.append(
            {
                'coordinate': self._programs[self._program_index]['coordinate'],
                'data': data
            }
        )
        print(f'{data = }')
        self.measuring_requested.emit()
        self.movement_request_created.emit(request)
        self._program_index += 1 

    def check_available_comports(self) -> list:
        return [
            port.device for port in comports()
        ]

    @Slot()
    def update_ports_list(self):
        self.ui.comboBoxCOMPorts.clear()
        comports = self.check_available_comports()
        self.ui.comboBoxCOMPorts.addItems(comports)

    @Slot(str)
    def update_logs(self, msg: str) -> None:
        self.ui.textEditLogs.append(msg)

    @Slot(bool)
    def connection_is_active(self, value: bool) -> None:
    # def unable_button(self, value: bool) -> None:
        # self.pushButtonDisconnect.setEnabled(value)
        self.ui.pushButtonSend.setEnabled(value)
        self.ui.pushButtonStartMotor.setEnabled(value)
        self.ui.pushButtonStopMotor.setEnabled(value)
        self.ui.pushButtonSetZero.setEnabled(value)
        self.ui.pushButtonCheckState.setEnabled(value)
        self.ui.pushButtonPoweroffMotor.setEnabled(value)
        self.ui.pushButtonMeasure.setEnabled(value)
        # self.pushButtonConnect.setEnabled(not value)
        self.ui.comboBoxCOMPorts.setEnabled(not value)
        self.ui.comboBoxBaudRate.setEnabled(not value)
        self.ui.pushButtonRefresh.setEnabled(not value)
        print(f'Connection status from widget: {value}')
        # self.pushButtonRefresh.setDisabled(value)

    @Slot()
    def disconnect_from_port(self):
        # self.connection_established.emit(True)
        self.disconnection_requested.emit()
        # msg = f'Connection to {self.port_name} has been closed.' 
        # self.logs_updated.emit(
        #     self.format_message(msg, 'INFO')
        # )

    # def format_message(self, msg: str, level: str) -> str:
    #     timestamp = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss.zzz')
    #     return f'{timestamp} {level}: {msg}'

    @Slot()
    def connect_to_port(self):
        if not self.active_connection:
            self.port_name = self.ui.comboBoxCOMPorts.currentText()
            # self.com_port_chosen.emit(self.port_name)
            self.baudrate = int(self.ui.comboBoxBaudRate.currentText())
            # self.baudrate_chosen.emit(int(self.baudrate))
            self.connection_requested.emit(self.port_name, self.baudrate)
            # icon = QIcon('./icons/disconnect.svg')
            self.ui.pushButtonConnect.setIcon(self._icons.disconnect)
            self.active_connection = True
        else:
            self.active_connection = False
            self.ui.pushButtonConnect.setIcon(self._icons.connect)
            # self.pushButtonConnect.setIcon(self.connect_icon)
            self.disconnection_requested.emit()
        print(f'{self.active_connection = }')
        # self.connection_established.emit(False)
        # msg = f'Connection to {self.port_name} with baudrate {self.baudrate} has been established.' 
        # self.logs_updated.emit(
        #     self.format_message(msg, 'INFO')
        # )
        # self.logs_updated.emit(f'{self.port_name} - {self.baudrate}')
        # print(f'{self.comboBoxCOMPorts.currentText()} - {self.comboBoxBaudRate.currentText()}')
