import time
import urequests
import network
from neopixel import NeoPixel
from machine import Pin
import micropython, sys, gc

ssid = 'Wokwi-GUEST'
password = ''
urls = (
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/",
"https://www.google.com/alyaiscool")

serviceStatus = [200,200,200,200,200,200,200,200]

def connectToWifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, '')
    while not sta_if.isconnected():
      print(".", end="")
      time.sleep(0.1)
    print(" Connected!")

def checkUrls():
  for index, url in enumerate(urls):
    try:
      print("Checking ", url)
      resp = urequests.head(url)
      print(index, "----", resp.status_code)
      serviceStatus[index] = resp.status_code
      del(resp)
      gc.collect()
    except:
      serviceStatus[index] = 500
      gc.collect()

def ledToRainbow(ledNumber):
  rainbowBand = 0
  if ledNumber < 8:
    rainbowBand = ledNumber
  else: # 8 9 10 11 12 13 14 15
    rainbowBand = abs(15-ledNumber)
  return rainbowBand
  
def lightPixels():
  for i in range(16):
    if serviceStatus[ledToRainbow(i)] == 200:
      pixels[i] = rainbow[ledToRainbow(i)]
    else:
      pixels[i] = (0,0,0)
  pixels.write()

rainbow = [(255 , 0 , 0),
(255 , 125 , 0),
(255 , 255 , 0),
(125 , 255 , 0),
(0 , 255 , 0),
(0 , 255 , 125),
(0 , 255 , 255),
(0 , 125 , 255)]

pixels = NeoPixel(Pin(13), 16)
connectToWifi()
lightPixels()

while True:
  checkUrls()
  lightPixels()
  time.sleep(60)

