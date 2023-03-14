#PicoW - Scan and Log Wifi Networks
import network
import binascii
import utime

wlan = network.WLAN() #  network.WLAN(network.STA_IF)
wlan.active(True)
#wlan_mac = (ubinascii.hexlify(wlan.config('mac')).decode()).upper()

#wlan.scan() wifi security dictionary
#Returns list of tuples with the information about WiFi access points: (ssid, bssid, channel, RSSI, security, hidden)
#There are five values for security:
wifi_scan_security_dict = {
    "0": "OPEN",
    "2": "WEP",
    "3": "WPA-PSK",
    "4": "WPA2-PSK",
    "5": "WPA/WPA2-PSK"   
}
# 4=WPA2, 2=WPA, 1=WEP_PSK, so 5=WPA2+WEP_PSK
// Return value of cyw43_wifi_link_status
#define CYW43_LINK_DOWN (0)
#define CYW43_LINK_JOIN (1)
#define CYW43_LINK_NOIP (2)
#define CYW43_LINK_UP (3)
#define CYW43_LINK_FAIL (-1)
#define CYW43_LINK_NONET (-2)
#define CYW43_LINK_BADAUTH (-3)
#and two for hidden:
# 0 – visible
# 1 – hidden

#Write to a logfile
def write_log(loginfo):
    log_file = open("wifi_scanner_log.txt", "a")
    log_file.write(str(utime.localtime()) + " : " + str(loginfo) + "\n")
    log_file.close()
            
def wifi_scanner():
    write_log(",SSID, BSSID (MAC), CHANNEL, RSSI, SECURITY, HIDDEN") # Title Header for easier reading log
    networks = wlan.scan() # list with tupples with 6 fields [ssid(0), bssid(1), channel(2), RSSI(3), security(4), hidden(5)]
    i=0
    networks.sort(key=lambda x:x[0],reverse=True) # sorted on ssid (0)
    for w in networks:
        i+=1
        mac = binascii.hexlify(w[1]).decode()
        z=0
        mac2 = ':'.join(mac[z:z+2] for z in range(0,12,2))
        
        secure = wifi_scan_security_dict.get(str(w[4]))
        #print(secure)
        loginfo = i,w[0].decode(),mac2.upper(),w[2],w[3],secure,w[5]
        #loginfo = i,w[0].decode(),mac2.upper(),w[2],w[3],w[4],w[5]
        #loginfo = i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5]
        #write_log(loginfo)
        print(i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5])
        print(i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],secure,w[5])

##############################################
try:
    while True:
        wifi_scanner()
        utime.sleep(5)
        print("Pressed CTRL+C to exit")
except KeyboardInterrupt:
    machine.reset
    print("DONE")
    
