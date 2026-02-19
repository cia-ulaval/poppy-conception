import numpy as np
import matplotlib.pyplot as plt


def temps(Wh, W=60):
    Wh = 0.8 * Wh
    sec = Wh*3600 / W
    minutes = sec/60

    return f"Pour {round(Wh,2)} Wh, ça donnerait {round(minutes,2)} minutes à décharger la batterie à {W} watts"


print(temps(Wh=4000*12/1000))



