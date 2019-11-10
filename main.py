import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from itertools import cycle
import matplotlib.colors as clr

colorpoints = [(1-(1-q)**4, c) for q, c in zip(np.linspace(0, 1, 20),
                                               cycle(['#ffff88', '#000000',
                                                      '#ffaa00',]))]
cmap = clr.LinearSegmentedColormap.from_list('mycmap',
                                             colorpoints, N=2048)

rc('animation', html='html5')

fig = plt.figure(figsize=(10, 10))
max_frames = 1
max_zoom = 10000
rmin, rmax, imin, imax = -2.5, 1.5, -2, 2

images = []


def mandelbrot(rmin, rmax, rpoints, imin, imax, ipoints,
               max_iterations=300, infinity_border=10):
    image = np.zeros((rpoints, ipoints))
    r, i = np.mgrid[rmin:rmax:(rpoints * 1j), imin:imax:(ipoints * 1j)]
    c = r + 1j * i
    z = np.zeros_like(c)
    for k in range(max_iterations):
        z = z ** 2 + c
        mask = (np.abs(z) > infinity_border) & (image == 0)
        image[mask] = k
        z[mask] = np.nan
    return -image.T


def init():
    return plt.gca()


def animate(i):
    if i > max_frames // 2:
        plt.imshow(images[max_frames // 2 - i], cmap='flag')
        print(i)
        return

    r_center, i_center = -0.793191078177363, 0.26093721735804
    zoom = (i / max_frames * 2) ** 3 * max_zoom + 1
    scalefactor = 1 / zoom
    rmin_ = (rmin - r_center) * scalefactor + r_center
    imin_ = (imin - i_center) * scalefactor + i_center
    rmax_ = (rmax - r_center) * scalefactor + r_center
    imax_ = (imax - i_center) * scalefactor + i_center
    image = mandelbrot(rmin_, rmax_, 500, imin_, imax_, 500)
    plt.imshow(image, cmap=cmap, interpolation='none')
    images.append(image)
    print("Frame {} created".format(i))
    return plt.gca()


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=max_frames, interval=150)
anim.save('test2.gif', writer='imagemagick')
