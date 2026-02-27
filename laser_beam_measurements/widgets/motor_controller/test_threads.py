import sys
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    worker = Worker()
    worker_thread = QThread()
    worker.moveToThread(worker_thread)
    worker_thread.started.connect(worker.do_work)
    worker_thread.start()

    qDebug(f"Main thread: {worker_thread.thread()}")
    app.exec()