#!/usr/bin/env python
import socket
#import atexit
import pigpio
import re
#import signal
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED
import time

factory = PiGPIOFactory(host='192.168.10.1')

client_socket11 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket11.connect(("127.0.0.1", 10001))

client_socket12 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket12.connect(("127.0.0.1", 10000))

client_socket13 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket13.connect(("127.0.0.1", 10002))

client_socket14 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket14.connect(("127.0.0.1", 10003))



Xdesno = LED(16,pin_factory=factory)
Xlevo = LED(13,pin_factory=factory)
Zgore = LED(6,pin_factory=factory)
Zdole = LED(5,pin_factory=factory)
Ynazad = LED(19,pin_factory=factory)  # ka zidu
Ynapred = LED(20,pin_factory=factory)  # od zida
Xdesno.on()
Xlevo.on()
Zgore.on()
Zdole.on()
Ynazad.on()
Ynapred.on()
#senzor za nuliranje 1gpio
pi = pigpio.pi()



def iskljucenoSve():
    Xdesno.on()
    Xlevo.on()
    Zgore.on()
    Zdole.on()
    Ynazad.on()
    Ynapred.on()


    

class decoder:

   """Class to decode mechanical rotary encoder pulses."""

   def __init__(self, pi, gpioA, gpioB, callback):

   

      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB
      self.callback = callback

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def _pulse(self, gpio, level, tick):



      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-1)

   def cancel(self):

      self.cbA.cancel()
      self.cbB.cancel()

if __name__ == "__main__":

    import time
    import pigpio
    import socket
    import rotary_encoder
    import math
    
    
    #client_socket11 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket11.connect(("127.0.0.1", 5011))

    posX = 0
    posY = 0
    posZ = 0

    def callback(way):

        global posX

        posX += way

        client_socket12.send((str(posX) + '\n') .encode())


    decoder = rotary_encoder.decoder(pi, 27, 17, callback)
    
    def callbackY(way1):

        global posY

        posY += way1

        client_socket13.send((str(posY) + '\n') .encode())
        


    decoder = rotary_encoder.decoder(pi, 21, 20, callbackY)


    def callbackZ(way2):

        global posZ

        posZ += way2

        client_socket14.send((str(posZ) + '\n') .encode())
        


    decoder = rotary_encoder.decoder(pi, 9, 10, callbackZ)


    while True:
        #iskljucenoSve()
        client_socket12.send((str(posX) + '\n') .encode())
        client_socket13.send((str(posY) + '\n') .encode())
        client_socket14.send((str(posZ) + '\n') .encode())
        
        print (posZ)
        global podatak
        client_socket11.settimeout(None)
        podatak=client_socket11.recv(1024).decode('utf-8')
        #podatak = re.sub("[^0-9]", "", podatak)
        print(podatak)

        
###############NULIRANJE OSE        
        if "hanzo" in podatak:
            print ("RADI HANZO")
        if 'nuliranje' in podatak:
#             global senzor
#             senzor = (pi.read(11))
            while (pi.read(15) == 0):
                
                (pi.read(15))
                
            else:
               
                iskljucenoSve()
                time.sleep(1)
                
                time.sleep(3.7)
                iskljucenoSve()
                time.sleep(2)
                posX = 0
                pass
            continue
#                  posX = 0
#                  nula=(math.isclose(150, posX, abs_tol = 8.0)) # vidi gde stoji sto u ravni sa testerom
#                  time.sleep(1)
#                  while true: 
#                      if posX == nula: # ovde tolerancija treba ispitati da se od nule vrati na plus neki impuls i staviti varijablu sa tolerancijom
#                          
#                          iskljucenoSve()
#                          break
#                      else:
#                          smerCW()
#                      break

                    
        if 'trenutna' in podatak:


            client_socket11.send((str(posX) + '\n') .encode())

            
            continue
        if 'stop' in podatak:
            continue

        if 'start' in podatak:
            
            while True:     #ovde pocinje X osa
                
                file1 = open('testIzPrograma.txt', 'r')
                Lines = file1.readlines()

                for line in Lines:
                    if "X" in line:
                        print(line)
                        X = line.replace("X", "")
                        X = int(X)
                        print(X)
                
                
                        global pozicijaX
                        
                        pozicijaX=(math.isclose(X, posX, abs_tol = 2.0))
                        print (pozicijaX)
                        while 1:
                            if pozicijaX is True:
                                pozicijaX=(math.isclose(X, posX, abs_tol = 2.0))
                                
                                iskljucenoSve()   # 0 releja
                                
        #                         
                                time.sleep(2)
                                pozicijaX=(math.isclose(X, posX, abs_tol = 2.0))
                                if pozicijaX is True:
        #                             
                                    break
                                else:
        #                             
                                    continue
                                
                                 #nista nece uraditi
                            
                            else:
                                pozicijaX=(math.isclose(X, posX, abs_tol = 2.0))
                                print(pozicijaX)
                                #print ("usao u else")
                                time.sleep(0.001)    # interval provere
                                if X > posX:
                                    print("DESNO")
                                    Xlevo.on()
                                    Xdesno.off()
                                    
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
        #                                     
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
                                if X < posX:
                                    
                                    print("LEVO")
                                    Xdesno.on()
                                    Xlevo.off()
                                    
                                    
                                        
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
            #                     
                                continue
                            
                      ###  break ### ?????????????????????????????? proba da li treba break
                            ###OVO JE ZA Y
                    if "Y" in line:
                        print(line)
                        Y = line.replace("Y", "")
                        Y = int(Y)
                        print(Y)
                
                
                        global pozicijaY
                        
                        pozicijaY=(math.isclose(Y, posY, abs_tol = 2.0))
                        print (pozicijaY)
                        while 1:
                            if pozicijaY is True:
                                pozicijaY=(math.isclose(Y, posY, abs_tol = 2.0))
                                
                                iskljucenoSve()   # 0 releja
                                
        #                         
                                time.sleep(2)
                                pozicijaY=(math.isclose(Y, posY, abs_tol = 2.0))
                                if pozicijaY is True:
        #                             
                                    break
                                else:
        #                             
                                    continue
                                
                                 #nista nece uraditi
                            
                            else:
                                pozicijaY=(math.isclose(Y, posY, abs_tol = 2.0))
                                print(pozicijaY)
                                #print ("usao u else")
                                time.sleep(0.001)    # interval provere
                                if Y > posY:
                                    #print("DESNO")
                                    Ynapred.on()
                                    Ynazad.off()
                                    
                                    
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
        #                                     
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
                                if Y < posY:
                                    
                                    #print("LEVO")
                                    Ynazad.on()
                                    Ynapred.off()
                                    
                                    
                                        
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
            #                     
                                continue  
                    if "Z" in line:
                        print(line)
                        Z = line.replace("Z", "")
                        Z = int(Z)
                        print(Z)
                
                
                        global pozicijaZ
                        
                        pozicijaZ=(math.isclose(Z, posZ, abs_tol = 100.0))
                        print (pozicijaZ)
                        while 1:
                            if pozicijaZ is True:
                                pozicijaZ=(math.isclose(Z, posZ, abs_tol = 100.0))
                                
                                iskljucenoSve()   # 0 releja
                                
        #                         
                                time.sleep(2)
                                pozicijaZ=(math.isclose(Z, posZ, abs_tol = 100.0))
                                if pozicijaZ is True:
        #                             
                                    break
                                else:
        #                             
                                    continue
                                
                                 #nista nece uraditi
                            
                            else:
                                pozicijaZ=(math.isclose(Z, posZ, abs_tol = 100.0))
                                print(pozicijaZ)
                                #print ("usao u else")
                                time.sleep(0.001)    # interval provere
                                if Z > posZ:
                                    #print("DESNO")
                                    Zgore.on()
                                    Zdole.off()
                                    
                                    
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
        #                                     
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
                                if Z < posZ:
                                    
                                    #print("LEVO")
                                    Zdole.on()
                                    Zgore.off()
                                    
                                    
                                        
                                    try:
                                        client_socket11.settimeout(0.05)
                                        slusam=client_socket11.recv(1024).decode('utf-8')
                                        if "stop" in slusam:
                                            iskljucenoSve()
        #                                     
                                            break
                                        break
                                    except:
                                        pass
                                    continue
            #                     
                                continue