import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams["figure.figsize"] = (9,4)
from functions import difraccion, interferencia, wavelength_to_rgb, int_dif

from pyodide import create_proxy

def setup_1():
    a = 4e-6
    L = 1
    lam0 = 400e-9
    x_lim = 4*lam0*L/a
    x = np.linspace(-x_lim, x_lim, 100000)
    Element("consta").write(f"L = {L} m <br />a = {int(a*1e6)} μm")
    return L,a,x,x_lim

def plot_1(fig, ax, lam1, lam2, L, a, x, x_lim):
    print(f"{a=}")
    Element("lam1_txt").write(f"{lam1} nm")
    Element("lam2_txt").write(f"{lam2} nm")

    ax.clear()    

    y = difraccion(x, lam1*1e-9, L, a)
    y2 = difraccion(x, lam2*1e-9, L, a)
    color1 = wavelength_to_rgb(lam1)
    color2 = wavelength_to_rgb(lam2)
    ax.plot(x,y, color=color1, label=f"$\lambda$ = {lam1} nm")
    ax.plot(x,y2, color=color2, label=f"$\lambda$ = {lam2} nm")

    loc = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.set_ylim(0,1)
    ax.set_xlim(-x_lim, x_lim)
    # ax.set_xlabel('sen(θ)')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('Intensidad')
    ax.legend()

    Element("viz").write(fig)
    

input_elements = document.getElementsByName("lam")

@create_proxy
def change_lambda(event):
    lam1, lam2 = [int(el.value) for el in input_elements]
    plot_1(fig, ax, lam1, lam2, *const_1)

for ele in input_elements:
    ele.addEventListener("change", change_lambda)

fig, ax = plt.subplots(layout='tight')
const_1 = setup_1()
plot_1(fig, ax, 400, 500, *const_1)

#################################
def setup_2():
    L = 1
    d = 30e-6
    a = 6e-6
    lam = 600 *1e-9
    x_lim = 2.2*lam*L/a
    x = np.linspace(-x_lim, x_lim, 100_000)
    Element("constb").write(f"L = {L} m <br/> a = {int(a*1e6)} μm<br/>d = {int(d*1e6)} μm")
    return L, a, d, x, x_lim

def plot_2(fig2, ax3, ax4, lam, N, L, a, d, x, x_lim):
       
    Element("N_txt").write(f"{N}")
    Element("lam22_txt").write(f"{lam} nm")

    ax3.clear()  
    ax4.clear()  

    y = int_dif(x, lam*1e-9, L, a, d, N)
    color = wavelength_to_rgb(lam)

    ax3.plot(x,y, color=color)
    ax3.margins(x=0)
    loc = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals
    ax3.xaxis.set_major_locator(loc)
    ax3.set_ylim(0,1)
    # ax3.set_xlabel('sen(θ)')
    ax.set_xlabel('x (m)')
    ax3.set_ylabel('Intensidad')
    height = 1
    image = np.tile(y, (height,1))

    colors = [
        (0,0,0),
        color,
    ]
    cmap = LinearSegmentedColormap.from_list("simple", colors)

    ax4.imshow(image, cmap=cmap, aspect="auto", extent=[-x_lim, x_lim, -1,1] )
    ax4.set_xlabel('sen(θ)')
    ax4.yaxis.set_visible(False)
    Element("vizb").write(fig2)


input2_elements = document.getElementsByName("params2")

@create_proxy
def change_params2(event):
    N, lam = [int(el.value) for el in input2_elements]
    plot_2(fig2, ax3, ax4, lam, N, *const_2)

for ele in input2_elements:
    ele.addEventListener("change", change_params2)


fig2, (ax3, ax4) = plt.subplots(2, 1, layout='tight')
fig2.set_size_inches(10, 8)
fig2.canvas.header_visible = False
    
const_2 = setup_2()
plot_2(fig2, ax3, ax4, 600, 5, *const_2)

##############


fig3, ax5 = plt.subplots(layout='tight')


L = 1
N = 6000        # lineas/cm
d = 1/N *1e-2   # metros
# a = d/10
l_inf = 480 *1e-9
l_sup = 650 *1e-9

x_lim = 3.2*l_sup*L/d
x = np.linspace(-x_lim, x_lim, 100_000)

# wv = 440 *1e-9
# waves = np.linspace(wv, wv*1.01, 40)

waves = np.linspace(l_inf, l_sup, 100)
for wave in waves:
    i = interferencia(x, wave, L, d, N)
    ax5.plot(x, i, label=f'{wave*1e9:.0f} nm', color=wavelength_to_rgb(wave*1e9))

# ax.legend()
# loc = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals
# ax.xaxis.set_major_locator(loc)
ax5.set_xlabel('x (m)')
ax5.set_ylabel('Intensidad')

Element("vizc").write(fig3)
