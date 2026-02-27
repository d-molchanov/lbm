import sys
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStyleFactory
)
from stepper_motor_controller_widget import StepperMotorControllerWidget
from mcu_communication import MCUCommunication
from stm32_communication import STM32Communication
# from port_listener import PortListener
# from port_listener import MCUCommunication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    main_window = QMainWindow()
    main_window.resize(900, 330)
    main_widget = StepperMotorControllerWidget()
    main_window.setCentralWidget(main_widget)

    # communication = MCUCommunication()
    communication = STM32Communication()
    # main_widget.com_port_chosen.connect(communication.set_port_name)
    # main_widget.baudrate_chosen.connect(communication.set_baudrate)
    main_widget.connection_requested.connect(
        communication.start_communication
    )
    main_widget.disconnection_requested.connect(
        communication.close_connection
    )
    main_widget.pushButtonCheckState.clicked.connect(
        communication.check_state
    )
    main_widget.pushButtonStopMotor.clicked.connect(
        communication.stop_motor
    )
    main_widget.pushButtonSetZero.clicked.connect(
        communication.set_zero
    )
    main_widget.movement_request_created.connect(
        communication.start_movement
    )

    main_widget.pushButtonPoweroffMotor.clicked.connect(
        communication.poweroff_motor
    )

    communication.logs_updated.connect(main_widget.update_logs)
    communication.connection_is_active.connect(
        main_widget.connection_is_active
    )
    
    communication_thread = QThread()
    communication.moveToThread(communication_thread)
    communication_thread.start()
    main_window.show()
    sys.exit(app.exec())