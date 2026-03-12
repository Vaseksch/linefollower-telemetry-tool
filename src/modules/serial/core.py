import serial
import serial.tools.list_ports
from .const import BAUD_RATE, ESP_KNOWN_VIDS_PIDS, FEATURES
from loguru import logger
import pandas as pd
from pandas import DataFrame

def find_esp_ports():
    """Return a list of serial ports likely connected to an ESP device."""
    candidates = []
    all_ports = serial.tools.list_ports.comports()

    for port in all_ports:
        vid = port.vid
        pid = port.pid

        matched = any(
            vid == v and (p is None or pid == p)
            for v, p in ESP_KNOWN_VIDS_PIDS
        )

        desc = (port.description or "").lower()
        keyword_match = any(k in desc for k in [
            "cp210", "ch340", "ch341", "ftdi", "uart", "usb serial",
            "esp", "arduino", "wemos", "nodemcu"
        ])

        if matched or keyword_match:
            candidates.append(port)

    return candidates

def read_serial_data() -> DataFrame:
    esp_ports = find_esp_ports()
    data_set: list = []
    if not esp_ports:
        logger.error("No port found")
        raise serial.PortNotOpenError

    for port in esp_ports:
        try:
            with serial.Serial(port.device, BAUD_RATE) as ser:
                data_avalible = False
                while ser.is_open:
                    data = ser.readline()
                    if data:
                        line = data.decode("utf-8", errors="replace")
                        line = line.strip()
                        if line == "data_end":
                            data_avalible = False
                        if data_avalible:
                            features = line.split(";")      
                            row = {}
                            for i, feature in enumerate(features):
                                row[FEATURES[i]] = feature
                            data_set.append(row)
                        if line == "data_start":
                            data_avalible = True
                    
                    if not data_avalible:
                        dataframe: DataFrame = pd.DataFrame(data=data_set, columns=FEATURES)    
                        dataframe["time"] = pd.to_numeric(dataframe["time"], errors="coerce")
                        dataframe["error"] = pd.to_numeric(dataframe["error"], errors="coerce")
                        dataframe["correction"] = pd.to_numeric(dataframe["correction"], errors="coerce")
                        dataframe["derivative"] = pd.to_numeric(dataframe["derivative"], errors="coerce") 
                        dataframe["mot_a_speed"] = pd.to_numeric(dataframe["mot_a_speed"], errors="coerce")          
                        dataframe["mot_b_speed"] = pd.to_numeric(dataframe["mot_b_speed"], errors="coerce")          
                        logger.debug(dataframe)
                        return dataframe
        except serial.SerialException as e:
            logger.error(f"Failed on port {port.device}", port.device, e)
            raise e