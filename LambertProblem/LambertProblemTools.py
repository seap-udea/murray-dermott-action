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
    
    @staticmethod
    def getFocus(center1, center2, radio1, radio2):
        r1 = radio1
        r2 = radio2

        c1 = np.array(center1)
        c2 = np.array(center2)

        d = ((c2[0]-c1[0])**2 + (c2[1] - c1[1])**2)**(1/2)
        a = (r1**2 - r2**2 + d**2)/(2*d)

        dx = (c2[0] - c1[0])/d
        dy = (c2[1] - c1[1])/d

        px = c1[0] + a*dx
        py = c1[1] + a*dy

        h = (r1**2 - a**2)**(1/2)

        p1_x = px + h*dy
        p1_y = py - h*dx

        p2_x = px - h*dy
        p2_y = py + h*dx

        point1 = [p1_x, p1_y]
        point2 = [p2_x, p2_y]

        return point1, point2
    






