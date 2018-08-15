#!/usr/bin/python3
from flask import Flask
from samsung import SamsungModule
from broadLink import BroadLinkDevice

import miio
import json
app = Flask(__name__)


broadLinkDevices = {}
xiaomiDevices = {}


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/samsung/is_on/<ip>/<mac>/')
def samsung_is_on(ip, mac):
    tv = SamsungModule(ip, mac)
    if tv.isTVOn:
        return "On"
    else:
        return "Off"


@app.route('/samsung/mute/<ip>/<mac>/')
def samsung_mute(ip, mac):
    tv = SamsungModule(ip, mac)
    if tv.isTVOn:
        tv.mute()
    return "Ok"


@app.route('/samsung/on/<ip>/<mac>/')
def samsung_on(ip, mac):
    tv = SamsungModule(ip, mac)
    tv.turnOn()
    return "Ok"


@app.route('/samsung/off/<ip>/<mac>/')
def samsung_off(ip, mac):
    tv = SamsungModule(ip, mac)
    tv.turnOff()
    return "Ok"


@app.route('/samsung/info/<ip>/<mac>/')
def samsung_info(ip, mac):
    tv = SamsungModule(ip, mac)
    return json.dumps(tv.getTVInfo())


def broadLikGetDeviceName(ip, mac, devtype):
    return str(ip + mac + devtype)


@app.route('/broadlink/is_on/<ip>/<mac>/<devtype>/')
def broadlink_isOn(ip, mac, devtype):
    global broadLinkDevices
    deviceName = broadLikGetDeviceName(ip, mac, devtype)
    if deviceName not in broadLinkDevices:
        broadLinkDevices[deviceName] = BroadLinkDevice(ip, mac, devtype)

    ret = broadLinkDevices[deviceName].is_On()
    retData = {}
    if ret[0]:
        retPower = None
        retData["result"] = True
        if broadLinkDevices[deviceName].hasPowerMonitor:
            retPower = broadLinkDevices[deviceName].getPower()
            if retPower[0]:
                retData["power"] = retPower[1]

        if ret[1]:
            retData["status"] = "On"
        else:
            retData["status"] = "Off"
    else:
        retData["result"] = False
        retData["error"] = ret[1]

    return json.dumps(retData)


@app.route('/broadlink/on/<ip>/<mac>/<devtype>/')
def broadlink_On(ip, mac, devtype):
    global broadLinkDevices
    deviceName = broadLikGetDeviceName(ip, mac, devtype)
    if deviceName not in broadLinkDevices:
        broadLinkDevices[deviceName] = BroadLinkDevice(ip, mac, devtype)

    ret = broadLinkDevices[deviceName].on()
    if ret[0]:
        if ret[1]:
            return json.dumps({"result": True, "status": "On"})
        else:
            return json.dumps({"result": True, "status": "Off"})
    else:
        return json.dumps({"result": False, "error": ret[1]})


@app.route('/broadlink/off/<ip>/<mac>/<devtype>/')
def broadlink_Off(ip, mac, devtype):
    global broadLinkDevices
    deviceName = broadLikGetDeviceName(ip, mac, devtype)
    if deviceName not in broadLinkDevices:
        broadLinkDevices[deviceName] = BroadLinkDevice(ip, mac, devtype)

    ret = broadLinkDevices[deviceName].off()
    if ret[0]:
        if ret[1]:
            return json.dumps({"result": True, "status": "On"})
        else:
            return json.dumps({"result": True, "status": "Off"})
    else:
        return json.dumps({"result": False, "error": ret[1]})


def xiaomiGetDevice(ip, token):
    devName = ip + token
    if devName not in xiaomiDevices:
        dev = miio.Plug(ip, token, False)
        xiaomiDevices[devName] = dev
    return xiaomiDevices[devName]


@app.route("/xiaomi/is_on/<ip>/<token>/")
def xiaomi_isOn(ip, token):
    dev = xiaomiGetDevice(ip, token)
    retData = {}
    try:
        status = dev.status()
        retData["result"] = True
        if status.is_on:
            retData["status"] = "On"
        else:
            retData["status"] = "Off"

    except Exception as e:
        retData["result"] = False
        retData["error"] = str(e)

    return json.dumps(retData)


@app.route("/xiaomi/on/<ip>/<token>/")
def xiaomi_on(ip, token):
    dev = xiaomiGetDevice(ip, token)
    retData = {}
    try:
        ret = None
        ret = dev.on()
        if ret[0] == "ok":
            retData["result"] = True
            retData["status"] = "On"
        else:
            retData["result"] = False
            retData["error"] = "Got wrong respone!"
    except Exception as e:
        retData["result"] = False
        retData["error"] = str(e)

    return json.dumps(retData)


@app.route("/xiaomi/off/<ip>/<token>/")
def xiaomi_off(ip, token):
    dev = xiaomiGetDevice(ip, token)

    retData = {}
    try:
        ret = None
        ret = dev.off()
        if ret[0] == "ok":
            retData["result"] = True
            retData["status"] = "Off"
        else:
            retData["result"] = False
            retData["error"] = "Got wrong respone!"
    except Exception as e:
        retData["result"] = False
        retData["error"] = str(e)

    return json.dumps(retData)


if __name__ == '__main__':
    app.run(debug=True, port="8050", host='0.0.0.0')
