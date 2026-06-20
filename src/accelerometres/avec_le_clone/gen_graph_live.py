import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


import mpu6050
import time

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()
    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()
    # Read temp
    temperature = mpu6050.get_temp()
    return accelerometer_data, gyroscope_data, temperature

fig_acc, ax_acc = plt.subplots(1,3)
fig_gyro, ax_gyro = plt.subplots(1,3)
ax1, ax2, ax3 = ax_acc
ax4, ax5, ax6 = ax_gyro
line1_acc, line2_acc, line3_acc = ax1.plot([], []), ax2.plot([], []), ax3.plot([], [])
line1_gyro, line2_gyro, line3_gyro = ax4.plot([], []), ax5.plot([], []), ax6.plot([], [])

def init():
    for ax in ax_acc:
        ax.set_ylim(-15,15)
    for ax in ax_gyro:
        ax.set_ylim(-360, 360)
    return line1_acc, line2_acc, line3_acc, line1_gyro, line2_gyro, line3_gyro

temps = []
acc_x, acc_y, acc_z = [], [], []            # accélérations [m/s^2]
w_x, w_y, w_z = [], [], []                  # Vitesses angulaires w [degrés/s]
compteur=0
time_delta = 0.1

def update(frame):
    instant_data = read_sensor_data()
    acc_data, gyro_data, temperature = instant_data
    # Update des accélérations
    acc_x.append(acc_data[0]["x"])
    acc_y.append(acc_data[0]["y"])
    acc_z.append(acc_data[0]["z"])
    # Update des vitesses angulaires
    w_x.append(gyro_data[0]["x"])
    w_y.append(gyro_data[0]["y"])
    w_z.append(gyro_data[0]["z"])
    temps.append(compteur*time_delta)
    compteur += 1

    # Update les plots
    line1_acc.set_data(temps, acc_x)
    line2_acc.set_data(temps, acc_y)
    line3_acc.set_data(temps, acc_z)
    line1_gyro.set_data(temps, w_x)
    line2_gyro.set_data(temps, w_y)
    line3_gyro.set_data(temps, w_z)

    return line1_acc, line2_acc, line3_acc, line1_gyro, line2_gyro, line3_gyro

ani_acc = animation.FuncAnimation(
    fig_acc, update, init_func=init,
    interval=1000*time_delta, 
    blit=False
)


ani_gyro = animation.FuncAnimation(
    fig_gyro, update, init_func=init,
    interval=1000*time_delta,
    blit=False
)


fig_acc.tight_layout()
fig_gyro.tight_layout()

fig_acc.show()
fig_gyro.show()
# fig_acc.savefig("acceleration_live.png")
# fig_gyro.savefig("vitesses_angulaires_live.png")
ani_acc.save("acceleration_live.gif", writer="pillow")
ani_gyro.save("vitesses_angulaires_live.gif", writer="pillow")

