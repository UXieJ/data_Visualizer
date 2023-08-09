from PySide6.QtCore import QThread, Signal, QTimer


class parseNetThread(QThread):
    fin = Signal(object)

    def __init__(self, uParser):
        super().__init__()
        self.parser = uParser

    def run(self):
        pointCloud = self.parser.parse_data
        self.fin.emit(pointCloud)




