import numpy as np
import matplotlib.pyplot as plt

from spiceypy import rotate
from scipy.integrate import solve_ivp


class Crtbp():
    def __init__(self, X0, mu):
        self.X0 = X0
        self.x0 = X0[0]
        self.y0 = X0[1]
        self.z0 = X0[2]
        self.vx0 = X0[3]
        self.vy0 = X0[4]
        self.vz0 = X0[5]
        self.mu = mu
        self.jacobi = Crtbp.get_Jacobi(self.X0, self.mu)
        self.tisserand = Crtbp.get_tisserand(self.X0, self.mu)
        self.R_hill = Crtbp.get_RHill(self.mu)
        self.LagrangePoints = Crtbp.Lagrange(self.mu)

    def __Equation_of_motion(self, t, X, mu):
        """ Equations of motion in the CRTBP

        Args:
            Y (list): State vector of the system  [x,y,z,vx,vy,vz]
            t (float): Time of integration (only used to propagation)
            mu (float): mass ratio (m2)/(m1+m2)

        Returns:
            dy/dt (list): Analytic time derivative of state vector 
        """
        x, y, z, vx, vy, vz = X
        mu1 = 1-mu
        mu2 = mu
        r1 = np.sqrt((x+mu2)**2 + y**2+z**2)
        r2 = np.sqrt((x-mu1)**2 + y**2+z**2)

        mu_r1 = mu1/(r1**3)
        mu_r2 = mu2/(r2**3)

        ax = 2*vy+x-(x+mu2)*mu_r1-(x-mu1)*mu_r2
        ay = -2*vx+y - (mu_r1+mu_r2)*y
        az = -(mu_r1+mu_r2)*z

        return [vx, vy, vz, ax, ay, az]

    def propagate(self, t, dt=200):
        """
        Numerical propagation to the  Circular Restriced Three Body Problem  
        Arguments:
            t: Time of Integration 
            dt: intervals between t
        Returns:
            X: numpy array of shape (6,dt) with test particle's position in each time
            T: array with evaluations time
        """

        X_synodic = solve_ivp(self.__Equation_of_motion, y0=self.X0, t_span=[0, t], t_eval=np.linspace(0, t, dt),
                              atol=1e-9, rtol=1e-9, args=(self.mu,))

        X = X_synodic.y
        T = X_synodic.t
        return X, T

    def plot_trayectory(self, t, dt=200, inertial=False, Lagrange=False, zero_curve=False, **args):

        Lagrange = self.Lagrange(self.mu)
        plot_3 = plot_L3 = plot_L45 = False
        D = 2
        if inertial:
            args['nrows'] = 1
            args['ncols'] = 2

        if self.z0 != 0 or self.vz0 != 0:
            args["subplot_kw"] = {'projection': '3d'}
        fig, (axs) = plt.subplots(**args)

        X, T = self.propagate(t, dt)
        R1, R2, X_I = Crtbp.Syn2Ine(X, T, self.mu)

        if Lagrange:
            ax = axs if not inertial else axs[0]
            ax.plot(self.LagrangePoints[0], 0, 'k+')
            ax.plot(self.LagrangePoints[1], 0, 'k+')

            if min(X[0, :]) < 0:
                ax.plot(self.LagrangePoints[2], 0, 'k+')

            if max(abs(X[1, :])) > np.sqrt(3)/2:
                ax.plot(self.LagrangePoints[3][0],
                        self.LagrangePoints[3][1], 'k+')
                ax.plot(self.LagrangePoints[4][0],
                        self.LagrangePoints[4][1], 'k+')

        if zero_curve:
            if self.z0 != 0 and self.vz0 != 0:
                raise UserWarning(
                    'Cannot generate Zero velocity curve in three dimension plots')
            else:
                x = np.linspace(-1.5, 1.5, 100)
                y = np.linspace(-1.5, 1.5, 100)
                X_mesh, Y_mesh = np.meshgrid(x, y)

                mu1 = 1-self.mu
                mu2 = self.mu

                r1 = np.sqrt((X_mesh+mu2)**2+Y_mesh**2)
                r2 = np.sqrt((X_mesh-mu1)**2+Y_mesh**2)
                CJ = X_mesh**2+Y_mesh**2+2*(mu1/r1+mu2/r2)

                ax = axs if not inertial else axs[0]

                ax.contourf(X_mesh, Y_mesh, CJ,
                            levels=[-100, self.jacobi], colors='k', alpha=0.3)

        if inertial:
            if "subplot_kw" in args.keys():
                axs[0].plot(X[0, :], X[1, :], X[2, :], 'k-')
                axs[0].plot(1-self.mu, 0, 'bo', markersize=3)
                axs[0].plot(self.mu, 0, 'ro', markersize=3)
                axs[0].set_xlabel('x')
                axs[0].set_ylabel('y')
                axs[0].set_zlabel('z')
                axs[1].plot(X_I[0, :], X_I[1, :], X_I[2, :], 'k-')
                axs[1].plot(R1[0, :], R1[1, :], R1[2, :], 'b--', alpha=0.5)
                axs[1].plot(R2[0, :], R2[1, :], R2[2, :], 'r--', alpha=0.5)
                axs[1].set_xlabel('x')
                axs[1].set_ylabel('y')
                axs[1].set_zlabel('z')

            else:
                axs[0].plot(X[0, :], X[1, :], 'k-')
                axs[0].plot(1-self.mu, 0, 'bo', markersize=3)
                axs[0].plot(self.mu, 0, 'ro', markersize=3)
                axs[0].set_xlabel('x')
                axs[0].set_ylabel('y')
                axs[1].plot(X_I[0, :], X_I[1, :], 'k-')
                axs[1].plot(R1[0, :], R1[1, :], 'r--', alpha=0.5)
                axs[1].plot(R2[0, :], R2[1, :], 'b--', alpha=0.5)
                axs[1].set_xlabel('x')
                axs[1].set_xlabel('y')
        else:
            axs.plot(X[0, :], X[1, :], 'k--')
            axs.plot(1-self.mu, 0, 'bo', markersize=3)
            axs.plot(self.mu, 0, 'ro', markersize=3)
            axs.set_xlabel('x')
            axs.set_ylabel('y')

        plt.show()

    @staticmethod
    def get_Jacobi(X, mu):
        """ Get the Jacobi integral for a given state to the Circular Restricted Three Body Problem

        Args:
            X (list): State Vector [x,y,z,vx,vy,vz]
            mu (_type_): mass ratio (m2/(m1+m2))

        Returns:
            Float: Jacobi Integral preserved during the motion
        """
        x, y, z, vx, vy, vz = X
        mu1 = 1-mu
        mu2 = mu

        r1 = np.sqrt((x+mu2)**2+y**2 + z**2)
        r2 = np.sqrt((x-mu1)**2+y**2 + z**2)

        CJ = x**2+y**2+2*(mu1/r1+mu2/r2) - vx**2 - vy**2 - vz**2

        return CJ

    @staticmethod
    def Lagrange(mu, point=0):
        """ Locations of System's Lagrange Points 

        Args:
            mu (int): mass ratio m2/(m1+m2)

        Returns:
            L1: x component of Lagrange Point L1 (colinear)
            L2: x component of Lagrange Point L2 (colinear)
            L3: x component of Lagrange Point L3 (colinear)
            L4: [x,y] components of Lagrange Point L4 (y > 0)
            L5: [x,y] components of Lagrange Point L5 (y < 0)
        """

        if point not in [0, 1, 2, 3, 4, 5]:
            raise TypeError('Not valid point')

        mu1 = 1 - mu
        mu2 = mu
        alpha = (mu2/(3*mu1))**(1/3)

        L1 = mu1 - (alpha - (alpha**2)/3 - (alpha**3)/9-(alpha**4)*(23/81))

        L2 = mu1 + (alpha + (alpha**2)/3 - (alpha**3)/9-(alpha**4)*(31/81))
        mu2mu1 = mu2/mu1
        L3 = -mu2 - 1 - (-(7/12)*(mu2mu1)+(7/12)*((mu2mu1)**2) -
                         (13223/20736)*((mu2mu1)**3))
        L4 = 1/2 - mu2
        Lagranges = L1, L2, L3, [L4, np.sqrt(3)/2], [L4, -np.sqrt(3)/2]

        return Lagranges if point == 0 else Lagranges[point-1]

    @staticmethod
    def get_tisserand(X, mu):
        Y_inertial = Crtbp.Syn2Ine(X, [0], mu)[2]
        hcos = np.dot(Y_inertial[3:, 0], np.cross(
            [0, 0, 1], Y_inertial[:3, 0]))
        velocity_m = np.linalg.norm(Y_inertial[3:, 0], axis=0)
        position_m = np.linalg.norm(Y_inertial[:3, 0], axis=0)
        tisserand = hcos+(1/2)*(2/position_m-velocity_m**2)
        return tisserand

    @staticmethod
    def __potential_derivatives(mu, L):

        x0, y0 = Crtbp.Lagrange(mu, point=L) if type(Crtbp.Lagrange(mu, point=L)
                                                     ) == list else [Crtbp.Lagrange(mu, point=L), 0]
        mu1 = 1 - mu
        mu2 = mu
        r10 = np.sqrt((x0+mu2)**2 + y0**2)
        r20 = np.sqrt((x0-mu1)**2 + y0**2)
        A = mu1/r10**3 + mu2/r20**3
        B = 3*(mu1/r10**5 + mu2/r20**5)*y0**2
        C = 3*(mu1*(x0+mu2)/r10**5 + mu2*(x0-mu1)/r20**5)*y0
        D = 3*((mu1*(x0+mu2)**2)/r10**5 + (mu2*(x0-mu1)**2)/r20**5)

        Uxx = 1 - A + D
        Uyy = 1 - A + B
        Uxy = C
        return Uxx, Uyy, Uxy

    @staticmethod
    def __eigenvalues_Lagrange(Uxx, Uyy, Uxy):

        aux1 = (1/2)*(Uxx+Uyy-4)
        aux2 = (1/2)*np.sqrt((4-Uxx-Uyy)**2 - 4*(Uxx*Uyy-Uxy**2 + 0j))
        eigen1, eigen2, = np.sqrt(
            aux1 - aux2 + 0j), - np.sqrt(aux1 - aux2 + 0j)
        eigen3, eigen4 = np.sqrt(
            aux1 + aux2 + 0j), - np.sqrt(aux1 + aux2 + 0j)
        eigens = np.array([eigen1, eigen2, eigen3, eigen4])
        return eigens

    @staticmethod
    def __Linear_Coefficients(X0, V0, mu, L):
        Uxx, Uyy, Uxy = Crtbp.__potential_derivatives(mu, L)
        eigens = Crtbp.__eigenvalues_Lagrange(Uxx, Uyy, Uxy)
        betas = (eigens**2-Uxx)/(2*eigens+Uxy)
        coefficients = np.array(
            [[1, 1, 1, 1], eigens, betas, betas*eigens])
        IC = np.zeros(4)
        IC[:2] = X0
        IC[2:] = V0
        alpha = np.linalg.solve(coefficients, IC)
        beta = alpha*betas
        return alpha, beta, eigens

    @staticmethod
    def stability(X0, V0, mu, L, eigenvalues=False):
        """ Analysis of Lagrange point stablility respect to an initial planar perturbation 
            with position X and velocity V
        X = x(lagrange)
        Args:
            X0 (list): position of perturbation respect Lagrange point [x0,y0] 
                where x = x(lagrange) * x0 and y = y(lagrange) * y0
            V0 (list): velocity of perturbation respect Lagrange point [vx0,vy0] 
            mu (_type_): mass ratio (m2)/(m1+m2)
            L (_type_): Lagrange Point
            eigenvalues (bool, optional): If True, return the eigenvalues of equation of motion 
                matrix respect perturbation, if the values are real the point is unstable. Defaults to False.

        Returns:
            x,y (function): Propagation functions of perturbation in x and y direction
        """

        alpha, beta, eigens = Crtbp.__Linear_Coefficients(X0, V0, mu, L)

        def x(t): return np.sum(alpha*np.exp(eigens*t))
        def y(t): return np.sum(beta*np.exp(eigens*t))

        if L == 1 or L == 2 or L == 3 or mu > (27-np.sqrt(621))/(54):
            print('Unstable point')
        if eigenvalues:
            return np.vectorize(x), np.vectorize(y), eigens

        return np.vectorize(x), np.vectorize(y)

    @staticmethod
    def Syn2Ine(X_synodic, t_span, mu):
        """
        Transformation between rotational (synodic) frame to inertial frame
        Arguments:
            X_synodic: Positional vector in rotational frame [x,y,z,vx,vy,vz]
            t_span: Time array
        Returns:
            r1: numpy array with shape (dt,3). Position x,y,z of main body with mass m1
            r2: numpy array with shape (dt,3). Position x,y,z of secondary body with mass m3
            Y_inertial: numpy array with shape (dt,6). Position x,y,z,vx,vy,vz to test Particle

        """
        try:
            X_synodic.shape[1]
        except:
            X_synodic = np.array(X_synodic).reshape((6, 1))

        Y_inertial = np.zeros(X_synodic.shape)

        # Vectors of main and secondary body
        r1 = np.zeros_like((X_synodic[:3, :]))
        r2 = np.zeros_like((X_synodic[:3, :]))
        for i in range(len(t_span)):
            R = rotate(-t_span[i], 3)
            r_i = np.matrix(X_synodic[:3, i])
            v_i = np.matrix(X_synodic[3:, i])
            Y_inertial[:3, i] = (R*r_i.T).T
            Y_inertial[3:, i] = (R*(v_i + np.cross([0, 0, 1], r_i)).T).T
            r1[:, i] = -mu * \
                np.array([np.cos(t_span[i]), np.sin(t_span[i]), 0])
            r2[:, i] = (1-mu) * \
                np.array([np.cos(t_span[i]), np.sin(t_span[i]), 0])
        return r1, r2, Y_inertial

    @staticmethod
    def Ine2Syn(X_inertial, t_span):
        """
        Transformation between inertial frame to rotational (synodic) frame t
        Arguments:
            X_inertial: Positional vector in inertial frame [x,y,z,vx,vy,vz]
            t_span: Time array
        Returns:
            r1: numpy array with shape (dt,3). Position x,y,z of main body with mass m1
            r2: numpy array with shape (dt,3). Position x,y,z of secondary body with mass m3
            Y_inertial: numpy array with shape (dt,6). Position x,y,z,vx,vy,vz to test Particle

        """

        if not isinstance(X_inertial, np.ndarray):
            X_inertial = np.array(X_inertial).reshape((6, 1))

        X_synodic = np.zeros(X_inertial.shape)

        for i in range(X_inertial.shape[1]):
            R = rotate(t_span[i], 3)
            r_i = np.matrix(X_inertial[:3, i])
            v_i = np.matrix(X_inertial[3:, i])
            X_synodic[:3, i] = (R*r_i.T).T
            X_synodic[3:, i] = (R*(v_i - np.cross([0, 0, 1], r_i)).T).T

        return X_synodic

    @staticmethod
    def get_RHill(mu):
        """Radius of the The Hill sphere of an astronomical body. The hill sphere
         is the region in which it dominates the attraction of satellites.

        Args:
            mu (float): mass ratio (m2)(m1+m2) 

        Returns:
            Rh (float): Hill radius
        """
        return (mu/3)**(1/3)


if __name__ == "__main__":
    X0 = np.array([1.1, 0, 0, -0.1, 0.2, 0])
    t = 30
    mu = 0.02
    dt = 400
    system = Crtbp(X0, mu)
    system.plot_trayectory(t, 800, inertial=True)
