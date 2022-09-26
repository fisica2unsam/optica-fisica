import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
plt.rcParams["figure.figsize"] = (9,4)
from functions import difraccion, wavelength_to_rgb


from pyodide.http import open_url
from pyodide import create_proxy

# url = (
#     "https://raw.githubusercontent.com/Cheukting/pyscript-ice-cream/main/bj-products.csv"
# )
# ice_data = pd.read_csv(open_url(url))
# current_selected = []






"""
LAMBDA1 = 400
LAMBDA2 = 500

fig = plot(lambda1, lambda2)

callback(lambda1, lambda2):
    nwdata (lambda1, lambda2)
    fig.update_data(nwdata)

bind_callback

"""
a = 4e-6
L = 1
lam0 = 400e-9
x_lim = 3.1*lam0*L/a
x = np.linspace(-x_lim, x_lim, 100000)

def plot(fig, ax, lam1, lam2, L, a):
    
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
    ax.set_xlabel('sen(θ)')
    ax.set_ylabel('Intensidad')
    ax.legend()

    Element("viz").write(fig)
    

input_elements = document.getElementsByName("lam")

@create_proxy
def change_lambda(event):
    lam1, lam2 = [int(el.value) for el in input_elements]
    plot(fig, ax, lam1, lam2, L, a)

for ele in input_elements:
    ele.addEventListener("change", change_lambda)

fig, ax = plt.subplots()
plot(fig, ax, 400, 500, 1, 4e-6)