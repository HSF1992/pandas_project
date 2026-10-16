import customtkinter as ctk
from GUI.app import app

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

window= ctk.CTk()
app(window)
window.mainloop()