# -*- coding: utf-8 -*-
import websocket
import logging
import json
import time
from pynput.keyboard import Key, Listener
import RPi.GPIO as gpio
try:
    import thread
except ImportError:
    import _thread as thread


class GpioComm:
    # ID_SD = 27    # Pin 27
    # ID_SC = 28    # Pin 28
    GPIO_5 = 5      # Pin 29
    # GND_30 = 30   # Pin 30
    GPIO_6 = 6      # Pin 31
    GPIO_12 = 12    # Pin 32
    GPIO_13 = 13    # Pin 33
    # GND_34 = 34   # Pin 34
    GPIO_19 = 19    # Pin 35
    GPIO_16 = 16    # Pin 36
    GPIO_26 = 26    # Pin 37
    GPIO_20 = 20    # Pin 38
    # GND_39 = 39   # Pin 39
    GPIO_21 = 21    # Pin 40

    LED = GPIO_5
    BUTTON = GPIO_6
    BUZZER = GPIO_12
    BALLANCE = GPIO_13

    _client = None
    listener = None
    car_id = 0
    display_id = None

    PROTO = 'ws://'
    HOST = '192.168.101.101'
    PORT = 8000
    URL = '/ws/sensor'

    def __init__(self, **kwargs):
        gpio.setmode(gpio.BCM)
        self._setup_gpio()
        self.car_id = kwargs.get('car_id')
        self.display_id = kwargs.get('display_id')

        logging.basicConfig(filename='pi-sensors.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
        logging.error('test of error')

    def _send_data_to_server(self):
        data = {}
        self._client.send(data)

    @staticmethod
    def _on_message(ws, message):
        data = json.dumps(message)
        if data['direction'] == 'client':
            logging.debug(message)

    @staticmethod
    def _on_error(ws, error):
        pass

    @staticmethod
    def _on_close(ws):
        pass

    @staticmethod
    def _on_open(ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                data = {
                    'command': '', 'message': f"Hello {i}"}
                ws.send()
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    @staticmethod
    def _read_sensors():
        try:
            button_state = gpio.input(GpioComm.BUTTON)
            if not button_state:
                gpio.output(GpioComm.LED, gpio.LOW)
            time.sleep(1)
        except Exception as e:
            logging.error(f'Error on read device sensor: {e}')

    @staticmethod
    def _on_press(key):
        print(f'{key} pressed')

    @staticmethod
    def _on_release(key):
        print(f'{key} release')
        if key == Key.esc:
            # Stop listener
            exit_program = False
            return exit_program

    def _setup_gpio(self):
        gpio.setup(self.LED, gpio.OUT)
        gpio.setup(self.BUTTON, gpio.IN, pullup=gpio.LOW)
        gpio.setup(self.BUZZER, gpio.OUT)
        gpio.add_event_detect(10, gpio.RISING, callback=GpioComm._read_sensors())
        # gpio.setup(self.BALANCE, gpio.IN)

    def setup_socket(self):
        host = f'{self.PROTO}{self.HOST}:{self.PORT}{self.URL}/{self.car_id}/{self.display_id}'
        try:
            websocket.enableTrace(True)
            self._client = websocket.WebSocketApp(
                host,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close)
            self._client.on_open = self._on_open
            self._client.run_forever()
        except Exception as e:
            logging.error(f'Error on connect to display server: {e}')

    # Collect events until released
    def get_keyboard(self):
        self.listener = Listener(
            on_press=GpioComm._on_press,
            on_release=GpioComm._on_release
        )
        self.listener.join()


sensor = GpioComm()
sensor.setup_gpio()
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

