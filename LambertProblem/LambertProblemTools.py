#clase que genera una elipse centrada en el origen con los focos sobre el eje x
import numpy as np

class elipse(): 
    a = 1
    
    def __init__(self, a, e = None, b = None): ##crear el constructor con 
        
        if e != None:  
            self.a = a
            self.e = e
            self.b = self.a*(1-self.e**2)**(1/2)  #minor semi axis 
            self.c = (self.a**2 - self.b**2)**(1/2)  #focus distance 
            

        elif b != None: 
            self.a = a
            self.b = b
            self.e = (1 - self.b**2/self.a**2)**(1/2)  
            self.c = (self.a**2 - self.b**2)**(1/2)    

    @classmethod #usar esto para crear las elipses que están desplazadas del origen o rotadas 
    def elipse_desplazada(cls, x, y):
        return 
            

#---propiedades-----------------------------------------------------------------
    

#---comportamiento---------------------------------------------------------------
    #calcular puntos de la elipse: 
    def GetElipse(self):

        theta = np.linspace(0,2*np.pi,200)
        elipsex = self.a*np.cos(theta)
        elipsey = self.b*np.sin(theta)

        elipse_positions = np.zeros((200,2))
        elipse_positions[:,0] = elipsex
        elipse_positions[:,1] = elipsey

        return elipse_positions




