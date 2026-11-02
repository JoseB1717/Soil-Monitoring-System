import time
import schedule
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import serial
import smtplib
from email.message import EmailMessage

MCP = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

from_email_addr ="jolix18183@gmail.com"
from_email_pass ="ahfrqlcmvzqcrmzo"
to_email_addr ="jolix1717@gmail.com"  # change to desired recipient
msg = EmailMessage()
msg['From'] = from_email_addr
msg['To'] = to_email_addr
msg['Subject'] = 'Plant Health Management System Alert'
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_email_addr, from_email_pass)


def read_arduino_data():
    ser = Nne  # Initialize ser to None
    nitrogen, phosphorus, potassium = None, None, None
    try:
        ser = serial.Serial('/dev/ttyACM0', 4800)
        if ser.isOpen():
            print("Serial port opened")
            sensor_data = ser.readline().decode().strip()
            print(sensor_data)
            values = list(map(int, sensor_data.split(',')))
            if len(values) == 3:
                nitrogen = values[0]
                phosphorus = values[1]
                potassium = values[2]
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser is not None:
            ser.close()
            print("Serial port closed")
    return nitrogen, phosphorus, potassium

def check_conditions_and_alert():
    while True:
        moisture_raw= MCP.read_adc(0)
        ph_value_raw = MCP.read_adc(1)
        moisture_value= -.33*moisture_raw+175
        ph_value = -1 / 32 * ph_value_raw + 32.3

        nitrogen, phosphorus, potassium = read_arduino_data()

        if moisture_value < 25: 
            body="Alert: Moisture level is low. You should water your plant. The recorded moisture level is: " + str(moisture_value) + "%"
            msg.set_content(body)
            server.send_message(msg)
        if moisture_value > 90:
            body="Alert: Moisture level is high. You should add water-storing crystals to your soil. The recorded moisture level is: " + str(moisture_value)+ "%"
            msg.set_content(body)
            server.send_message(msg)
        if ph_value < 5:
            body="Alert: pH level is out of range, it is too low. You should add hydrated lime to raise pH. The recorded pH level is: " + str(ph_value)
            msg.set_content(body)
            server.send_message(msg)
        if ph_value > 8:
            body="Alert: pH level is too high. You should add lemon juice to lower pH. The recorded pH level is: " + str(ph_value)
            msg.set_content(body)
            server.send_message(msg)
        if nitrogen < 30:
            body="Alert: Nitrogen level too low. You should add more fertilizer. The recorded moisture level is: " + str(nitrogen) + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        if nitrogen > 80:
            body="Alert: Nitrogen level very high. You should stop adding any nitrogen to your soil for now. The recorded moisture level is: " + str(nitrogen) + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        if phosphorus < 30:
            body="Alert: Phosphorus level is low. Consider adding more phosphorus fertilizer. The recorded moisture level is: " + str(phosphorus)  + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        if phosphorus > 80:
            body="Alert: Phosphorus level is high. Stop applying phosphorus fertilizer until further notice. The recorded moisture level is: " + str(phosphorus) + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        if potassium < 30:
            body="Alert: Potassium level is low Consider adding more potassium fertilizer. The recorded moisture level is: " + str(potassium) + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        if potassium > 80:
            body="Alert: Potassium level is high. Stop applying potassium fertilizer until the level decreases. The recorded moisture level is: " + str(potassium) + "mg/kg"
            msg.set_content(body)
            server.send_message(msg)
        time.sleep(30)

try:
    while True:
        check_conditions_and_alert()
except KeyboardInterrupt:
    pass
