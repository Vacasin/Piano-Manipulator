import os

from music21 import converter

import pianoplayer
import tkinter as tk
from PIL import ImageTk, Image
import sys

from pianoplayer import core
from pianoplayer.hand import Hand
from pianoplayer.scorereader import reader
import subprocess

if len(sys.argv) < 2:  # no args are passed, pop up GUI

    if sys.version_info >= (3, 0):
        from tkinter import Frame, Tk, BOTH, Label, Scale, Checkbutton, BooleanVar,Canvas,Entry
        from tkinter.ttk import Button, Style, Combobox
        from tkinter import filedialog as tkFileDialog
    else:
        from tkinter import Frame, Tk, BOTH, Label, Scale, Checkbutton, BooleanVar,Canvas,Entry
        from Tk import Button, Style, Combobox
        import tkFileDialog



    ######################
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

            Button(self, text="Import Score", command=self.importCMD).place(x=100, y=20)

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

            Button(self, text="Generate", command=self.generateCMD).place(x=100, y=70)

            Button(self, text="Musescore", command=self.musescoreCMD).place(x=100, y=120)

            Button(self, text="Player", command=self.vpCMD).place(x=100, y=170)

            self.meas = Scale(self, from_=2, to=100, bg='white', length=210, orient='horizontal')
            self.meas.set(100)

            # self.meas.place(x=40, y=110)
            # Label(self, text='Max nr. of measures', bg="white").place(x=40, y=150)

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

    root = tk.Tk()
    root.geometry('300x220')
    app = PianoGUI(root)
    root.mainloop()


