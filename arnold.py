#!/usr/bin/env python
# -*-coding:Utf-8 -*-

# TODO 
# * Lire et chiffrer par megaoctet ou plus
# * Afficher la progression


from optparse import OptionParser
import sys
import os
import progressbar
import mmap

######################
##      OPTIONS     ## 
######################

vers = "%prog 2.0 (CC BY-NC-SA 3.0 FR)2014"
desc = "Crypte et decrypte des fichiers"
parser = OptionParser(version=vers, description=desc)
parser.add_option("-o", "--output", dest="outfile", default="out", action="store", type="string", help="Output file", metavar="FILE")
parser.add_option("-s", "--seed", dest="seed", action="store", type="string", help="seed key")
parser.add_option("-c", "--cl", dest="cl", action="store", type="string", help="Linear combination for the seed")
parser.add_option("-i", "--input", dest="infile", action="store", type="string", help="Input file", metavar="FILE")
(options, args) = parser.parse_args()

############################
##        CLASSES         ##
############################

class Lfsr():
    """Define all method for the lfsr"""

    def __init__(self, graine, masque):
	"""Constructor"""
	# TODO vérifier que la graine et le masque ont la même taille
	self.graine = graine
	self.cl = masque
    
    def get_bit(self):
	"""Get the next bit"""
	next_bit = False;
	for i in range(0, len(self.cl)):
	    if self.cl[i]:
		next_bit = self.graine[i]
		for j in range(i+1, len(self.cl)):
		    if self.cl[j]:
			next_bit = next_bit ^ self.graine[j]
		break
	return next_bit

    def next_octet(self):
	"""Set the next bytes of seed"""
	for i in xrange(0,8):
	    self.graine.append(self.get_bit())
	    self.graine = self.graine[1:]
    
    def get_int(self):
	"""Return the integer corresponding to the octet of seed"""
	str = ''
	self.next_octet()
	for i in xrange(0,8):
	    if self.graine[i]:
		str += '1'
	    else:
		str += '0'
	return int(str, 2)
    
    def get_int2(self):
	"""Return the integer corresponding to the octet of seed faster"""
	self.next_octet()
	return sum(1<<i for i, b in enumerate(self.graine) if b) % 256

######################
##     FONCTIONS    ##
######################

def str_to_bool (chaine):
    """Translate string to boolean array"""
    bools = []
    for c in chaine:
	if (c in ['1', 'y', 't']):
	    bools.append(True)
	else:
	    bools.append(False)
    return bools

def chiffre():
    """Chiffre un fichier en le lisant octet par octet"""
    fic_in = open(options.infile, 'rb')
    fic_out = open(options.outfile, 'wb')
    l = Lfsr(str_to_bool(options.seed), str_to_bool(options.cl))
    taille = os.path.getsize(options.infile)
    i = 0
    pbar = progressbar.ProgressBar(maxval=taille).start()
    try:
	while True:
	    i = i+1
	    octet = fic_in.read(1)
	    if octet == "":
		break
	    pbar.update(i)
	    out = chr(l.get_int2() ^ ord(octet))
	    fic_out.write(out)
    except IOError:
	sys.stderr.write('Erreur d\'E/S\n')
    finally:
	pbar.finish()
	fic_in.close()
	fic_out.close()

def chiffre2():
    """Chiffre un fichier par taille de blocs variable"""
    fic_in = open(options.infile, 'rb')
    fic_out = open(options.outfile, 'wb')
    l = Lfsr(str_to_bool(options.seed), str_to_bool(options.cl))
    taille = os.path.getsize(options.infile)
    blocksiz = 1024 * 1024
    i = 0
    pbar = progressbar.ProgressBar(maxval=taille).start()
    try:
	while True:
	    if i+blocksiz > taille:
		blocksiz = taille-i+blocksiz
	    octet = fic_in.read(blocksiz)
	    if blocksiz < 1:
		break
	    out = ""
	    for j in xrange(0, blocksiz):
		out = out + chr(l.get_int2() ^ ord(octet[j]))
		i = i + 1
		pbar.update(i)
	    fic_out.write(out)
    except IOError:
	sys.stderr.write('Erreur d\'E/S\n')
    finally:
	pbar.finish()
	fic_in.close()
	fic_out.close()

#####################
##    PROGRAMME    ##
#####################

if (options.seed == None or options.cl == None):
    sys.stderr.write('Seed key and mask required, see -h for more informations\n')
elif (len(options.seed) != len(options.cl)):
    sys.stderr.write('Seed key and mask must have same length\n')
elif (options.infile == None):
    sys.stderr.write('Input file required with -i or --input option, see -h for more informations\n')
else:
    chiffre()
