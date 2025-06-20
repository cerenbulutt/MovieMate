import os
import tkinter as tk
os.environ['TCL_LIBRARY'] = r'C:\Users\ceren\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\ceren\AppData\Local\Programs\Python\Python313\tcl\tk8.6'


# UI
window = tk.Tk()
window.title("MovieMate")
window.geometry("700x700")
window.resizable(True, True)

# Frame for search
search_frame = tk.Frame(window, padx=20, pady=20)
search_frame.grid(row=0, column=0, sticky="ew")

content_label = tk.Label(search_frame, text="Aramak istediğiniz filmi giriniz:", font=('Arial', 12, "bold"))
content_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

movie_input = tk.Entry(search_frame, width=40, font=('Arial', 11))
movie_input.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

search_button = tk.Button(search_frame, text="Ara", font=('Arial', 11, "bold"), width=10)
search_button.config(fg="Green")
search_button.grid(row=0, column=2, padx=(10, 0), pady=(0, 10))

# Frame for results
result_frame = tk.Frame(window, padx=20, pady=10)
result_frame.grid(row=1, column=0, sticky="nsew")

show_movie = tk.Text(result_frame, width=80, height=18, font=('Arial', 10), wrap="word", borderwidth=2, relief="groove")
show_movie.grid(row=0, column=0, sticky="nsew")


window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

window.mainloop()
