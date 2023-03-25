import os, sys


#from Tkinter import Frame, Tk, Label, Button, Scale, HORIZONTAL, Checkbutton, IntVar
from tkinter import *
#from tkFileDialog import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageStat, ImageDraw, ImageFont, TiffImagePlugin, ImageTk

import tkinter as tk
from scipy import ndimage

import math

import scipy
#import pylab
from scipy import polyval, polyfit, ndimage
from pylab import polyfit, polyval

import numpy as np
def Show_pic(pic):
	im = pic.copy()
	im.thumbnail((800,800), Image.ANTIALIAS)
	imtk=ImageTk.PhotoImage(im)
	label = tk.Label(image=imtk, height =600, width = 800)
#	label = Label(image=imtk, height =600, width = 800)
	label.image= imtk
	label.grid(row =5, rowspan=50, column =2)
	main.update()

def Pixel_check(curFile, dirF, file):
	pic = Image.open(curFile)
	pic2= Image.open(curFile)
	picr= Image.open(curFile)
	if (rotPic.get()):
		print ("Rotating picture 180")
		pic = pic.rotate(180)
	if (flipPic.get()):
		print ("Flipping picture")
		pic = pic.transpose(Image.FLIP_LEFT_RIGHT)
	imgdata = pic.load()
	print (file, " loaded")
	###################
	totleaflength=0
	###################
	speedP=speedPscale.get()
	xsize, ysize = pic.size
	xsize=xsize/speedP
	ysize=ysize/speedP
	pic=pic.resize((int(xsize),int(ysize)))
	pic2=pic2.resize((int(xsize),int(ysize)))
	picr=picr.resize((int(xsize),int(ysize)))
	xsize, ysize = pic.size
	print (xsize,"x", ysize)
	#minG=minGscale.get()
	minR=minRscale.get()
	#ratG=ratGscale.get()
	#ratGb=ratGbscale.get()
	threshW = threshWscale.get()
	ratR=ratRscale.get()
	##################################

	#################################
	#print minG, minR, ratG, ratR
	pic = pic.convert("RGB")
	pixels = pic.load() # create the pixel map
	leafpix = []
	scalepix = []
	backpix = []
	leafonly = pic2.load()
	scaleonly = picr.load()
	for i in range(pic.size[0]):    # for every pixel:
		for j in range(pic.size[1]):
			#print pixels[i,j]
			r, g, b = pixels[i,j]
			if r>minR and g*ratR<r and b*ratR<r :
				scalepix.append((i,j))
				#pixels[i,j] = (0,0,255)
				scaleonly[i,j] = (255,0,0)
				leafonly[i,j] = (0,0,0)
			else:
				scaleonly[i,j] = (0,0,0)
				if r < threshW and b< threshW  and g< threshW :
					leafpix.append((i,j))
					leafonly[i,j] = (0,255,0)
					#scaleonly[i,j] = (0,0,0)
				else:
					leafonly[i,j] = (0,0,0)
					backpix.append((i,j))

	gCnt=len(leafpix)
	#rCnt=len(scalepix)
	if (delBack.get()):
		for i in backpix:
			pixels[i] = (255,255,255)



	#pic2 = Image.open(pic2)
	pic2 = pic2.convert('L')
	flat = np.array(pic2)

#	picr = Image.open(picr)
	picr = picr.convert('L')
	flatr = np.array(picr)



#	flat = scipy.misc.fromimage(pic2,flatten=1)
#	flatr= scipy.misc.fromimage(picr,flatten=1)

	blobs, leaves = ndimage.label(flat)
	blobsr, scales = ndimage.label(flatr)
	scalehist=ndimage.measurements.histogram(blobsr, 1,scales,scales)
#########################################
#Blob analysis.  Only the largest red blob is analyzed as scale area
	try: maxscale=max(scalehist)
	except: pass
	cnt=1
	gcnt=0
	parcnt=0
	rCnt=0
	largescale = []
	#totleaflength=0

	for s in scalehist:
		#print s
		#if s>1000:
		if s == maxscale:
			cnti=0
			cntj=0
			gcnt=0
			parcnt=parcnt+1
			for i in range(pic.size[0]):    # for every pixel:
				for j in range(pic.size[1]):
					if blobsr[j,i]==cnt:
						gcnt=gcnt+1
						rCnt=rCnt+1
						cnti=cnti+i
						cntj=cntj+j
						pixels[i,j]=(255,0,0)
						flat[j,i] = (0)
			cnti=cnti/gcnt
			cntj=cntj/gcnt
			largescale.append(gcnt)
			if labpix.get():
				draw=ImageDraw.Draw(pic)
				draw.text((cnti,cntj),str(gcnt), (0,0,0))


		cnt=cnt+1
		####################
	scalesize = SSscale.get()
	if scalesize ==0:
		print ("No scale.  Leaf lengths not to scale")
		#scalesize =1
		scalesquarelength=1
		scalelength=1
	else:
		scalesquarelength=math.sqrt(gcnt)
		if scalesquarelength ==0:
			scalesquarelength=1
		scalelength = math.sqrt(SSscale.get())

		##########
		##########

############
#Leaf blob analysis
	blobhist=ndimage.measurements.histogram(blobs, 1,leaves,leaves)
	minPsize=minPscale.get()

########largest leaf elements only instead of minimum particle size
	try: maxleaf=max(blobhist)
	except: pass
	if ThereCanBeOnlyOne.get():
		cnt=1
		gcnt=0
		parcnt=0
		gCnt=0
		largeleaf = []
		############
		########
		totleaflength=0
		#########
		#############
		for s in blobhist:
			if s == maxleaf:
				cnti=0
				cntj=0
				gcnt=0
				parcnt=parcnt+1
				for i in range(pic.size[0]):    # for every pixel:
					for j in range(pic.size[1]):
						if blobs[j,i]==cnt:
							gcnt=gcnt+1
							gCnt=gCnt+1
							cnti=cnti+i
							cntj=cntj+j
							pixels[i,j]=(0,255,0)
							flat[j,i] = (0)
				cnti=cnti/gcnt
				cntj=cntj/gcnt
				##############
				########

				#print gcnt
				if SSscale.get()>0:
					gcnt = float(gcnt)/float(rCnt)*SSscale.get()
					gcnt = "%.3f" % gcnt
					#gcnt=int(gcnt)
				#print gcnt
				########
				##########################################

				largeleaf.append(gcnt)

				##############
				##########
				leaflength=0
				templength=0

				#########
				###########
				##########################
				##########################
				#Creates an outline array for leaf
				##################
				if (doleaflength.get()):

					blobedgepix = []

					for i in range(pic.size[0]):    # for every pixel:
						for j in range(pic.size[1]):
							if blobs[j,i]==cnt:
								try:
									if blobs[j-1,i]!=cnt or blobs[j,i-1]!=cnt or blobs[j,i+1]!=cnt or blobs[j+1,i]!=cnt:
										blobedgepix.append((i,j))
								except IndexError:
									blobedgepix.append((i,j))
					###########
					#Checks for maximum length between any two pixels in perimeter of leaf.
					##################
					for i in blobedgepix:
						xpix,ypix =i
						for j in blobedgepix:
							xtemp,ytemp = j
							templength=math.sqrt((xpix-xtemp)**2+(ypix-ytemp)**2)
							if leaflength< templength:
								leaflength=templength
					totleaflength=totleaflength+leaflength
					############
					#################
				####################
				###########
				if (doleaflength.get()):
					if scalesize ==0:
						#print "No scale.  Leaf length not to scale"
						leaflength=int(leaflength)
						#print leaflength
						#scalesize =1
					else:
						leaflength=int(10*scalelength/scalesquarelength*leaflength)
						#print "Maximum Length in mm (Only if your scale is square)"
						#leaflength=int(leaflength)
						#print leaflength
					largeleaf.append(gcnt)
					############
				#####################
				##############

				if labpix.get():
					draw=ImageDraw.Draw(pic)
					##############
					##############
					if scalesize ==0:
						draw.text((cnti,cntj),str(gcnt)+' pixels area', (0,0,0))
						if (doleaflength.get()):
							draw.text((cnti,cntj-10),str(leaflength)+' pixels long', (0,0,0))
						#scalesize =1
					else:
						##

						draw.text((cnti,cntj),str(gcnt)+' cm^2', (0,0,0))
						if (doleaflength.get()):
							draw.text((cnti,cntj-10),str(leaflength)+' mm', (0,0,0))
						####gcnt=gcnt*scalesize/



					#draw.text((cnti,cntj),str(gcnt), (0,0,0))


			cnt=cnt+1
		###############
		###########
		if (doleaflength.get()):
			if scalesize ==0:
				totleaflength=int(totleaflength)
			else:
				totleaflength=int(10*scalelength/scalesquarelength*totleaflength)
				print ("Total length in mm (Only if your scale is square)")

		#largeleaf.append(int(totleaflength))
		leafprint= ', '.join(map(str, largeleaf))
		#print int(totleaflength)
		###########
		####################

		#leafprint= ', '.join(map(str, largeleaf))
#Leaf element minimum particle size:
	elif minPsize>10:
		cnt=1
		gcnt=0
		parcnt=0
		gCnt=0
		############
		########
		totleaflength=0
		#########
		#############
		largeleaf = []
		for s in blobhist:
			if s>minPsize:
				cnti=0
				cntj=0
				gcnt=0
				##############
				##########
				leaflength=0
				templength=0

				#########
				###########
				parcnt=parcnt+1
				##########################
				#Creates an outline array for leaf
				##################
				if (doleaflength.get()):

					blobedgepix = []

					for i in range(pic.size[0]):    # for every pixel:
						for j in range(pic.size[1]):
							if blobs[j,i]==cnt:
								try:
									if blobs[j-1,i]!=cnt or blobs[j,i-1]!=cnt or blobs[j,i+1]!=cnt or blobs[j+1,i]!=cnt:
										blobedgepix.append((i,j))
								except IndexError:
									blobedgepix.append((i,j))
					###########
					#Checks for maximum length between any two pixels in perimeter of leaf.
					##################
					for i in blobedgepix:
						xpix,ypix =i
						for j in blobedgepix:
							xtemp,ytemp = j
							templength=math.sqrt((xpix-xtemp)**2+(ypix-ytemp)**2)
							if leaflength< templength:
								leaflength=templength
					totleaflength=totleaflength+leaflength
					############
					#################

				for i in range(pic.size[0]):    # for every pixel:
					for j in range(pic.size[1]):
						if blobs[j,i]==cnt:
							gcnt=gcnt+1
							gCnt=gCnt+1
							cnti=cnti+i
							cntj=cntj+j
							pixels[i,j]=(0,255,0)
							flat[j,i] = (0)
				cnti=cnti/gcnt
				cntj=cntj/gcnt
				####################
				###########
				if (doleaflength.get()):
					if scalesize ==0:
						#print "No scale.  Leaf areas not to scale"
						leaflength=int(leaflength)
						#print leaflength
						#scalesize =1
					else:
						leaflength=int(10*scalelength/scalesquarelength*leaflength)
						#print "Maximum Length in mm (Only if your scale is square)"
						#leaflength=int(leaflength)
						#print leaflength
					largeleaf.append(leaflength)
					############
				#####################
				##############
				########
				if SSscale.get()>0:
					gcnt = float(gcnt)/float(rCnt)*SSscale.get()
					gcnt = "%.3f" % gcnt
					#gcnt=(gcnt*100)
				########
				##########################################
				largeleaf.append(gcnt)
				if labpix.get():
					draw=ImageDraw.Draw(pic)
					#draw.text((cnti,cntj),str(gcnt), (0,0,0))
					##############
					if scalesize ==0:
						draw.text((cnti,cntj),str(gcnt)+' pixels area', (0,0,0))
						if (doleaflength.get()):
							draw.text((cnti,cntj-10),str(leaflength)+' pixels long', (0,0,0))
						#scalesize =1
					else:
						draw.text((cnti,cntj),str(gcnt)+' cm^2', (0,0,0))
						if (doleaflength.get()):
							draw.text((cnti,cntj-10),str(leaflength)+' mm', (0,0,0))
						####gcnt=gcnt*scalesize/
					##############
			cnt=cnt+1
		###############
		###########
		if (doleaflength.get()):
			if scalesize ==0:
				totleaflength=int(totleaflength)
			else:
				totleaflength=int(10*scalelength/scalesquarelength*totleaflength)
				print ("Total length in mm (Only if your scale is square)")


		print (int(totleaflength))
				##########
		#largeleaf.append(int(totleaflength))
		leafprint= ', '.join(map(str, largeleaf))
		###########
		####################
		#leafprint= ', '.join(map(str, largeleaf))
	else:
		print ("NO CONNECTED COMPONENT ANALYSIS")
		for i in leafpix:
			pixels[i] = (0,255,0)
		leafprint = "No connected component analysis"
	if rCnt < 1:
		rCnt+=1
	scalesize = SSscale.get()

	#if scalesize ==0:
	#	print ("No scale.  Leaf areas not to scale")
		#scalesize =1
	leafarea = float(gCnt)/float(rCnt)*scalesize
	Show_pic(pic)
	highlightfile = dirF+'/leafarea.csv'
	pixdata=file+', '+str(gCnt)+', '+str(rCnt)+', '+'%.2f' % leafarea+','+str(int(totleaflength))+','+leafprint+'\n'
	#pixdata=file+', '+str(gCnt)+', '+str(rCnt)+', '+'%.2f' % leafarea+','+leafprint+'\n'

	return totleaflength, gCnt, rCnt, pic, pixdata

def test_LA():
	print ("Measuring...")
	global chosfile
	global dirF

	#get absolute path
	dirF = os.path.dirname(chosfile)
	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	file = os.path.basename(chosfile)
	(totleaflength, gCnt, rCnt, pic, pixdata) = Pixel_check(chosfile, dirF, file)
	if rCnt < 1:
		rCnt+=1
	scalesize = SSscale.get()
	if scalesize ==0:
		print ("No scale.  Leaf area not to scale.")
		#######
		####
		######
		#scalesize =1
	leafarea = float(gCnt)/float(rCnt)*scalesize
	if rCnt <2:
		rCnt = 0
	filelabel= Label (main, height =1, width=60)
	speedP=speedPscale.get()
	xsize=xsize/speedP
	ysize=ysize/speedP
	filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
	filelabel.grid (row =1, column =2)
	Pixlabel = Label(main, height = 1, width = 60)
	#################
	scalesquarelength=math.sqrt(rCnt)

	######

	######
	if scalesquarelength ==0:
		scalesquarelength =1
	scalelength = math.sqrt(SSscale.get())
	if (doleaflength.get()):
		if scalesize ==0:
			totleaflength=int(totleaflength)
			Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf length pixels: "+ str(totleaflength))
		else:
			#print ("scale square length ", scalesquarelength, ", ")
			#print ("total leaf length ", totleaflength, ", ")
			#print ("scale length ", scalelength, ", ")
			#totleaflength=int(10*scalelength/scalesquarelength*totleaflength)
			print ("Total length in mm (Only if your scale is square)")
			#####
			#print ("scale square length ", scalesquarelength, ", ")
			#print ("total leaf length ", totleaflength, ", ")
			#print ("scale length ", scalelength, ", ")
			########
			Pixlabel.configure (text = "Leaf pix: "+ str(gCnt)+ "  Scale pix: "+ str(rCnt)+ " Leaf area: "+ '%.2f' % leafarea+ "cm^2"+" Length mm: "+ str(totleaflength))
	else:

		Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")
	#############
	##################
	#########################
	#Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")

	Pixlabel.grid(row =2, column =2)

	print ("Finished processing image")

def single_LA():
	print ("Measuring...")
	global chosfile
	global dirF

	dirF = os.path.dirname(chosfile)
	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	file = os.path.basename(chosfile)
	(totleaflength, gCnt, rCnt, pic, pixdata) = Pixel_check(chosfile, dirF, file)

	if rCnt < 1:
		rCnt+=1
	leafarea = float(gCnt)/float(rCnt)*4.0
	if rCnt <2:
		rCnt = 0
	filelabel= Label (main, height =1, width=60)
	speedP=speedPscale.get()
	xsize=xsize/speedP
	ysize=ysize/speedP
	filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
	filelabel.grid (row =1, column =2)
	Pixlabel = Label(main, height = 1, width = 60)
	Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")
	Pixlabel.grid(row =2, column =2)
	highlightfile = dirF+'/leafarea.csv'
	try:
		with open(highlightfile, "a") as f:
		####################
			if (doleaflength.get()):
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length pixels, Component length pixels:, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length mm, Component length mm:, Component area cm^2:")
			else:
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component area cm^2:")
#			f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length, Component green pixels:")
			f.write("\n")
	except:
		open (dirF+'/leafarea.csv', "w")
		print ("creating new output file")
		with open(highlightfile, "a") as f:
				####################
				####################
			if (doleaflength.get()):
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length pixels, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length mm, Component area cm^2:")
			else:
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component area cm^2:")

			#f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
			#f.write("\n")
			f.write("\n")
	save_Output(highlightfile, file, pixdata, pic, dirF)
	print ("Finished processing image")

def run_LA():
	print ("Measuring...")
	global dirS
	global dirF
	global chosfile

	dirS = os.path.abspath(dirS)
	dirF = os.path.abspath(dirF)
	filesInCurDir = os.listdir(dirS)
	try:
		with open(dirF+'/leafarea.csv', "a") as f:
		####################
			if (doleaflength.get()):
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length pixels, Component length pixels, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length mm, Component length mm:, Component area cm^2:")
			else:
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component area cm^2:")
#			f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length, Component green pixels:")
			f.write("\n")
	except:
		open (dirF+'/leafarea.csv', "w")
		#print "creating new output file"
		with open(dirF+'/leafarea.csv', "a") as f:
			###################
			if (doleaflength.get()):
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length pixels, Component length pixels, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, leaf length mm, Component length mm:, Component area cm^2:")
			else:
				if SSscale.get() ==0:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component green pixels:")
				else:
					f.write("filename,total green pixels,red pixels (scale),leaf area cm^2, Component area cm^2:")
#			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, leaf length, Component green pixels:")
			f.write("\n")

#			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
#			f.write("\n")
#	except:
#		open (dirF+'/leafarea.csv', "w")
#		with open(dirF+'/leafarea.csv', "a") as f:
#			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
#			f.write("\n")
	for file in filesInCurDir:
		curFile = os.path.join(dirS, file)
		try:
			pic = Image.open(curFile)
			xsize, ysize = pic.size
		except:
			continue
		Show_pic(pic)

		chosfile = curFile
		if (autocheck.get()):
			global ConsData
			ConsData = [0,0,0,0,0]
			auto_Settings(ConsData)
		(totleaflength, gCnt, rCnt, pic, pixdata) = Pixel_check(curFile, dirF, file)
		if rCnt < 1:
			rCnt+=1
		leafarea = float(gCnt)/float(rCnt)*4.0
		if rCnt <2:
			rCnt = 0

		filelabel= Label (main, height =1, width=60)
		speedP=speedPscale.get()
		xsize=xsize/speedP
		ysize=ysize/speedP
		filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
		filelabel.grid (row =1, column =2)
		Pixlabel = Label(main, height = 1, width = 60)
		Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")
		Pixlabel.grid(row =2, column =2)
		highlightfile = dirF+'/leafarea.csv'
		save_Output(highlightfile, file, pixdata, pic, dirF)
	print ("Finished processing images")

def S_dir():
	global dirS
	dirS = askdirectory()
	Slabel.configure(text = dirS)
def F_dir():
	global dirF
	dirF = askdirectory()
	Flabel.configure(text = dirF)
def check_Sett():
	print ("Batch processing")
	run_LA()
def chos_file():
	global chosfile
	chosfile = askopenfilename()
	#chosfile = askopenfilename(filetypes=[("image file", "*.jpg; *.jpe; *.jpeg; *.tiff; *.tif")])
	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	Show_pic(pic)
	file = os.path.basename(chosfile)
	filelabel= Label (main, height =1, width=60)
	filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
	filelabel.grid (row =1, column =2)
	Pixlabel = Label(main, height = 1, width = 60)
	Pixlabel.configure (text = "  ")
	Pixlabel.grid(row =2, column =2)
	print ("loaded   "+chosfile)

def chos_calib():
	global choscalib
	choscalib = askopenfilename(filetypes=[("comma-delimited","*.csv")])
	print ("loading calib file")
	with open(choscalib) as csvfile:
		#next(csvfile) # ignore header
		a = [row.strip().split(',') for row in csvfile]
	######linear regression for min G
	x = [float(i[0]) for i in a]
	y = [float(i[3]) for i in a]
	(m,b) =polyfit(x,y,1)
	mg=m
	bg=b
	######linear regression for G/R
	x = [float(i[1]) for i in a]
	y = [float(i[4]) for i in a]
	(m,b) =polyfit(x,y,1)
	mgr=m
	bgr=b
	######linear regression for G/B
	x = [float(i[2]) for i in a]
	y = [float(i[5]) for i in a]
	(m,b) =polyfit(x,y,1)
	mgb=m
	bgb=b
	############
	############
	x = [float(i[6]) for i in a]
	y = [float(i[8]) for i in a]
	(m,b) =polyfit(x,y,1)
	mmr=m
	bmr=b

	x = [float(i[7]) for i in a]
	y = [float(i[9]) for i in a]
	(m,b) =polyfit(x,y,1)
	mmg=m
	bmg=b

	print ("min G equation:",mg, "x+", bg,"\n G/R equation:", mgr,"x+",bgr,"\n G/B equation:",mgb, "x+",bgb)
	print ("min R equation:",mmr, "x+", bmr,"\n R/G&R/B equation:", mmg,"x+",bmg)
	print ("Loaded calib file")
	return mg,bg,mgr,bgr,mgb,bgb, mmr, bmr, mmg, bmg

def load_calib():
	try:
		with open(os.path.join(sys.path[0], "calib.csv")) as csvfile:
			#next(csvfile) # ignore header
			a = [row.strip().split(',') for row in csvfile]
		######linear regression for min G
		x = [float(i[0]) for i in a]
		y = [float(i[3]) for i in a]
		(m,b) =polyfit(x,y,1)
		####################
		print (sum((polyval(polyfit(x,y,1),x)-y)**2)/(len(x)))
		####################
		mg=m
		bg=b
		######linear regression for G/R
		x = [float(i[1]) for i in a]
		y = [float(i[4]) for i in a]
		(m,b) =polyfit(x,y,1)
		mgr=m
		bgr=b

		######linear regression for G/B
		x = [float(i[2]) for i in a]
		y = [float(i[5]) for i in a]
		(m,b) =polyfit(x,y,1)
		mgb=m
		bgb=b
		############
		############
		x = [float(i[6]) for i in a]
		y = [float(i[8]) for i in a]
		(m,b) =polyfit(x,y,1)
		mmr=m
		bmr=b

		x = [float(i[7]) for i in a]
		y = [float(i[9]) for i in a]
		(m,b) =polyfit(x,y,1)
		mmg=m
		bmg=b


		print ("loaded calib")
	except:
		mg= 1.223
		bg=-111
		mgr=0.360
		bgr=0.589
		mgb=0.334
		bgb=0.534
		mmr=1.412
		bmr=-140.6
		mmg=0.134
		bmg=0.782

		print ("calib file not found")
		print ("Set to default arabidopsis values")

	return mg,bg,mgr,bgr,mgb,bgb, mmr, bmr, mmg, bmg

def sing_Meas():
	print ("Measuring image")
	test_LA()
def show_Output():
	global dirF
	print (dirF)
	print ("Opening output file in default application")
	#Below is the code for windows
	outputfile = 'start '+dirF+'/leafarea.csv'
	#Below shoul dbe the code for Mac
	#outputfile = 'open "'+dirF+'/leafarea.csv"'
	print (outputfile)
	os.system(outputfile)

def save_Output(highlightfile, file, pixdata, pic, dirF):
	print ("save output")
	with open(highlightfile, "a") as f:
		f.write(pixdata)
	tifffile = file.replace('.jpg', '.tiff')
	pic.save(dirF+'/highlight'+tifffile)
def auto_Settings(WhatData):
	global chosfile
	pic = Image.open(chosfile)
	speedP=8
	xsize, ysize = pic.size
	xsize=xsize/speedP
	ysize=ysize/speedP
	pic=pic.resize((int(xsize),int(ysize)))
	xsize, ysize = pic.size
	print (xsize,"x", ysize)
	#ratG=2
	#ratGb=1.8
	thresW = 75
	cnt =0
	lpcntb = 0
	lpcnt =-1
	pixMinGreen = xsize*ysize*0.0025
	pic = pic.convert("RGB")
	pixels = pic.load() # create the pixel map


	ratR=2
	minR = 150
	cnt =0
	lpcntb = 0
	lpcnt =0
# Conservative pixel selection of 200+ pixels at 1/8th resolution:
	while cnt <pixMinGreen:
		scalepix=[]
		for i in range(pic.size[0]):    # for every pixel:
			for j in range(pic.size[1]):
				r, g, b = pixels[i,j]
				if g*ratR < r and b*(ratR)< r  and r> minR:
					scalepix.append((r,g,b))

		cnt=len(scalepix)
		lpcnt=lpcnt+1
		if lpcnt <8:
			ratR = 0.94*ratR
		if lpcnt >7:
			ratR = 2
			minR = 0.99*minR
		if lpcnt >10:
			cnt =(pixMinGreen+10)
	print (minR, ratR, "to select >",pixMinGreen," scale pixels after", lpcnt, "loops")
	ravg=0
	rgavg=0
	rbavg=0
	cnt=len(scalepix)
	if cnt>0:
		for i in scalepix:
			r, g, b = i
			if g<1: g=r
			if b<1: b=r
			ravg=ravg+r
			rgavg= rgavg+(float(r)/float(g))
			rbavg= rbavg+(float(r)/float(b))

		ravg=float(ravg)/float(cnt)
		rgavg=float(rgavg)/float(cnt)
		rbavg=float(rbavg)/float(cnt)
		rgavg=(rgavg+rbavg)/2
		rrat=mmrgset*rgavg+bmrgset
		if rrat <1.011: rrat=1.01
		minRscale.set(mmrset*ravg+bmrset)
		ratRscale.set(rrat)
	else:
		minRscale.set(255)
		ratRscale.set(2)
		print ("No Scale detected")
	#ConsData = [gavg, gravg, bravg, ravg, rgavg]
	ConsData = [ravg, rgavg]
    
	#print ConsData, "Values can be added to calib file"
	print (ravg, mmrset, bmrset, (mmrset*ravg+bmrset))
	#ratGbscale.set(0.334*bravg+0.534)
	return ConsData

def auto_Sing():
	global ConsData
	ConsData = [0,0,0,0,0]
	auto_Settings(ConsData)
	sing_Meas()

#load calib file on first run
#mgset, bgset, mgrset, bgrset, mgbset, bgbset = load_calib()

#load calib file on first run
mgset, bgset, mgrset, bgrset, mgbset, bgbset, mmrset, bmrset, mmrgset, bmrgset = load_calib()

main = Tk()
main.title("Easy Leaf Area (Scanner edition with length measurements")

Frame1 = Frame(main)
Frame1.grid (row= 1, column = 1, rowspan = 17)


runsingbut = Button(Frame1, text ="Analyze with current settings", command = test_LA)

saveresults = Button(Frame1, text ="Save analysis", command = single_LA)

SObut = Button(main, text ="Open output csv file", command = show_Output)

singbut = Button(Frame1, text = "Open an image", command = chos_file)
singlabel = Label(Frame1)
###############################
#loadcalibbut= Button(Frame1, text = "Load calib File", command = calib_set)

###############################
Batchlabel = Label(Frame1)
Batchlabel.configure (text ="Batch Processing:")

dirS ="C:/"
Sbut = Button(Frame1, text = "Select batch source Folder", command = S_dir)
Slabel = Label(Frame1)
Slabel.configure (text ="C:/")

dirF ="C:/"
Fbut = Button(Frame1, text = "Select batch output Folder", command = F_dir)
Flabel = Label(Frame1)
Flabel.configure (text ="C:/")

CSbut = Button(Frame1, text ="Start Batch with current settings", command = check_Sett)


Frame3 = Frame(main)
Frame3.grid (row= 1, column = 3, rowspan = 10)
##################
#addTocalibbut = Button (Frame1,text = "Add to calib File", command =addTocalib)
###############

#minG =100
#minGscale = Scale(Frame3, from_=0, to=255, label="Leaf minimum Green RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 250, variable = minG )
#minGscale.set(25)

minR =200
minRscale = Scale(Frame3, from_=0, to=255, label="Scale minimum Red RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 250, variable = minR )
minRscale.set(225)

#ratG =1.2
#ratGscale = Scale(Frame3, from_=0.9, to=2, resolution = 0.02, label="Leaf Green Ratio: (G/R)", orient=HORIZONTAL, tickinterval = 0.5, length = 200, variable = ratG )
#ratGscale.set(1.05)

threshW =220
threshWscale = Scale(Frame3, from_=0, to=255, resolution = 1, label="Scanner threshold", orient=HORIZONTAL, tickinterval = 50, length = 200, variable = threshW )
threshWscale.set(190)

#ratGb =1.35
#ratGbscale = Scale(Frame3, from_=0.8, to=2, resolution = 0.02, label="Leaf Green Ratio: (G/B)", orient=HORIZONTAL, tickinterval = 0.5, length = 200, variable = ratGb )
#ratGbscale.set(1.07)

ratR =1.3
ratRscale = Scale(Frame3, from_=1, to=2, resolution = 0.02, label="Scale Red Ratio: (R/G & R/B)", orient=HORIZONTAL, tickinterval = 0.5, length = 200, variable = ratR )
ratRscale.set(1.95)

speedP =1
speedPscale = Scale(Frame3, from_=1, to=8, resolution = 1, label="Processing Speed:", orient=HORIZONTAL, tickinterval = 1, length = 200, variable = speedP )
speedPscale.set(4)

minPsize =500
minPscale = Scale(Frame3, from_=1, to=5000, resolution = 10, label="Minimum Leaf Size (pixels):", orient=HORIZONTAL, tickinterval = 1000, length = 250, variable = minPsize )
minPscale.set(0)
#################
Scalesize =4.1
SSscale = Scale(Frame3, from_=0, to=20, resolution = 0.1, label="Scale area (cm^2):", orient=HORIZONTAL, tickinterval = 4, length = 250, variable = Scalesize )
SSscale.set(4)
###################
flipPic = IntVar()

C1 = Checkbutton(Frame1, text = "Flip image horizontal", variable = flipPic)
flipPic.get()

rotPic = IntVar()
C2 = Checkbutton(Frame1, text = "Rotate image 180 deg", variable = rotPic)
rotPic.get()

delBack = IntVar()
C3 = Checkbutton(Frame1, text = "Delete background", variable = delBack)
delBack.get()

labpix = IntVar()
C5 = Checkbutton(main, text = "Label Pixels", variable = labpix)
labpix.get()
#############################
doleaflength = IntVar()
C7 = Checkbutton(main, text = "Measure Leaf Length", variable = doleaflength)
doleaflength.get()


######################
######################
ThereCanBeOnlyOne = IntVar()
C6 = Checkbutton(main, text = "Only one Leaf component", variable = ThereCanBeOnlyOne)
ThereCanBeOnlyOne.get()
######################

autosetbut = Button(Frame1, text ="Auto settings", command = auto_Sing)

autocheck = IntVar()
C4 = Checkbutton(Frame1, text = "Use auto settings", variable = autocheck)
autocheck.get()

singbut.grid(row=1, column =1, pady=5)
autosetbut.grid(row=2, column =1, pady=5)
runsingbut.grid(row=3, column =1, pady=5)
saveresults.grid(row=4, column =1, pady=5)
C1.grid(row=5, column =1, pady=5)
C2.grid(row = 6, column =1, pady=5)
C3.grid(row=7, column = 1, pady=5)
Batchlabel.grid(row=9, column=1, pady=10)
Sbut.grid(row=10, column=1, pady=5)
Slabel.grid(row=11, column=1, pady=5)
Fbut.grid(row=12, column=1, pady=5)
Flabel.grid(row=13, column=1, pady=5)
CSbut.grid(row=14, column=1, pady=5)
C4.grid(row=15, column = 1, pady=5)
###############
#loadcalibbut.grid(row=16, column = 1, pady=5)
#addTocalibbut.grid(row=17, column =1, pady=5)
C6.grid(row=15, column = 3, pady=5)
##############
C7.grid(row=16, column=3, pady=5)
##############
threshWscale.grid(row=1, column =3)
#ratGscale.grid(row=2, column =3)
#ratGbscale.grid(row=3, column =3)

minRscale.grid(row=4, column =3)
ratRscale.grid(row=5, column =3)

speedPscale.grid(row=7, column=3)
minPscale.grid(row=8, column = 3)
SSscale.grid(row=6, column =3)

filelabel= Label (main, height =1, width=100)

filelabel.configure (text = " ")
filelabel.grid (row =1, column =2)
SObut.grid(row=3, column =2)
C5.grid(row=4, column = 2)
main.mainloop()