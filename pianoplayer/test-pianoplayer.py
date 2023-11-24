import os

from music21 import converter
from tkinter import *
import pianoplayer
import tkinter
from PIL import ImageTk, Image
import sys

from pianoplayer import core
from pianoplayer.hand import Hand
from pianoplayer.scorereader import reader
import subprocess
from tkinter.messagebox import *

index = tkinter.Tk()  #创建主窗口
# index.attributes('-alpha',1)  #窗口背景透明化

# 加载图片
canvas = tkinter.Canvas(index, width=800, height=600, bg=None)
image_file = tkinter.PhotoImage(file="images/pianoplayer-bg.png")
image = canvas.create_image(250, 0, anchor='n', image=image_file)
canvas.pack()

if len(sys.argv) < 2:  # no args are passed, pop up GUI

    if sys.version_info >= (3, 0):
        from tkinter import Frame, Tk, BOTH, Label, Scale, Checkbutton, BooleanVar,Canvas,Entry
        from tkinter.ttk import Button, Style, Combobox
        from tkinter import filedialog as tkFileDialog
    else:
        from tkinter import Frame, Tk, BOTH, Label, Scale, Checkbutton, BooleanVar,Canvas,Entry
        from Tk import Button, Style, Combobox
        import tkFileDialog

    class PianoGUI(Frame):

        def __init__(self, parent):
            Frame.__init__(self, parent, bg="white")
            self.parent = parent
            self.filename = 'scores/bach_invention4.xml'
            self.Rcb = BooleanVar()
            self.Lcb = BooleanVar()
            self.RightHandBeam = 0
            self.LeftHandBeam = 1
            self.initUI()

        def initUI(self):
            self.parent.title("PianoPlayer")
            self.style = Style()
            self.style.theme_use("clam")
            self.pack(fill=BOTH, expand=True)


            # Label(self, text="Hand Size:", bg="white").place(x=40, y=50)
            hvalues = ('XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL')
            self.handsize = Combobox(self, state="readonly", values=hvalues, width=4)
            self.handsize.current(3)
            # self.handsize.place(x=130, y=50)

            # Label(self, text="Scan:", bg="white").place(x=80, y=80)
            Rcb = Checkbutton(self, text="Right", variable=self.Rcb, bg="white")
            Rcb.select()
            # Rcb.place(x=130, y=80)
            Lcb = Checkbutton(self, text="Left", variable=self.Lcb, bg="white")
            Lcb.select()
            # Lcb.place(x=200, y=80)
            self.meas = Scale(self, from_=2, to=100, bg='white', length=210, orient='horizontal')
            self.meas.set(100)

            # self.meas.place(x=40, y=110)
            # Label(self, text='Max nr. of measures', bg="white").place(x=40, y=150)

            # 按钮
            ImportBtn = tkinter.Button(index, text='Import Score', width=12, height=1, relief='ridge',font=('Comic Sans MS', 11, 'bold'),
                                       activebackground='#317bff',activeforeground='white',command=self.importCMD,
                                       pady=7,bd=0.5, fg='white',bg='#6db2ff')
            ImportBtn.place(relx=0.1, rely=0.15)
            GenerateBtn = tkinter.Button(index, text='Generate', width=12, height=1, bd=0.5, relief='ridge',font=('Comic Sans MS', 11, 'bold'),
                                       activebackground='#317bff',activeforeground='white', fg='white',bg='#6db2ff',
                                         pady=7,command=self.generateCMD)
            GenerateBtn.place(relx=0.1, rely=0.3)
            MusescoreBtn = tkinter.Button(index, text='Musescore', width=12, height=1, bd=0.5, relief='ridge',font=('Comic Sans MS', 11, 'bold'),
                                       pady=7,activebackground='#317bff',activeforeground='white', fg='white',bg='#6db2ff',command=self.musescoreCMD)
            MusescoreBtn.place(relx=0.1, rely=0.45)
            PlayerBtn = tkinter.Button(index, text='Player', width=12, height=1, bd=0.5, relief='ridge',font=('Comic Sans MS', 11, 'bold'),
                                       pady=7,activebackground='#317bff',activeforeground='white', fg='white',bg='#6db2ff',command=self.vpCMD)
            PlayerBtn.place(relx=0.1, rely=0.6)

        def importCMD(self):
            ftypes = [('XML Music files', '*.xml'), ('Midi Music files', '*.mid'),
                      ('PIG Music files', '*.txt'), ('All files', '*')]
            dlg = tkFileDialog.Open(self, filetypes=ftypes)
            self.filename = dlg.show()
            print('Input File is ', self.filename)

        def generateCMD(self):
            sf = converter.parse(self.filename)

            if self.Rcb.get():
                self.rh = Hand("right", self.handsize.get())
                self.rh.noteseq = reader(sf, beam=self.RightHandBeam)
                self.rh.generate(nmeasures=self.meas.get())

            if self.Lcb.get():
                self.lh = Hand("left", self.handsize.get())
                self.lh.noteseq = reader(sf, beam=self.LeftHandBeam)
                self.lh.generate(nmeasures=self.meas.get())

            print("Saving score to output.xml")
            sf.write('xml', fp='output.xml')
            print("\nTo visualize score type:\n musescore output.xml\n")

        def vpCMD(self):
            from pypiano import Game

            game = Game()
            game.run(self.rh, self.lh, name=os.path.basename(self.filename))

        def musescoreCMD(self):
            print('try opening musescore')
            cmd = 'MuseScore4 ./output.xml'
            subprocess.Popen(cmd, shell=True)


index.title('PianoPlayer') #设置主窗口标题
index.geometry('640x480') #设置主窗口大小
#下面两行代码的作用是固定窗口大小，不可拉动调节
index.maxsize(640,480)
index.minsize(640,480)
app = PianoGUI(index)
index.mainloop()