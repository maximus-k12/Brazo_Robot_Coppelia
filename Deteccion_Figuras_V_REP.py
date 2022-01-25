S#UNIVERSIDAD SAN CARLOS DE GUATEMALA
#FACULTADE DE INGENIERIA
#ESCUELA DE MECANICA ELECTRICA
#LABORATORIO DE ROBOTIA

#--------------------------------- Gurpo No.4 ------------------------
#Nonbre: Frank Robinson Morales Hernandez       Carne: 201503767
#Nombre: Adolfo Max Rodriguez Pimentesl         Carne: 201444696

# importamos las librerías necesarias
import sim
import numpy as np
import sys
import time
import cv2
import numpy as linealg
import matplotlib.pyplot as plt
import time

#------------------------- Modulo de CoppeliaSim -----------------------
def connect(port):
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID

clientID = connect(19999)
# Obtenemos el manejador para el target 
returnCode,handle=sim.simxGetObjectHandle(clientID,'target',sim.simx_opmode_blocking)
target = handle
print(target)
# A partir de su manejador podemos accionar sobre el objeto, por ejemplo, obtener su posición
returnCode,pos=sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_blocking)
print(pos)
#Guardamos el handle de la cámara del robot (el 'Vision_sensor')
error_cam, camara = sim.simxGetObjectHandle(clientID, 'Camara', sim.simx_opmode_oneshot_wait)
#Capturamos un frame para activar la cámara y esperamos 1 segundo:
_, resolution, image = sim.simxGetVisionSensorImage(clientID, camara, 0, sim.simx_opmode_streaming)
time.sleep(1)

while(1):
    #Capturamos un frame de la cámara del robot. Guardamos la imagen y su resolución:
    _, resolution, image = sim.simxGetVisionSensorImage(clientID, camara, 0, sim.simx_opmode_buffer)
    #Modificaremos esta imagen para que OpenCV pueda tratarla:
    img = np.array(image, dtype = np.uint8) #La convertimos a un array de numpy
    img.resize([resolution[0], resolution[1], 3]) #Cambiamos sus dimensiones
    img = np.rot90(img,2) #La rotamos 90 grados para enderezarla
    img = np.fliplr(img) #La invertimos
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #Cambiamos su espacio de color de RGB a BGR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#imagen binaria
    canny = cv2.Canny(gray, 10, 150)#algoritmo de detección de bordes
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)
    _,cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#Funcion para poder encontrar los contronos externos

    for c in cnts:

        epsilon = 0.01*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True) #Funcion de aproximacion de Curvas poligonal
        #print(len(approx))
        x,y,w,h = cv2.boundingRect(approx)

#-------------------------------------------- TRIANGULO --------------------------------
        if len(approx)==3: 
            cv2.putText(img,'Triangulo', (x,y-5),1,1,(0,255,0),1)
            inputBuffer = bytearray()
            res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_1", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
            res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_1", [0],[],[], inputBuffer, sim.simx_opmode_blocking)

#---------------------------------------------- CUADRADO --------------------------------
        if len(approx)==4:
            aspect_ratio = float(w)/h
            print('aspect_ratio= ', aspect_ratio)
            if aspect_ratio == 1:
                cv2.putText(img,'Cuadrado', (x,y-5),1,1,(0,255,0),1)
                inputBuffer = bytearray()
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_2", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_2", [0],[],[], inputBuffer, sim.simx_opmode_blocking)                

 #------------------------------------------- CIRCUNFERENCIA --------------------------------                             
        if len(approx)>10:
            inputBuffer = bytearray()
            cv2.putText(img,'Circulo', (x,y-5),1,1,(0,255,0),1)
            res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_3", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
            res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_3", [0],[],[], inputBuffer, sim.simx_opmode_blocking) 
            
#----------------------- dibujar el contorno de la figura encontrada --------------        
    cv2.drawContours(img, [approx], 0, (0,255,0),2)# funcion para dibujar los contornos
#------Mostramos la imagen--------------------  
    cv2.imshow('Image', img) 
    #Se sale con S.
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
#Cerramos la conexión:
cap.release()
cv2.destroyAllWindows()
