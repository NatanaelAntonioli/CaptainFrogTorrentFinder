from tkinter import *
from torrent_search import *
from PIL import ImageTk, Image
import subprocess 

handlers = []


def clicked():
    inp = inputtxt.get(1.0, "end-1c")
    global handlers
    handlers= listar_torrents(inp)
    listbox.delete(0, END)

    for i in range (len(handlers)):
        #titulo_buscar = Label(window, text=lista_handlers[i][0])
        #titulo_buscar.grid(column=1, row=i)
        listbox.insert(END, str(handlers[i][2]) + " | " + str(handlers[i][0]))

def listbox_clicked(event):
    cs = listbox.curselection()
    for list in cs:
        # Checar se é windows ou unix-like
        if os.name == 'nt': # windows
            os.startfile(handlers[list][1])
        else: # linux com xdg-open
            subprocess.call(['xdg-open', handlers[list][1]])
            

global_offset = 130
x_offset_adjust = 23

# Define a janela
window = Tk()
window.resizable(0,0)
window.title("Captain Frog's Torrent Finder")
window.geometry('800x600')

# Define o termo de busca
titulo_buscar = Label(window, text="Insert search term: ")
titulo_buscar.place(x=10 + x_offset_adjust, y=10 + global_offset, in_=window)

# Define o campo onde recebemos o input
inputtxt = Text(window, height=1, width=50)
inputtxt.place(x=130 + x_offset_adjust, y=13 + global_offset, in_=window)

# Define o botão
btn = Button(window, text="Search!", command=clicked)
btn.place(x=550 + x_offset_adjust, y=9 + global_offset, in_=window)

# Define a listbox
listbox = Listbox(window, height=25, width=120)
listbox.place(x=30, y=50 + global_offset, in_=window)
listbox.bind('<Double-1>', listbox_clicked)

# Define a imagem do sapo
frame = Frame(window, width=20, height=10)
frame.pack()
frame.place(x=10 + x_offset_adjust, y=30)

img = ImageTk.PhotoImage(Image.open("sapo.png"))
image = Label(frame, image = img)
image.pack()

# Define o título
titulo_sapo = Label(window, text="Captain Frog's Torrent Finder")
titulo_sapo.place(x = 120 + x_offset_adjust, y=10, in_=window)
titulo_sapo.config(font=("Calibri", 20))

# Define o subtítulo

subtitulo_1 = Label(window, text="Please wait a few seconds to see results.")
subtitulo_1.place(x = 120 + x_offset_adjust, y=50, in_=window)

subtitulo_2 = Label(window, text="M - Main results, probably in good health.")
subtitulo_2.place(x = 120 + x_offset_adjust, y=70, in_=window)

subtitulo_3 = Label(window, text="S - Secondary results, could be in good health but probably aren't.")
subtitulo_3.place(x = 120 + x_offset_adjust, y=90, in_=window)

subtitulo_4 = Label(window, text="G - Google search results, useful for niche contents.")
subtitulo_4.place(x = 120 + x_offset_adjust, y=110, in_=window)

window.mainloop()