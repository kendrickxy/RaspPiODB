# OBD CONNECTION:



######### Connect using the python code. Though, it's better to know the device's port before doing anything else.
	
import obd

connection = obd.OBD() # auto connect

# OR

connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0. We won't use it, but it' s an option.

# OR

ports = obd.scan_serial()      # return list of valid USB or RF ports
print (ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
connection = obd.OBD(ports[0]) # connect to the first port in the list




######### Command lookup. It allows you can call up  a function. 

import obd

c = obd.commands.RPM

# OR

c = obd.commands['RPM']

# OR

c = obd.commands[1][12] # mode 1, PID 12 (RPM) 2 bits returned formula is: (256 * (bit A) + (bit B)) / 4

# With our torque goal, we can try out the command obd.commands[1][99] # mode 1, PID 99	returns 2 bits. Engine reference torque: 0 to 65,535 N⋅m
# Torque formula (256*(bit A)+ (bit B))

print(c)




######### CHeck if a PID command exists:

import obd
pidval = obd.commands.has_pid(1, 12) # True
# Let's specially check for our torque values.

######### Create our own OBD command!

from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

# Define the decoding function
def decode_torque(messages):
    d = messages[0].data[2:]
    A = d[0]  # first byte
    B = d[1]  # second byte
    value = 256 * A + B
    return value  # convert the raw value to Newton-meters

c = OBDCommand(
    "Torque",                   # name
    "Engine reference torque",  # description
    b"0163",                    # command
    2,                          # number of return bytes to expect
    decode_torque,                        # decoding function
    # ECU.ENGINE,                 # (optional) ECU filter
)

# By default, custom commands will be treated as "unsupported by the vehicle". There are two ways to handle this:

o = obd.OBD()

# use the `force` parameter when querying
o.query(c, force=True)

# OR

# add your command to the set of supported commands, which we'll most likely use.
o.supported_commands.add(c)
o.query(c)




######### Handeling response

import obd

connection = obd.OBD()

response = connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_2)

# in the test results, lookup the result for MISFIRE_COUNT
result = response.value.MISFIRE_COUNT

# check that we got data for this test
if not result.is_null():
    print(result.value) # will be a Pint value
else:
    print("Misfire count wasn't reported")

response.value.MISFIRE_MONITORING.available