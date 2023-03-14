#PicoW Wifi Connect with Error Messages
import network
import time
import sys

global_message = "Default Global Message"    #Message String
ssid = ''
password = ''
network.hostname ("PicoTester")              #Set the name of the PicoW Board seen in your router

                                             #The Pico W has two Wifi interfaces:
                                             #network.STA_IF, the station interface
                                             #network.AP_IF, the access-point interface, up to 4 devices
#wlan = network.WLAN(network.AP_IF)          #Set the Wifi mode to Access Point
wlan = network.WLAN(network.STA_IF)          #Set the Wifi mode to STATION, use this by default

#Wlan.status() Error Codes Dictionary        #The various error messages defined
wifi_err_status_dict = {
    "-3": "STAT_WRONG_PASSWORD – failed due to incorrect password",
    "-2": "STAT_NO_AP_FOUND – failed because no access point replied",
    "-1": "STAT_CONNECT_FAIL – failed due to other problems",
    "0": "STAT_IDLE – no connection and no activity",
    "1": "STAT_CONNECTING – connecting in progress",
    "3": "STAT_GOT_IP – connection successful",
    "??": "STAT_BEACON_TIMEOUT",             # Unknown err code to me, couldn't test
    "?!": "STAT_HANDSHAKE_TIMEOUT"           # Unknown err code to me, couldn't test
}

### FUNCTION
def connect_wifi():
    #Check if Wifi is enabled and make it active
    if wlan.active() == False:
        wlan.active(True)
        global_message = "Activating Wifi"
        print(global_message)
    
    #Check of Wifi is connected
    if wlan.isconnected() == False:
        #Connect to Wifi
        global_message = "Connecting to Wifi..."
        print(global_message)
        wlan.connect(ssid, password)
        
        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:   #If the error message is out of scope
                break                                     #break the loop
            max_wait -= 1
            global_message = "...waiting for connection..."
            print(global_message + str(wlan.status()))
            time.sleep(1)
        
        # Handle connection error v2        
        if wlan.status() != 3:
            network_err = wifi_err_status_dict.get(str(wlan.status())) #Get the error code from the dictionary
            print(network_err)
            #raise RuntimeError(network_err)
            sys.exit()                                    #Exit program ... for now
        else:
            global_message = ".Connected."
            print(global_message)
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )
            print(wlan.status())
    else:
        print ("...Already Connected to Wifi, Bypassing")
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        print(wlan.status())

###############       
connect_wifi()

#wlan.disconnect()
#wlan.active(False)