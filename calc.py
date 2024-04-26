import math
import re
import tkinter as tk
import numpy as np
from oplib.Op import Operation
from oplib import plotter

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x400")
        self.master.title("CalPlot")
        
        self.mainOp = Operation("main", None, False)
        self.currOp = self.mainOp
        self.input_var = tk.StringVar()
        self.input_var.set("")
        self.trigon_mode = "Rad"
        
        #main window
        self.main_window = tk.Text(self.master, wrap="none", height=2, state="disabled")
        self.main_window.pack()
        
        #Configure main_window to be horizontally scrollable
        scrollbar_x = tk.Scrollbar(self.master, orient="horizontal", command=self.main_window.xview)
        self.main_window.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Update main_window content when input_var changes
        self.input_var.trace("w", lambda *args: self.main_window.config(state="normal", highlightthickness=0, wrap="none") or self.main_window.delete(1.0, "end") or self.main_window.insert("end", self.input_var.get()) or self.main_window.config(state="disabled", highlightthickness=0, wrap="none))
        
        # Number area
        self.number_area = tk.Frame(self.master)
        self.number_area.pack(side="left", fill="both", expand=True)
        self.create_number_buttons()
        
        # Operation area
        self.operation_area = tk.Frame(self.master)
        self.operation_area.pack(side="left", fill="both", expand=True)
        self.create_operation_buttons()
        
        # X interval area
        x_input_label = tk.Label(self.master, text="X Interval:")
        x_input_label.pack()
        self.x_interval_entry = tk.Entry(self.master)
        self.x_interval_entry.pack()
        self.x_interval_entry.insert(0, "1")
        
        # X range from input field
        x_from_label = tk.Label(self.master, text="X From:")
        x_from_label.pack()
        self.x_from_entry = tk.Entry(self.master)
        self.x_from_entry.pack()
        self.x_from_entry.insert(0, "0")
        
        # X range "to" input field
        x_to_label = tk.Label(self.master, text="X To:")
        x_to_label.pack()
        self.x_to_entry = tk.Entry(self.master)
        self.x_to_entry.pack()
        self.x_to_entry.insert(0, "10")
        
        # Plot button
        self.plot_button = tk.Button(self.master, text="Plot", command=self.plot_graph)
        self.plot_button.pack()
        
        # Configure grid weights
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        
        # Keyboard key press event
        self.master.bind('<Key>', self.on_key_press)
        
    def create_number_buttons(self):
        for i in range(1,10):
            button = tk.Button(self.number_area, text=str(i), command=lambda num=str(i): self.add_to_input(num))
            button.grid(row=(i-1//3, column=(i-1)%3, sticky="nsew")
        button_zero = tk.Button(self.number_area, text="0", command=lambda num="0": self.add_to_input(num))
        button_zero.grid(row=3, column=1, sticky="nsew")
        self.number_area.grid_rowconfigure(0, weight=1)
        self.number_area.grid_rowconfigure(1, weight=1)
        self.number_area.grid_rowconfigure(2, weight=1)
        self.number_area.grid_columnconfigure(0, weight=1)
        self.number_area.grid_columnconfigure(1, weight=1)
        self.number_area.grid_columnconfigure(2, weight=1)
        
    def create_operation_buttons(self):
        operations=['+', '-', '/', '*', 'sin', 'cos', 'tan', '^', 'e', '.', 'log', ',', '(', ')', 'Switch', '=', 'C']
        row = 0
        col = 0
        max_col = 3
        for operation in operations:
            button = tk.Button(self.operation_area, text=operation, command=lambda op=operation: self.add_to_input(op))
            button.grid(row=row, column=col, sticky="nsew")
            col+=1
            if col > max_col-1:
                col = 0
                row += 1
        for i in range(row+1):
            self.operation_area.grid_rowconfigure(i, weight=1)
        for i in range(max_col):
            self.operation_area.grid_columnconfigure(i, weight=1)
    
    def add_to_input(self, value):
        current_input=self.mainOp.get_display_str()
        
        if value == "=":
            try:
                result = self.evaluate_expression()
                self.input_var.set(f"{current_input}={result}")
                return
            except Exception as e:
                self.input_var.set("Error")
        elif value == "C":
            self.mainOp.clear()
            self.currOp = self.mainOp
        elif value == "Switch":
            self.switch_trigon_mode()
        else:
            self.currOp = self.currOp.add_val(value)
        
        self.input_var.set(self.mainOp.get_display_str())
    
    def evaluate_expression(self):
        processed_input = self.mainOp.get_eval_str(self.trigon_mode)
        print(processed_input)
        result = eval(processed_input)
        return np.around(result, decimals=10)
        
    # Accept user input from keyboard
    def on_key_press(self, event):
        if event.widget != self.main_window:
            return
        
        key = event.char
        if key.isdigit() or key in ['+', '-', '/', '*', '.', ',', '(', ')', 'e', 'x']:
            self.add_to_input(key)
        elif key == '\r':
            self.add_to_input('=')
        elif key == 's':
            self.add_to_input('sin')
        elif key == 'c':
            self.add_to_input('cos')
        elif key == 't':
            self.add_to_input('tan')
        elif key == 'p':
            self.add_to_input('^')
        elif key == 'l':
            self.add_to_input('log')
        elif key == '\b': # backspace key
            self.remove_last_operation()
        elif event.keysym == 'Escape': # check for Escape key
            self.add_to_input('C')
    
    def remove_last_operation(self):
        self.currOp = self.mainOp.remove_val()
        self.input_var.set(self.mainOp.get_display_str())
    
    def plot_graph(self):
        plotter.plot_graph(self)
    
    def switch_trigon_mode(self):
        curr_mode = self.trigon_mode
        if curr_mode is "Rad":
            self.trigon_mode = "Deg"
        else:
            self.trigon_mode = "Rad"
        print(self.trigon_mode)

def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()