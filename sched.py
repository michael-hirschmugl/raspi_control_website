import schedule
import time
from enum import Enum
import json
from os.path import exists
import sys
from datetime import datetime
import serial
from signal import signal, SIGINT
from crcmod import mkCrcFun

def handler(signal_received, frame):
    # Handle any cleanup here
    print(dbg_tm(), "SIGINT or CTRL-C detected. Exiting gracefully")
    sys.exit(0)

def func():
    print(dbg_tm(), "Geeksforgeeks")

def settings_file_exists(settingsFileName):
    if exists(settingsFileName):
        return File_Status.SAME_FOLDER
    else:
        if exists("../" + settingsFileName):
            return File_Status.UPPER_FOLDER
        else:
            return File_Status.NO_FILE

class File_Status(Enum):
    NO_FILE = 0
    SAME_FOLDER = 1
    UPPER_FOLDER = 2

class Errors(Enum):
    NO_ERROR = 0
    COULD_NOT_WRITE_TO_SETTINGS_FILE = -1
    COULD_NOT_GENERATE_SETTINGS_FILE = -2
    COULD_NOT_OPEN_SETTINGS_FILE_TO_READ = -3
    COULD_NOT_CONNECT_TO_INVERTER = -4

def generate_settings_file(settingsFileName, folderLevel, settingsContent):
    settingsJson = json.dumps(settingsContent)
    if folderLevel == File_Status.UPPER_FOLDER:
        settingsFileName = "../" + settingsFileName
    try:
        with open(settingsFileName,"w") as settingsFile:
            settingsFile.write(settingsJson)
    except:
        print(dbg_tm(), "Could not write settings file.")
        return [Errors.COULD_NOT_GENERATE_SETTINGS_FILE, folderLevel]
    return [Errors.NO_ERROR, folderLevel]

def read_settings_file(settingsFileName, folderLevel):
    if folderLevel == File_Status.UPPER_FOLDER:
        settingsFileName = "../" + settingsFileName
    try:
        with open(settingsFileName, "rb") as settingsFile:
            settingsContent = json.load(settingsFile)
    except:
        print(dbg_tm(), "Could not open settings file for reading.")
        return [Errors.COULD_NOT_OPEN_SETTINGS_FILE_TO_READ, []]
    return [Errors.NO_ERROR, settingsContent]

def write_settings_file(settingsFileName, folderLevel, settingsContent):
    settingsJson = json.dumps(settingsContent)
    if folderLevel == File_Status.UPPER_FOLDER:
        settingsFileName = "../" + settingsFileName
    try:
        with open(settingsFileName,"w") as settingsFile:
            settingsFile.write(settingsJson)
    except:
        print(dbg_tm(), "Could not write to settings file.")
        return Errors.COULD_NOT_WRITE_TO_SETTINGS_FILE
    return Errors.NO_ERROR

def dbg_tm():
    dt = datetime.now()
    str_date_time = dt.strftime("%d-%m-%Y, %H:%M:%S")
    return str_date_time

def crc16_xmodem(data):
    crc16 = mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
    return crc16(data)

def test_func(inverter):
    command = "QMN"
    commandBytes = command.encode("utf-8")
    commandCrc = crc16_xmodem(commandBytes)
    commandBytesArray = bytearray(commandBytes)
    commandBytesArray.append(commandCrc >> 8)
    commandBytesArray.append(commandCrc & 255)
    commandBytesArray.append(13)
    
    try:
        inverter.write(commandBytesArray)
    except serial.SerialException as e:
        print(dbg_tm(), "Serial write error.")
        return None
    except TypeError as e:
        print(dbg_tm(), "Serial write error.")
        return None

    try:
        bResponse = inverter.read_until(b"\x0D", size=128)
    except serial.SerialException as e:
        print(dbg_tm(), "Serial read error.")
        return None
    except TypeError as e:
        print(dbg_tm(), "Serial read error.")
        return None
    else:
        #Some data was received
        sResponse = bResponse[0:len(bResponse)-3].decode()
        print(commandBytesArray, sResponse)
        return None

    return None

def test_func2(inverter):
    command = "QID"
    commandBytes = command.encode("utf-8")
    commandCrc = crc16_xmodem(commandBytes)
    commandBytesArray = bytearray(commandBytes)
    commandBytesArray.append(commandCrc >> 8)
    commandBytesArray.append(commandCrc & 255)
    commandBytesArray.append(13)
    
    try:
        inverter.write(commandBytesArray)
    except serial.SerialException as e:
        print(dbg_tm(), "Serial write error.")
        return None
    except TypeError as e:
        print(dbg_tm(), "Serial write error.")
        return None

    try:
        bResponse = inverter.read_until(b"\x0D", size=128)
    except serial.SerialException as e:
        print(dbg_tm(), "Serial read error.")
        return None
    except TypeError as e:
        print(dbg_tm(), "Serial read error.")
        return None
    else:
        #Some data was received
        sResponse = bResponse[0:len(bResponse)-3].decode()
        print(commandBytesArray, sResponse)
        return None

    return None

if __name__ == "__main__":

    signal(SIGINT, handler)

    # Initial values
    ##################################
    settingsFileName = "settings.ini"
    inverterRS232Settings = {"port": "/dev/ttyUSB0", "baudrate": 2400, "timeout": 5}

    # Settings file handling
    ##################################
    settingsFileFolderLevel = settings_file_exists(settingsFileName)

    if settingsFileFolderLevel == File_Status.NO_FILE:
        print(dbg_tm(), "No settings file found. Generating...")
        settingsFileFolderLevel = File_Status.SAME_FOLDER
        if generate_settings_file(settingsFileName, settingsFileFolderLevel, inverterRS232Settings)[0] == Errors.COULD_NOT_GENERATE_SETTINGS_FILE:
            print(dbg_tm(), "Could not generate settings file. Stop.")
            sys.exit(Errors.COULD_NOT_GENERATE_SETTINGS_FILE)
        else:
            print(dbg_tm(), "Settings file generated.")
    else:
        print(dbg_tm(), "Settings file found at folder level:", settingsFileFolderLevel)
    
    [errTemp, readSettingsContent] = read_settings_file(settingsFileName, settingsFileFolderLevel)
    if errTemp == Errors.COULD_NOT_OPEN_SETTINGS_FILE_TO_READ:
        print(dbg_tm(), "Could not open settings file. Stop.")
        sys.exit(Errors.COULD_NOT_OPEN_SETTINGS_FILE_TO_READ)

    for x in inverterRS232Settings:
        if x not in readSettingsContent:
            print(dbg_tm(), "Adding " + x + " to settings file.")
            readSettingsContent[x] = inverterRS232Settings[x]
            write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent)
    
    if write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent) == Errors.COULD_NOT_WRITE_TO_SETTINGS_FILE:
        print(dbg_tm(), "Could not open settings file. Stop.")
        sys.exit(Errors.COULD_NOT_WRITE_TO_SETTINGS_FILE)

    [errTemp, readSettingsContent] = read_settings_file(settingsFileName, settingsFileFolderLevel)
    if errTemp == Errors.COULD_NOT_OPEN_SETTINGS_FILE_TO_READ:
        print(dbg_tm(), "Could not open settings file. Stop.")
        sys.exit(Errors.COULD_NOT_OPEN_SETTINGS_FILE_TO_READ)
    print(dbg_tm(), "Content of settings file:\n", readSettingsContent)

    # Establish connection to inverter
    ##################################
    connectionTries = 0
    while True:
        try:
            with serial.Serial(inverterRS232Settings["port"], inverterRS232Settings["baudrate"], inverterRS232Settings["timeout"]) as inverter:
                print(dbg_tm(), "Connected to inverter!")
                inverter.reset_input_buffer()
                inverter.reset_output_buffer()
                inverter.flush()
                schedule.every(5).seconds.do(func)
                schedule.every(2).seconds.do(test_func, inverter)
                schedule.every(4).seconds.do(test_func2, inverter)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
                break
        except serial.SerialException as e:
            #There is no new data from serial port
            connectionTries = connectionTries + 1
            print(dbg_tm(), "Could no connect to inverter. Try:", connectionTries)
            if connectionTries >= 5:
                print(dbg_tm(), "Could no connect to inverter. Stop.")
                sys.exit(Errors.COULD_NOT_CONNECT_TO_INVERTER)
        except TypeError as e:
            #Disconnect of USB->UART occured
            sys.exit(Errors.COULD_NOT_CONNECT_TO_INVERTER)
                


    #schedule.every(5).seconds.do(func)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)