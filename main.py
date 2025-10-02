import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
canvas = tk.Canvas()
root.title("RoFT Signboard Generator")
root.iconbitmap("resources/RTCat Avatar.ico")
root.geometry("512x512")

def load():
    btn.place(x=256,y=0,width=50,height=20,anchor="n")
    btn2.config(command=unload)

def unload():
    btn.place_forget()
    btn2.config(command=load)

label = tk.Label(text="0")
label.place(x=100,y=60,width=30,height=20,anchor='n')
root.update_idletasks()
labelWidth = label.winfo_width()
labelHeight = label.winfo_height()
print(labelWidth,",",labelHeight)

img = Image.open("output.png")
res_img = img.resize((128,128))
tk_img = ImageTk.PhotoImage(res_img)
label = tk.Label(root, image=tk_img)
label.place(x=256,y=64,anchor='n')

btn = tk.Button(text="btn",relief="flat") # image=pixel,width=50,height=20,compound="c"
btn.place(x=256,y=0,width=50,height=20,anchor='n')

btn2 = tk.Button(text="btn2",command=unload) # image=pixel,width=50,height=20,compound="c"
btn2.place(x=256,y=20,width=50,height=20,anchor='n')

closebutton = tk.Button(text="X",bg="#f00",fg="#fff",font="Arial 8 bold",relief="flat",command=root.destroy)
closebutton.place(x=512,y=0,width=50,height=20,anchor='ne')

entry = tk.Entry(highlightthickness=3,highlightbackground="red",highlightcolor="green")
entry.place(x=250,y=200,width=50,height=20,anchor='n')

entry2 = tk.Entry(highlightthickness=3,highlightbackground="red",highlightcolor="green")
entry2.place(x=250,y=220,width=50,height=20,anchor='n')

options = ["A","B","C","D"]

varoptions = tk.StringVar(root)
varoptions.set(options[0])
selector = tk.OptionMenu(root,varoptions,*options)
selector.place(x=256,y=40,width=50,height=20,anchor="n")
listoptions = tk.StringVar(root,["a","Ab"])
listbox = tk.Listbox(root,listvariable=listoptions)
listbox.place(x=256,y=300,width=50,height=40,anchor="n")
root.update_idletasks()
selectorWidth = selector.winfo_width()
selectorHeight = selector.winfo_height()
print(selectorWidth,",",selectorHeight)

#canvas.create_rectangle(125,40,174,59,outline ="black",width = 2)
#canvas.pack()

root.mainloop()
