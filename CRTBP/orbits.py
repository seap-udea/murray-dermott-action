import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from spiceypy import rotate,mxv
from scipy.integrate import odeint
import matplotlib.animation as animation

def CRTBP(Y0,t,alpha,dt = 100):
    """
    Numerical solution to Circular Restriced Three Body Problem
    Input:
    Y: Positional vector [x,y,z,vx,vy,vz]
    t: Time of Integration 
    alpha: Parameter m2/(m1+m2)
    """
    def equation(Y,t):
        x,y,z,vx,vy,vz = Y
        mu1 = 1-alpha
        mu2 = alpha
        r1 = np.sqrt((x+mu2)**2 + y**2+z**2)
        r2 = np.sqrt((x-mu1)**2 + y**2+z**2)
        
        mu_r1 = mu1/(r1**3)
        mu_r2 = mu2/(r2**3)

        ax = 2*vy+x-(x+mu2)*mu_r1-(x-mu1)*mu_r2
        ay = -2*vx+y - (mu_r1+mu_r2)*y
        az = -(mu_r1+mu_r2)*z
        
        return [vx, vy, vz, ax, ay, az]

    ts = np.linspace(0,t,dt)

    Yrot = odeint(equation,y0=Y0,t = ts,
                  atol = 1e-10,rtol =1e-10,mxstep=1000)
    return Yrot

Y0 = np.array([1.1,0,0,-0.1,0.2,0])
t = 30
mu = 0.02
dt = 1000
Yrot = CRTBP(Y0,t,mu,dt)


def CRTBP_inertial(Yrot,t,dt):
    ts = np.linspace(0,t,dt)
    YStatic = np.zeros_like(Yrot)
    R1 = np.zeros_like(Yrot[:,:3])
    R2 = np.zeros_like(Yrot[:,:3])

    for i in range(YStatic.shape[0]):
    
        RMatrix = rotate(-ts[i],3)
        YStatic[i][:3] = mxv(RMatrix,Yrot[i][:3].T)
        YStatic[i][3:] = mxv(RMatrix,Yrot[i][3:]+np.array([-Yrot[i][1],Yrot[i][0],0]))
        
        R1[i] = -mu * np.array([np.cos(ts[i]),np.sin(ts[i]),0])
        R2[i] = (1-mu) * np.array([np.cos(ts[i]),np.sin(ts[i]),0])
    return R1,R2,YStatic

r1, r2, YStatic = CRTBP_inertial(Yrot,t,dt)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), tight_layout=True)


def graph_orbit(ti):
    global  Yrot, YStatic
    ax1.cla()
    ax2.cla()
    ax1.plot(YStatic[ti,0],YStatic[ti,1],'bo')
    ax1.plot(YStatic[:ti,0],YStatic[:ti,1],'b--')
    ax1.plot(r1[ti,0],r1[ti,1],'ro')
    ax1.plot(r2[ti,0],r2[ti,1],'go')
    ax1.set_xlim(min(YStatic[:,0]),max(YStatic[:,0]))
    ax1.set_ylim(min(YStatic[:,1]),max(YStatic[:,1]))

    ax2.plot(Yrot[ti,0],Yrot[ti,1],'bo')
    ax2.plot(Yrot[:ti,0],Yrot[:ti,1],'b--')
    ax2.plot(mu,0,'ro')
    ax2.plot(1-mu,0,'go')
    ax2.set_xlim(min(Yrot[:,0]),max(Yrot[:,0]))
    ax2.set_ylim(min(Yrot[:,1]),max(Yrot[:,1]))



anim = animation.FuncAnimation(fig, graph_orbit,frames = np.arange(dt), blit=False, interval=1,
                              repeat=True) 
plt.show()