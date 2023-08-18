import math
import struct

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtNetwork import QUdpSocket


class UdpReceiver(QObject):
    dataProcessed = Signal()

    def __init__(self, results=None):
        super().__init__()

        self.udpSocket = QUdpSocket(self)
        self.port = 9000
        self.byteData = bytes(1)
        self.results = results if results is not None else []
        self.grouped_data = {}

        test = self.udpSocket.bind(self.port)  # Bind to the address and port you want to listen on

        self.currentBuffer = {}
        self.previousBuffer = {}
        self.currentCircleNo = None

        if test:
            print("bind success")
        self.udpSocket.readyRead.connect(self.handleReadyRead)
        # udp itself won't exceed RAM, THE MAX size of UDP is 65607 bytes, consider fragmentation
        # Consider using a larger buffer for the UDP socket if you're experiencing packet loss

    @Slot()
    def handleReadyRead(self):
        while self.udpSocket.hasPendingDatagrams():
            # the readDatagram method return  a tuple containning 3 values
            data, _, _ = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            self.parse_data(data)

    def parse_data(self, data):
        try:
            frame_header = struct.unpack_from('>I', data, 0)[0]
            # Read frame length
            frame_length = struct.unpack_from('>I',data, 4)[0]
            # Read command
            command = struct.unpack_from('>I', data, 8)[0]
            # Read sequence
            sequence = struct.unpack_from('>I', data, 12)[0]
            # Read status
            status_offset = 16
            status = data[status_offset:status_offset+130]  # Assuming status is already 130 bytes
            # Read data
            data_offset = status_offset + 130
            frame_data = data[data_offset:data_offset+1300]  # Assuming data is already 1300 bytes
            # Read crc16
            crc16_offset = data_offset + 1300
            crc16 = struct.unpack_from('>H', data, crc16_offset)[0]
            self.results.append(frame_data)
            # with open('output.txt', 'w') as file:
            # self.grouped_data = {}

            # To ensure that all data with the same circleNumber have been stored

            for data in self.results:
                offset = 0

                while offset < len(data):
                    circleNumber, angular, first_return_dist, first_return_amp = struct.unpack_from('>2I3s2s', data,
                                                                                                    offset)
                    # print("circleNumber, in dataParse.py dist", circleNumber, first_return_dist)
                    act_angular = (angular / math.pow(2, 25) / 72) * 360
                    first_return_dist = int.from_bytes(first_return_dist, byteorder='big')
                    first_return_amp = int.from_bytes(first_return_amp, byteorder='big')
                    x = first_return_dist * math.cos(math.radians(act_angular)) * 0.0005
                    y = first_return_dist * math.sin(math.radians(act_angular)) * 0.0005
                    if self.currentCircleNo is None:
                        self.currentCircleNo = circleNumber

                    elif self.currentCircleNo != circleNumber:
                        self.previousBuffer = self.currentBuffer.copy()
                        self.currentBuffer.clear()
                        self.currentCircleNo = circleNumber

                    # Continue filling the currentBuffer
                    if circleNumber not in self.currentBuffer:
                        self.currentBuffer[circleNumber] = {"x": [], "y": [], "angular": [], "first_return_amp": []}
                    self.currentBuffer[circleNumber]["x"].append(x)
                    self.currentBuffer[circleNumber]["y"].append(y)
                    self.currentBuffer[circleNumber]["angular"].append(act_angular)
                    self.currentBuffer[circleNumber]["first_return_amp"].append(first_return_amp)

                    offset += struct.calcsize('>2I3s2s')

                    # The dataProcessed signal is emitted to notify other parts of the application that the data processing is complete.
                self.dataProcessed.emit()
                # self.write_grouped_data_to_file(grouped_data, 'output.txt')
                self.results.clear()

        except struct.error:
            print("Error unpacking data")

    def write_grouped_data_to_file(self, grouped_data, filename):
        with open(filename, 'a') as file:
            for circleNumber, data_points in grouped_data.items():
                file.write(f"Circle Number: {circleNumber}\n")
                file.write('-' * 60 + '\n')  # separator for clarity
                for point in data_points:
                    act_angular, first_return_dist, first_return_amp, x, y = point
                    file.write(
                        f"Angular: {act_angular}, First Return Dist: {first_return_dist}, First Return Amp: {first_return_amp}, x: {x}, y: {y}\n")
                file.write('\n')  # empty line for separation between different circleNumbers
            file.flush()

    def close_connection(self):
        self.udpSocket.close()