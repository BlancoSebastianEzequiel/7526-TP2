import numpy as np
import matplotlib.pyplot as plt

def calculate_price(a, b, c, d, x):
    return ((a + c) / b) - ((d / b) * x)

def price_simulation(a, b, c ,d, seed, iterations):
    price_t = [seed]
    for i in range(1, iterations):
        price_t.append(calculate_price(a, b, c, d, price_t[-1]))

    return price_t

def plot_price_simulation(a,b,c,d,seed, iterations):
    p_simulation = price_simulation(a,b,c,d,seed, iterations)
    simulation_size = len(p_simulation)
    time_axis = np.linspace(0, simulation_size, simulation_size)
    plt.plot(time_axis, p_simulation)
    plt.ylabel("Price")
    plt.xlabel("Time")
    plt.show()

"""
    COBWEB plot implementation, based on:
    
    - https://en.wikipedia.org/wiki/Cobweb_plot
    - https://codereview.stackexchange.com/questions/56281/fixed-point-iteration-and-cobweb-plot
    - https://scipython.com/blog/cobweb-plots/
    - https://tex.stackexchange.com/questions/45678/creating-cobweb-diagrams-of-some-functions-with-tikz-pstrick-etc/45764#45764
    - https://www.youtube.com/watch?v=nxcKh36rep0
    
"""
def plot_price_coweb_simulation(a,b,c,d,seed, iterations):
    price_t = []
    next_price_t = []
    current = seed
    for i in range(iterations):
        #store Pt
        price_t.append(current)
        #store Pt+1
        next_price_t.append(calculate_price(a, b, c, d, current))
        #update current price to Pt+1
        current = next_price_t[-1]

    #plot (x, x) starting from seed
    plt.plot(price_t, price_t, 'g')
    #plot (x, f(y)) starting from seed
    plt.plot(price_t, next_price_t, 'b')


    #Iteration plot
    px = []
    py = []
    current = seed
    for it in range(iterations):
        # plot (x,f(x))
        px.append(current)
        current = calculate_price(a,b,c,d, current)
        py.append(current)
        # plot (f(x), f(x))
        px.append(current)
        py.append(current)

    plt.plot(px, py, 'r')
    plt.ylabel("Xt+1")
    plt.xlabel("Xt")
    plt.show()

print("Param set 1")

plot_price_simulation(10.0, 1.0, 0.4, 0.9, 10, 100)
plot_price_coweb_simulation(10.0, 1.0, 0.4, 0.9, 10, 100)

print("Param set 2")

plot_price_simulation(0.9, 0.89, 0.5, 0.9, 1.0, 100)
plot_price_coweb_simulation(0.9, 0.89, 0.5, 0.9, 1.0, 100)