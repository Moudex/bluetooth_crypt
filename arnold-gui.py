#!/usr/bin/env python
# -*-coding:Utf-8 -*-

from Tkinter import *
import tkFileDialog
import os
import linecache

Main = Tk()

seedFile = ""
ficFile = ""
msg = StringVar()
msg.set("Welcome to the Arnold crypt/decrypter")

def openSeed():
    global seedFile
    seedFile = tkFileDialog.askopenfilename(filetypes = [("Seed Files", "*.seed")])

def openFile():
    global ficFile
    ficFile = tkFileDialog.askopenfilename(filetypes = [("All", "*"),("Arnold Files","*.arn")])

def OnValidate(S):
    return S.isdigit()

def run():
    global seedFile
    global ficFile
    global e_index
    if 0 >= len(seedFile):
	msg.set("Please choose a seed file")
	return
    elif 0 >= len(ficFile):
	msg.set("Please choose a file to crypt/decrypt")
	return
    elif 0 >= e_index.get():
	msg.set("Please enter an index for the seed")
	return
    elif len(e_index.get()) <= 0:
	msg.set("Please enter correct indexe for the seed")
	return
    
    seed = linecache.getline(seedFile, int(e_index.get())).rstrip()
    if seed == '':
	msg.set("Please enter correct indexe for the seed")
	return

    cl = ''
    if len(seed)==16:
	cl = '1100000000110000'
    elif len(seed)==128:
	cl = '00001000000010001000000010000001000000010001000000000001000010001000000000000000000010001001000000010000000000000000000000010001'
    else:
	msg.set("Length seed error")
	return

    out = ''
    name,ext = os.path.splitext(ficFile)
    if ext == '.arn':
	out = name
    else:
	out = ficFile + '.arn'

    os.system("./arnold.py -i %s -o %s -s %s -c %s" % (ficFile, out, seed, cl))
    Main.destroy()

Fenetre = PanedWindow(Main, orient=VERTICAL)
Fenetre.pack(fill=BOTH, expand=1)
Main.title("Arnold")

# Titre
titre = Label(Fenetre, textvariable=msg, bd=2, relief="ridge")
Fenetre.add(titre)

# Graines
p_graines = PanedWindow(Fenetre)
l_graines = Label(p_graines, text="Seed file : ")
l_graines.pack(side=LEFT)
b_graines = Button(p_graines, text="Browse", command= lambda: openSeed())
b_graines.pack(side=RIGHT)
Fenetre.add(p_graines)

# Index
p_index = PanedWindow(Fenetre)
l_index = Label(p_index, text="Index of seed : ")
l_index.pack(side=LEFT)
validatecmd = (p_index.register(OnValidate), '%S')
e_index = Entry(p_index, validate="key", vcmd=validatecmd, width=4)
e_index.pack(side=RIGHT)
Fenetre.add(p_index)

# Fichiers
p_fichier = PanedWindow(Fenetre)
l_fichier = Label(p_fichier, text="File to crypt/decrypt : ")
l_fichier.pack(side=LEFT)
b_fichier = Button(p_fichier, text="Browse", command=lambda: openFile())
b_fichier.pack(side=RIGHT)
Fenetre.add(p_fichier)

Fenetre.add(p_fichier)

# Bouton crypt/decrypt
b_crypt = Button(Fenetre, text="Crypt/Decrypt", command= lambda: run())
Fenetre.add(b_crypt)

Main.mainloop()
