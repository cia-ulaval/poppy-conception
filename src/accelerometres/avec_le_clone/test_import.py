import mpu6050
import time
import numpy as np
import matplotlib.pyplot as plt

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()
    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()
    # Read temp
    temperature = mpu6050.get_temp()
    return accelerometer_data, gyroscope_data, temperature


temps = np.arange(0,5,0.1)
accelero_data_x = []
accelero_data_y = []
accelero_data_z = []
gyro_data_x, gyro_data_y, gyro_data_z = [], [], []
temp_data = []



for i in range(50):
# IL FAUDRA  MODIFIER POUR QUE CE SOIT UN while True ÉVENTUELLEMENT. cAR IL FAUDRA CONSTAMMENT LIRE LE DATA DE L'ACCÉLÉROMÈTRE.
    # Read the sensor data
    data = read_sensor_data()
    accelero_data_x.append(data[0]["x"])
    accelero_data_y.append(data[0]["y"])
    accelero_data_z.append(data[0]["z"])
    gyro_data_x.append(data[1]["x"])
    gyro_data_y.append(data[1]["y"])
    gyro_data_z.append(data[1]["z"])
    temp_data.append(data[2])

    # Print the sensor data
    print("Accelerometer data:", data[0])
    print("Gyroscope data:", data[1])
    print("Temp:", data[2])

    # Wait for 1 second
    time.sleep(0.1)

fig, axes = plt.subplots(1,3)
ax1, ax2, ax3 = axes
ax1.plot(temps, accelero_data_x)
ax2.plot(temps, accelero_data_z)
ax3.plot(temps, accelero_data_y)
for ax in axes:
    ax.set_ylim(-15, 15)
ax1.set_ylabel("position en x")
ax2.set_ylabel("position en y")
ax3.set_ylabel("position en z")

fig2, axes2 = plt.subplots(1,3)
ax4,ax5,ax6 = axes2
ax4.plot(temps, gyro_data_x)
ax5.plot(temps, gyro_data_y)
ax6.plot(temps, gyro_data_z)

for ax in axes2:
    ax.set_ylim(-360, 360)

plt.tight_layout()
fig.savefig("acceleration.png")
fig2.savefig("vitesses_angulaires.png")
# plt.show()

