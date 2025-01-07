import obd

connection = obd.OBD() # auto connect

### If above doesn't work, find the bluetooth port:
# ports = obd.scan_serial()      # return list of valid USB or RF ports
# print (ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
# connection = obd.OBD(ports[0]) # connect to the first port in the list

command = obd.commands.RPM # or obd.commands[1][12] mode 1, PID 12 (RPM)

response = connection.query(command)

print (response)