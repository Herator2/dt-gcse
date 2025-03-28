import bluetooth
import advertising
import ubinascii
from machine import Pin
import time

# Bluetooth Constants
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# BLE Flags
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# Custom motor control service
_SERVICE_UUID = bluetooth.UUID(0xFFE0)

# Motor control characteristic
_TEMP_CHAR = (
    bluetooth.UUID(0xFFE1),
    _FLAG_WRITE,
)

# The motor service used by BLE
_MOTOR_SERVICE = (
    _SERVICE_UUID,
    (_TEMP_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)


# Flash the LED?
flash = True

# Blink the LED?
blink = False

# Main car class
class car:
    def __init__(self, ble, name=""):
        # Setup BLE
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_MOTOR_SERVICE,))
        # Set no connections
        self._connections = set()
        # Create name if passed name was blank
        if len(name) == 0:
            name = 'DT Car %s' % ubinascii.hexlify(self._ble.config('mac')[1],':').decode().upper()
        # Create BLE payload
        self._payload = advertising.advertising_payload(
            name=name, services=[]
        )
        # Start BLE advertisement
        self._advertise()
    
    # Handle events
    def _irq(self, event, data):
        # Track connections so we can send notifications
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("CONNECTED -> LISTENING")
            led = Pin('LED', Pin.OUT)
            led.on()
            global flash
            flash = False
        # On a disconnect -> Begin advertisement again
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            print("DISCONNECTED -> ADVERTISING")
            led = Pin('LED', Pin.OUT)
            led.off()
            self._advertise()
        # On data write
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            # Check if the write was to our motor control characteristic.
            if attr_handle == self._handle:
                # Read the new data written by the central.
                value = self._ble.gatts_read(self._handle)
                print("Received data on motor control characteristic:", value)
                # Call your custom function with the new data.
                self.on_motor_control_write(value)
    
    def on_motor_control_write(self, data):
        print("MOTOR CONTROL WRITE")
        print("DATA", data)
        #data = int(str(data.decode("utf-8")).strip())
        
        led = Pin("LED", Pin.OUT)
        
        global blink
        blink = True
        
        # Instructions
        
        # LED control
        if data == b'\x00': led.off()
        elif data == b'\x01': led.on()
        
        # GPIO 0
        elif data == b'\x02': Pin(0, Pin.OUT).off()
        elif data == b'\x03': Pin(0, Pin.OUT).on()
        # GPIO 1
        elif data == b'\x04': Pin(1, Pin.OUT).off()
        elif data == b'\x05': Pin(1, Pin.OUT).on()
        
        # GPIO 2
        elif data == b'\x06': Pin(2, Pin.OUT).off()
        elif data == b'\x07': Pin(2, Pin.OUT).on()
        # GPIO 3
        elif data == b'\x08': Pin(3, Pin.OUT).off()
        elif data == b'\x09': Pin(3, Pin.OUT).on()
        
        # Forward
        elif data == b'\x0a':
            Pin(1, Pin.OUT).off()
            Pin(3, Pin.OUT).off()
            Pin(0, Pin.OUT).on()
            Pin(2, Pin.OUT).on()
            print("READ FORWARD COMMAND")
        
        # Backward
        elif data == b'\x0d':
            Pin(0, Pin.OUT).off()
            Pin(2, Pin.OUT).off()
            Pin(1, Pin.OUT).on()
            Pin(3, Pin.OUT).on()
            print("READ BACKWARD COMMAND")
        
        # Turn one way
        elif data == b'\x0b':
            Pin(0, Pin.OUT).on()
            Pin(2, Pin.OUT).off()
            Pin(1, Pin.OUT).off()
            Pin(3, Pin.OUT).on()
            print("READ TURN(1) COMMAND")
        
        # Turn other way
        elif data == b'\x0c':
            Pin(0, Pin.OUT).off()
            Pin(2, Pin.OUT).on()
            Pin(1, Pin.OUT).on()
            Pin(3, Pin.OUT).off()
            print("READ TURN(2) COMMAND")
            
        # Turn other way
        elif data == b'\x0e':
            Pin(0, Pin.OUT).off()
            Pin(2, Pin.OUT).off()
            Pin(1, Pin.OUT).off()
            Pin(3, Pin.OUT).off()
            print("READ STOP COMMAND")
    
    # Start advertisement
    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        global flash
        flash = True

if __name__ == "__main__":
    ble = bluetooth.BLE()
    x = car(ble)
    while True:
        if flash:
            Pin("LED", Pin.OUT).toggle()
            time.sleep_ms(500)
        elif blink:
            blink = False
            Pin("LED", Pin.OUT).off()
            time.sleep_ms(50)
        else:
            Pin("LED", Pin.OUT).on()
            
            
