#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import queue
import serial
import time
import threading
import lewansoul_lx16a
from pip._vendor.msgpack.fallback import xrange
from Artnet.ArtnetPacket import listen_and_redirect_artnet_packets
from MoxelDriver.MoxelDriver import MoxelDriver

SERIAL_PORT = '/dev/tty.usbserial-1430'


### ::START:: threading logic

# threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.LifoQueue(10)
exitFlag = 0

# def process_data(threadName, q):
#    while not exitFlag:
#       queueLock.acquire()
#       if not workQueue.empty():
#          data = q.get()
#          queueLock.release()
#          print ("%s processing %s" % (threadName, data))
#       else:
#          queueLock.release()
#          time.sleep(1)

workQueue = queue.Queue(2)
class myThread (threading.Thread):
   def __init__(self, threadID, name, q, fp):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
      self.fp = fp
   def run(self):
       print ("Starting " + self.name)
       self.fp(workQueue, queueLock)
       print ("Exiting " + self.name)
### ::END:: threading logic


def main():
    # print("hello world!")
    #
    # controller = lewansoul_lx16a.ServoController(
    #     serial.Serial(SERIAL_PORT, 115200, timeout=1),
    # )
    #
    # ### ::START:: Logic Create Servos
    #
    # START_ID = 7
    # END_ID = 12
    #
    # mi_range = xrange(START_ID, END_ID+1)
    # num_servos = END_ID - START_ID+1   # Assumes contiguous IDs!!
    #
    # servos = []
    #
    # for j in mi_range:
    #     print("int: %i", j)
    #     servos.append(controller.servo(j))
    ### ::END:: Logic Create Servos


    ### ::START:: artnet receive thread
    threadID = 1 ## ?? Why repeated from above

    # Create new threads



    #### The artnet receiver
    artnet_receiver_thread = myThread(threadID, "artnet", workQueue, listen_and_redirect_artnet_packets)

    miMoxels = MoxelDriver("miMoxels", workQueue, queueLock)
    #### The moxel driver
    moxel_driver_thread = myThread(threadID, "lx_16a", workQueue, miMoxels.drive_servos)
    threadID += 1

    artnet_receiver_thread.start()
    moxel_driver_thread.start()


    artnet_receiver_thread.join()
    moxel_driver_thread.join()

    ### ::START:: Control loop - convert this to a thread.

    # get the most recent fifo off the stack
    # for (z) in range(11):
    #     for i in range(num_servos):
    #         servos[i].move_prepare( (i*100 + z*100)%1000 )
    #         controller.move_start()
    #
    #     sleep(1)
    ### ::END::

if __name__ == "__main__":
    main()

print("Guru99")

print("Value in built variable name is:  ",__name__)