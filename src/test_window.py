import tkinter as tk

# 1. Create the main window
root = tk.Tk()

# 2. Set the window's title and size
root.title("Tkinter Test")
root.geometry("300x200")  # Width x Height

# 3. Add a label with some text
label = tk.Label(root, text="If you can see this, tkinter is working!")
label.pack(pady=20)  # 'pady' adds some space on the top and bottom

# 4. Start the window's main event loop
# This line is crucial! It keeps the window open and responsive.
root.mainloop()

print("Window has been closed.")
