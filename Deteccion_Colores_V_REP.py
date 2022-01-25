
#UNIVERSIDAD SAN CARLOS DE GUATEMALA
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
import numpy as np
import matplotlib.pyplot as plt

#----------------------- Modulo de CoppeliaSim-----------------------
def connect(port):
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID
clientID = connect(19999)
#--------------------- Conexion con el Scrip-------------------------
#Guardamos el handle de la cámara del robot (el 'Vision_sensor')
error_cam, camara = sim.simxGetObjectHandle(clientID, 'Camara', sim.simx_opmode_oneshot_wait)
#Capturamos un cuadro  para activar la cámara y esperamos 1 segundo:
_, resolution, image = sim.simxGetVisionSensorImage(clientID, camara, 0, sim.simx_opmode_streaming)
time.sleep(1)


#-----------------Funcion para dibujar el contorno de las figuras -------------
def dibujar(mask,color):
    _,contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            cv2.circle(img, (x,y), 7, (0,255,0), -1)
            x,y,w,h = cv2.boundingRect(c)
            if color == (255,0,0):
                inputBuffer = bytearray()
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_1", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_1", [0],[],[], inputBuffer, sim.simx_opmode_blocking)    
                cv2.putText(img,'Color Azul', (x,y-15), font, 0.75,color,2,cv2.LINE_AA)
            if color == (0,255,255):
                inputBuffer = bytearray()
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_2", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_2", [0],[],[], inputBuffer, sim.simx_opmode_blocking)   
                cv2.putText(img,'Color Amarillo', (x,y-15), font, 0.75,color,2,cv2.LINE_AA)
            if color == (0,0,255):
                inputBuffer = bytearray()
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_3", [1],[],[], inputBuffer, sim.simx_opmode_blocking)
                res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "target", sim.sim_scripttype_childscript, "mover_3", [0],[],[], inputBuffer, sim.simx_opmode_blocking)   
                cv2.putText(img,'Color Rojo', (x,y-15), font, 0.75,color,2,cv2.LINE_AA)
            cv2.putText(img, '{},{}'.format(x,y),(x+35,y+45), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            cv2.drawContours(img, [nuevoContorno], 0, color, 3)

#---------------------- Rangos De colores a Detectar-------------------------
#---------------Color Azul------------------
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)
#--------------Color Rojo-------------------
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)
#--------------Color Amarillo-----------------
amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX  #Fuentes de letra

while (1):
    #------ Variable que controlan el Scrip en CoppeliaSim -------------------
    _, resolution, image = sim.simxGetVisionSensorImage(clientID, camara, 0, sim.simx_opmode_buffer) #Capturamos un cuadro de imaden de la cámara del robot. Guardamos la imagen y su resolución:

    #---------- Modificacion de imagen para el uso de Open ----------------------
    img = np.array(image, dtype = np.uint8) #La convertimos a un array de numpy
    img.resize([resolution[0], resolution[1], 3]) #Cambiamos sus dimensiones
    img = np.rot90(img,2) #La rotamos 90 grados para enderezarla
    img = np.fliplr(img) #La invertimos
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #Cambiamos su espacio de color de RGB a BGR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)
    _,cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #-----------------Funciones de OpenCv Para maskara del Espacio HSV--------------------------------------
    
    frameHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#Conversion de Imagen a HSV
    maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)#Seleccion del rango del color
    maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1) #Para encontrar los rangos de HSV
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskAzul,(255,0,0))
    dibujar(maskAmarillo,(0,255,255))
    dibujar(maskRed,(0,0,255))

    #------------------------- Visualizacion de imagen ---------------------------------
    cv2.imshow('img', img) #Visualizacion de imagen solo en el color Rojo
    #cv2.imshow('maskRed', maskRed)
    #----------------------------- Cierre de ventana--------------------------------------
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
cap.release()
cv2.destroyAllWindows()