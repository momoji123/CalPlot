import math
import matplotlib.pyplot as plt
import numpy as np

def plot_graph(calc):
    x_interval = eval(calc.x_interval_entry.get())
    x_from = eval(calc.x_from_entry.get())
    x_to = eval(calc.x_to_entry.get())
    
    # Generate x values based on the interval and range
    x_values = np.arange(x_from, x_to + x_interval / 2, x_interval)
    
    # Replace 'x' in the input with the generated x values
    y_values = []
    input_val = calc.mainOp.get_eval_str(calc.trigon_mode)
    for x in x_values:
        replaced_val = input_val.replace('x', str(x))
        y_values.append(eval(replaced_val))
    
    # Plot the graph
    plt.plot(x_values, y_values)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph of ' + calc.input_var.get())
    plt.show()