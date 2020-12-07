import lewansoul_lx16a
import serial
from pip._vendor.msgpack.fallback import xrange


class MoxelDriver:

    def __init__(self, name, workQueue, queueLock):
        self.workQueue = workQueue
        self.queueLock = queueLock
        self.name = name

        self.SERIAL_PORT = '/dev/cu.usbserial-1430'
        self.START_ID = 7
        self.END_ID = 12
        self.servos = []

        # careful the following assumes contiguous IDs
        self.num_servos = self.END_ID - self.START_ID + 1

        self.mi_range = xrange(self.START_ID, self.END_ID + 1)

        self.controller = lewansoul_lx16a.ServoController(
            serial.Serial(self.SERIAL_PORT, 115200, timeout=1),
        )

        self.create_controller_set()

    def __str__(self):
        return ("My current state is...")

    def create_controller_set(self):
        print("creating_controller_set")
        for j in self.mi_range:
            print("int: %i", j)
            self.servos.append(self.controller.servo(j))

    def drive_servos(self, q, ql):
        while True:
            try:
                # print("moxels - try lock")
                self.queueLock.acquire()
                # print("moxels - got lock")
                if not self.workQueue.empty():
                    # print("moxels - GET ITEM")

                    artnet_item = self.workQueue.get()

                    self.queueLock.release()

                    moxel_cmd = []
                    for i in range(self.num_servos):
                        moxel_cmd.append(artnet_item.data[i])

                    print("processed artnet packet created cmd: ", moxel_cmd)

                    for i in range(self.num_servos):
                        self.servos[i].move_prepare((moxel_cmd[i] * 4) % 1024)
                        self.controller.move_start()
                else:
                    # print("moxels - NO ITEM")

                    self.queueLock.release()


            except KeyboardInterrupt:
                print ("error in Moxel EXCEPTION")