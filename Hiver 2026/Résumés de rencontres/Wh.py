import numpy as np
import matplotlib.pyplot as plt


def temps(Wh, W=60):
    sec = Wh*3600 / W
    minutes = sec/60
    heures = sec/3600
    return (Wh, sec, minutes, heures)


for énergie in range(10, 100, 10):
    print(temps(énergie, W=70))

print(temps(Wh = 10000*12/1000, W=60))
