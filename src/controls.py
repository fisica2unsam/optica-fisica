import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams["figure.figsize"] = (9,4)
from functions import difraccion, interferencia, wavelength_to_rgb, int_dif
import js
from pyscript import Element

# from pyodide import create_proxy
from pyodide.ffi import create_proxy

def num(n):
    try:
        x = int(n)
    except ValueError:
        x = float(n)
    return x

LOC = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals

def setup_1():
    x_lim = 0.4
    x = np.linspace(-x_lim, x_lim, 100000)
    return x,x_lim

def plot_1(fig, ax, lam1, lam2, L, a, x, x_lim):
    ax.clear()    

    y = difraccion(x, lam1*1e-9, L, a*1e-6)
    y2 = difraccion(x, lam2*1e-9, L, a*1e-6)
    color1 = wavelength_to_rgb(lam1)
    color2 = wavelength_to_rgb(lam2)
    ax.plot(x,y, color=color1, label=f"$\lambda$ = {lam1} nm")
    ax.plot(x,y2, color=color2, label=f"$\lambda$ = {lam2} nm")

    ax.xaxis.set_major_locator(LOC)
    ax.set_ylim(0,1)
    ax.set_xlim(-x_lim, x_lim)
    # ax.set_xlabel('sen(θ)')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('Intensidad')
    ax.legend()

    Element("viz").write(fig)
    

input_elements = js.document.getElementsByName("params1")

@create_proxy
def change_lambda(event):
    L, a, lam1, lam2 = [num(el.value) for el in input_elements]
    Element("L1_txt").write(f"L = {L:.2f} m")
    Element("a1_txt").write(f"a = {a:.2f} μm")
    Element("lam1_txt").write(f"λ₁ = {lam1} nm")
    Element("lam2_txt").write(f"λ₂ = {lam2} nm")
    plot_1(fig, ax, lam1, lam2, L, a, *const_1)

for ele in input_elements:
    ele.addEventListener("change", change_lambda)

fig, ax = plt.subplots(layout='tight')
const_1 = setup_1()
plot_1(fig, ax, 400, 500, 1, 4, *const_1)

#################################
def setup_2():
    x_lim = 0.31
    x = np.linspace(-x_lim, x_lim, 100_000)
    return x, x_lim

def plot_2(fig2, ax3, ax4, lam, N, L, a, d, x, x_lim):
    ax3.clear()  
    ax4.clear()  
  
    y = int_dif(x, lam*1e-9, L, a*1e-6, d*1e-6, N)
    color = wavelength_to_rgb(lam)

    ax3.plot(x,y, color=color)
    ax3.margins(x=0)
    ax3.xaxis.set_major_locator(LOC)
    ax3.set_ylim(0,1)
    # ax3.set_xlabel('sen(θ)')
    ax3.set_ylabel('Intensidad')
    height = 1
    image = np.tile(np.sqrt(y), (height,1))

    colors = [
        (0,0,0),
        color,
    ]
    cmap = LinearSegmentedColormap.from_list("simple", colors)

    ax4.imshow(image, cmap=cmap, aspect="auto", extent=[-x_lim, x_lim, -1,1] )
    # ax4.set_xlabel('sen(θ)')
    ax4.set_xlabel('x (m)')
    ax4.xaxis.set_major_locator(LOC)
    ax4.yaxis.set_visible(False)
    Element("vizb").write(fig2)


input2_elements = js.document.getElementsByName("params2")

@create_proxy
def change_params2(event):
    L, N, a, d, lam = [num(el.value) for el in input2_elements]
    Element("N2_txt").write(f"N = {N}")
    Element("L2_txt").write(f"L = {L:.2f} m")
    Element("a2_txt").write(f"a = {a:.2f} μm")
    Element("d2_txt").write(f"d = {d} μm")
    Element("lam22_txt").write(f"λ₂ = {lam} nm")
    plot_2(fig2, ax3, ax4, lam, N, L, a, d, *const_2)

for ele in input2_elements:
    ele.addEventListener("change", change_params2)


fig2, (ax3, ax4) = plt.subplots(2, 1, layout='tight')
fig2.set_size_inches(10, 8)
fig2.canvas.header_visible = False
    
const_2 = setup_2()
plot_2(fig2, ax3, ax4, 600, 5, 1, 4, 30, *const_2)

##############

def setup_3():
    # x_lim = 3.2*l_sup*L/d
    x_lim = 0.6
    x = np.linspace(-x_lim, x_lim, 40_000)
    return x, x_lim

def plot_3(fig3, ax5, l_inf, l_sup, N, L, d, x, x_lim):
    ax5.clear()
    waves = np.linspace(l_inf, l_sup, 100)
    for wave in waves:
        i = interferencia(x, wave*1e-9, L, d*1e-6, N)
        ax5.plot(x, i, color=wavelength_to_rgb(wave)) # label=f'{wave} nm',

    # ax5.xaxis.set_major_locator(LOC)
    ax5.set_ylim(0.01,0.5)
    ax5.yaxis.set_visible(False)
    ax5.set_xlabel('x (m)')
    ax5.set_ylabel('Intensidad')

    Element("vizc").write(fig3)


input3_elements = js.document.getElementsByName("params3")

@create_proxy
def change_params3(event):
    L, N, l_inf, l_ran = [num(el.value) for el in input3_elements]
    d = 1e4/N # micrones
    l_sup = l_inf + l_ran
    Element("L3_txt").write(f"L = {L:.2f} m")
    Element("N3_txt").write(f"{N} líneas/cm")
    Element("d3_txt").write(f"d = {d:.2f} μm")
    Element("lam31_txt").write(f"λ₁ = {l_inf} nm")
    Element("lam32_txt").write(f"{l_ran} nm")
    Element("lam33_txt").write(f"λ₂ = {l_sup} nm")
    
    plot_3(fig3, ax5, l_inf, l_sup, N, L, d, *const_3)

for ele in input3_elements:
    ele.addEventListener("change", change_params3)


fig3, ax5 = plt.subplots(layout='tight')
const_3 = setup_3()
plot_3(fig3, ax5, 480, 680, 3000, 1, 10/3, *const_3)
