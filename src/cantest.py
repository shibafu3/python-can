import time
import can

bus = can.interface.Bus(channel = 'can0', bustype='socketcan_native', bitrate=500000, canfilters=None)

buffered_reader = can.BufferedReader()

class CallBackFunction(can.Listener):
  def on_message_received(self, msg):
    print(msg.data)

call_back_function = CallBackFunction()
can.Notifier(bus, [call_back_function, ])

data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

try:
  while True:
    msg = can.Message(arbitration_id=0x1, dlc=8, data=data)
    bus.send(msg)
    time.sleep(1)

except KeyboardInterrupt:
  print('exit')
  bus.shutdown()
