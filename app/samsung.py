import urllib.request
import json
import socket

import samsungctl
from samsungctl import exceptions
from wakeonlan import send_magic_packet


class SamsungTVInfo(object):

    def __getTvInfo(self, ip):
        try:
            urlTv = "http://%s:8001/api/v2/" % (ip)
            webData = urllib.request.urlopen(urlTv, timeout=1)
            data = webData.read()
            encoding = webData.info().get_content_charset('utf-8')
            return json.loads(data.decode(encoding))
        except urllib.error.URLError:
            return False
        except socket.timeout:
            return False
        except:
            return {}

    def __init__(self, ip):
        data = self.__getTvInfo(ip)
        self.modelName = data['device']['modelName']
        self.name = data['name']
        self.ip = ip
        self.mac = data['device']['wifiMac']
        self.networkType = data['device']['networkType']


class SamsungModule(object):
    @property
    def isTVOn(self):
        urlTv = "http://%s:8001/api/v2/" % (self.ip)
        try:
            urllib.request.urlopen(urlTv, timeout=1)
        except urllib.error.URLError:
            return False
        except socket.timeout:
            return False
        except:
            return False
        return True

    def __init__(self, hostIp, mac, name="Domoticz", port=None, conectionMode="websocket", description="PC", id="", timeout=1):
        self.ip = hostIp
        self.mac = mac

        self.config = {
            "name": name,
            "description": description,
            "id": id,
            "host": hostIp,
            "method": conectionMode,
            "timeout": timeout,
            "port": port
        }

    def getTVInfo(self):
        info = SamsungTVInfo(self.ip)
        return {"model": info.modelName, "name": info.name, "ip": info.ip, "mac": info.mac, "networktype": info.networkType}

    def __sendCommand(self, command):
        try:
            print(self.config)
            with samsungctl.Remote(self.config) as remote:
                for key in command:
                    remote.control(key)

        except exceptions.ConnectionClosed:
            print("Error: Connection closed!")
        except exceptions.AccessDenied:
            print("Error: Access denied!")
        except exceptions.UnknownMethod:
            print(
                "Error: Unknown method '{}'".format(self.config["method"]))
        except socket.timeout:
            print("Error: Timed out!")
        except OSError as e:
            print("Error: %s", e.strerror)
        # except:
        #     print("Unexpected error:", sys.exc_info()[0])

    def turnOff(self):
        self.__sendCommand(["KEY_POWER"])

    def mute(self):
        self.__sendCommand(["KEY_MUTE"])

    def turnOn(self):
        print("Send Magic package:%s" % (self.mac))
        send_magic_packet(self.mac)
