import numpy as np
import mpu6050
import time
import matplotlib.pyplot as plt
import sys
import select


# Create a new Mpu6050 object






class Accelerometre:
    def __init__(self):
        self.time = time.time()
        self.mpu6050 = mpu6050.mpu6050(0x68)
        self.acc_x=0.   # Pour les 6 premiers, leurs valeurs seront écrasées immédiatement, sans avoir été utilisées.
        self.acc_y=0.
        self.acc_z=0.
        self.gyr_x=0.
        self.gyr_y=0.
        self.gyr_z=0.
        self.vit_x=0.
        self.vit_y=0.
        self.vit_z=0.
        self.pos_x=0.
        self.pos_y=0.
        self.pos_z=0.
        self.ang_x=0.
        self.ang_y=0.
        self.ang_z=0.
        self.heat=0.


    def _read_sensor_data(self):
        return self.mpu6050.get_accel_data(), self. mpu6050.get_gyro_data(), self.mpu6050.get_temp()

    def update(self,t1):
        data = self._read_sensor_data()

        # Update des accélérations.
        self.acc_x = data[0]["x"]
        self.acc_y = data[0]["y"]
        self.acc_z = data[0]["z"]
        # Update des vitesses angulaires.
        self.gyr_x = data[1]["x"]
        self.gyr_y = data[1]["y"]
        self.gyr_z = data[1]["z"]

        # Vitesses linéaires
        self.vit_x = self._calculate_vitesse(t0=self.time,t1=t1,acc_1=self.acc_x,v0=self.vit_x)
        self.vit_y = self._calculate_vitesse(t0=self.time,t1=t1,acc_1=self.acc_y,v0=self.vit_y)
        self.vit_z = self._calculate_vitesse(t0=self.time,t1=t1,acc_1=self.acc_z,v0=self.vit_z)

        # Positions linéaires
        self.pos_x = self._calculate_position(t0=self.time,t1=t1,v1=self.vit_x,p0=self.pos_x)
        self.pos_y = self._calculate_position(t0=self.time,t1=t1,v1=self.vit_y,p0=self.pos_y)
        self.pos_z = self._calculate_position(t0=self.time,t1=t1,v1=self.vit_z,p0=self.pos_z)

        # Angles
        self.ang_x = self._calculate_angle(t0=self.time,t1=t1,w1=self.gyr_x,a0=self.ang_x)
        self.ang_y = self._calculate_angle(t0=self.time,t1=t1,w1=self.gyr_y,a0=self.ang_y)
        self.ang_z = self._calculate_angle(t0=self.time,t1=t1,w1=self.gyr_z,a0=self.ang_z)
        
        acc = [self.acc_x, self.acc_y, self.acc_z]
        gyr = [self.gyr_x, self.gyr_y, self.gyr_z]
        vit = [self.vit_x, self.vit_y, self.vit_z]
        pos = [self.pos_x, self.pos_y, self.pos_z]
        ang = [self.ang_x, self.ang_y, self.ang_z]

        # On update self.time
        self.time = t1
        return acc, gyr, vit, pos, ang

    def _calculate_vitesse(self,t0, t1, acc_1, v0) -> float: 
        return v0 + acc_1*(t1-t0)

    def _calculate_position(self,t0, t1, v1, p0) -> float:
        return p0 + v1*(t1-t0)
    
    def _calculate_angle(self,t0, t1, w1, a0) -> float:
        return a0 + w1*(t1-t0)      # a1 est l'angle0
    
    def _calculate_angle_acc(self,t0, t1, w0, w1) -> float:
        return (w1-w0)/(t1-t0)
    

accelero_1 = Accelerometre()



def check_input():
    # Retourne True si une entrée est disponible dans stdin
    return select.select([sys.stdin], [], [], 0)[0]



def data_generator(N):
    accelerations = []
    gyros = []
    vitesses = []
    positions = []
    angles = []


    while len(accelerations) < N:
        donnees_instant = accelero_1.update(t1=time.time())
        accelerations.append(donnees_instant[0])
        gyros.append(donnees_instant[1])
        vitesses.append(donnees_instant[2])
        positions.append(donnees_instant[3])
        angles.append(donnees_instant[4])
    
    accelerations = np.array(accelerations)
    gyros = np.array(gyros)
    vitesses = np.array(vitesses)
    positions = np.array(positions)
    angles = np.array(angles)
    return accelerations, gyros, vitesses, positions, angles
           

data_generator(1e4)