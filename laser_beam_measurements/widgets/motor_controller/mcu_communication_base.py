
from PySide6.QtCore import QObject, Signal, QDateTime, QThread


class MCUCommunicationBase(QObject): 
    connection_is_active = Signal(bool)
    logs_updated = Signal(str)
    answer_sent = Signal(str)

    def __init__(self, parent = None, **kwargs) -> None:
        super().__init__(parent)
        print('Hello from mcu_communication_base!')
        self._thread: QThread | None = kwargs.get('thread', None)
        create_thread = kwargs.get('create_thread', False)
        if self._thread is None and create_thread:
            self._thread = QThread()
            self.moveToTread(self._thread)
            if not self._thread.isRunning():
                self._thread.start()
                print('Thread is started!')


    def _format_log_message(self, msg: str, level: str) -> str:
        timestamp = QDateTime.currentDateTime().toString(
            'yyyy-MM-dd HH:mm:ss.zzz'
        )
        return f'{timestamp} {level}: {msg}'
    
    def update_logs(self, msg: str, level: str) -> None:
        log_message = self._format_log_message(msg, level)
        self.logs_updated.emit(log_message)

    def start_communication(self) -> None:
        raise NotImplementedError()
    
    def stop_communication(self) -> None:
        raise NotImplementedError()
    
    def read_data(self) -> bytes:
        raise NotImplementedError()
    
    def write_data(self, data: bytes) -> None:
        raise NotImplementedError()
    
    def create_request(self, data: dict) -> bytes:
        raise NotImplementedError()
    

def main() -> None:
    communication = MCUCommunicationBase()
    communication.start_communication()

if __name__ == '__main__':
    main()