
import os
import sys
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageStat, ImageDraw, ImageFont, ImageTk  # Removed TiffImagePlugin as it's rarely used directly
import tkinter as tk
from scipy import ndimage
import numpy as np
from numpy import polyfit, polyval

def Show_pic(pic):
	im = pic.copy()
	im.thumbnail((800,800))
	#	im.thumbnail((800,800), Image.ANTIALIAS)

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

	speedP=speedPscale.get()
	xsize, ysize = pic.size
	xsize=xsize/speedP
	ysize=ysize/speedP
	pic=pic.resize((int(xsize),int(ysize)))
	pic2=pic2.resize((int(xsize),int(ysize)))
	picr=picr.resize((int(xsize),int(ysize)))
	xsize, ysize = pic.size
	print (xsize,"x", ysize)
	minG=minGscale.get()
	minR=minRscale.get()
	ratG=ratGscale.get()
	ratGb=ratGbscale.get()
	ratR=ratRscale.get()
	##################################
	global mingGactual, ratGactual, ratGbactual
	mingGactual = minG
	ratGactual = ratG
	ratGbactual = ratGb
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
			if r*ratG < g and b*ratGb<g  and g> minG:
				leafpix.append((i,j))
				leafonly[i,j] = (0,255,0)
				scaleonly[i,j] = (0,0,0)
			else:
				leafonly[i,j] = (0,0,0)
				if r>minR and g*ratR<r and b*ratR<r :
					scalepix.append((i,j))
					#pixels[i,j] = (0,0,255)
					scaleonly[i,j] = (255,0,0)
				else:
					backpix.append((i,j))
					scaleonly[i,j] = (0,0,0)
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
				largeleaf.append(gcnt)
				if labpix.get():
					draw=ImageDraw.Draw(pic)
					draw.text((cnti,cntj),str(gcnt), (0,0,0))


			cnt=cnt+1
		leafprint= ', '.join(map(str, largeleaf))
#Leaf element minimum particle size:
	elif minPsize>10:
		cnt=1
		gcnt=0
		parcnt=0
		gCnt=0
		largeleaf = []
		for s in blobhist:
			if s>minPsize:
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
				largeleaf.append(gcnt)
				if labpix.get():
					draw=ImageDraw.Draw(pic)
					draw.text((cnti,cntj),str(gcnt), (0,0,0))
			cnt=cnt+1
		leafprint= ', '.join(map(str, largeleaf))
	else:
		print ("NO CONNECTED COMPONENT ANALYSIS")
		for i in leafpix:
			pixels[i] = (0,255,0)
		leafprint = "No connected component analysis"
	if rCnt < 1:
		rCnt+=1
	scalesize = SSscale.get()

	if scalesize ==0:
		print ("No scale.  Leaf areas not to scale")
		#scalesize =1
	leafarea = float(gCnt)/float(rCnt)*scalesize
	Show_pic(pic)
	highlightfile = dirF+'/leafarea.csv'
	pixdata=file+', '+str(gCnt)+', '+str(rCnt)+', '+'%.2f' % leafarea+','+leafprint+'\n'

	return gCnt, rCnt, pic, pixdata

def test_LA():
	print ("Measuring...")
	global chosfile
	global dirF

	#get absolute path
	dirF = os.path.dirname(chosfile)
	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	file = os.path.basename(chosfile)
	(gCnt, rCnt, pic, pixdata) = Pixel_check(chosfile, dirF, file)
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
	Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")

	Pixlabel.grid(row =2, column =2)

	print ("Finished processing image")

def addTocalib():
	global ConsData
	ConsData = [0,0,0,0,0]
	minG=minGscale.get()
	minR=minRscale.get()
	ratG=ratGscale.get()
	ratGb=ratGbscale.get()
	ratR=ratRscale.get()
	ConservativeData = auto_Settings(ConsData)
	minGscale.set(minG)
	ratGscale.set(ratG)
	ratGbscale.set(ratGb)
	minRscale.set(minR)
	ratRscale.set(ratR)
	sing_Meas()

	global chosfile
	global dirF

	calibdata=str(ConservativeData[0])+', '+str(ConservativeData[1])+', '+str(ConservativeData[2])+', '+str(minG)+', '+str(ratG)+', '+str(ratGb)+', '+str(ConservativeData[3])+', '+str(ConservativeData[4])+', '+str(minR)+', '+str(ratR)+'\n'
	dirF = os.path.dirname(chosfile)
	Newcalib = dirF+'/Newcalib.csv'
	try:
		open(Newcalib, "a")
	except:
		open (dirF+'/Newcalib.csv', "w")
		print ("Creating new calib file: Newcalib.csv")
	with open(Newcalib, "a") as f:
		f.write(calibdata)
	print ("Finished adding to calib file: Newcalib.csv.")
def single_LA():
	print ("Measuring...")
	global chosfile
	global dirF

	dirF = os.path.dirname(chosfile)
	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	file = os.path.basename(chosfile)
	(gCnt, rCnt, pic, pixdata) = Pixel_check(chosfile, dirF, file)

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
			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
			f.write("\n")
	except:
		open (dirF+'/leafarea.csv', "w")
		print ("creating new output file")
		with open(highlightfile, "a") as f:
			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
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
			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
			f.write("\n")
	except:
		open (dirF+'/leafarea.csv', "w")
		with open(dirF+'/leafarea.csv', "a") as f:
			f.write("filename,total green pixels,red pixels (4 cm^2),leaf area cm^2, Component green pixels:")
			f.write("\n")
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
		(gCnt, rCnt, pic, pixdata) = Pixel_check(curFile, dirF, file)
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
	#outputfile = 'start '+dirF+'/leafarea.csv'
	#Below shoul dbe the code for Mac
	outputfile = 'open "'+dirF+'/leafarea.csv"'
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
	ratG=2
	ratGb=1.8
	minG = 75
	cnt =0
	lpcntb = 0
	lpcnt =-1
	pixMinGreen = xsize*ysize*0.0025
	pic = pic.convert("RGB")
	pixels = pic.load() # create the pixel map
	while cnt <pixMinGreen:
		leafpix = []
		for i in range(pic.size[0]):    # for every pixel:
			for j in range(pic.size[1]):
				r, g, b = pixels[i,j]
				if r*ratG < g and b*(ratGb)<g  and g> minG:
					leafpix.append((r,g,b))
		lpcnt=lpcnt+1
		cnt=len(leafpix)
		if lpcnt <12:
			ratG = 0.94*ratG
			ratGb = 0.94*ratGb
		if lpcnt >11:
			minG = 0.9*minG
		if lpcnt >15:
			cnt =(pixMinGreen+10)
			print ("OOPS NOT ENOUGH LEAF PIXELS")

	print (minG, ratG, ratGb, "to select >",pixMinGreen," leaf pixels after", lpcnt, "loops")
	gavg=0
	gravg=0
	bravg=0
	if cnt==0: cnt=1
	for i in leafpix:
		r, g, b = i
		if r<1: r=g
		if g<1: g=0.1
		if b<1: b=g
		gavg=gavg+g
		gravg= gravg+(float(g)/float(r))
		bravg= bravg+(float(g)/float(b))

	gavg=float(gavg)/float(cnt)
	gravg=float(gravg)/float(cnt)
	bravg=float(bravg)/float(cnt)
	global ConsData
	#ConsData = [gavg, gravg, bravg]
	#print ConsData, "Values can be added to calib file"
	gavg= mgset*gavg+bgset
	if gavg <10: gavg=10
	minGscale.set(gavg)
	ratGscale.set(mgrset*gravg+bgrset)
	ratGbscale.set(mgbset*bravg+bgbset)

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
	ConsData = [gavg, gravg, bravg, ravg, rgavg]
	#print ConsData, "Values can be added to calib file"
	print (ravg, mmrset, bmrset, (mmrset*ravg+bmrset))
	#ratGbscale.set(0.334*bravg+0.534)
	return ConsData

def auto_Sing():
	global ConsData
	ConsData = [0,0,0,0,0]
	auto_Settings(ConsData)
	sing_Meas()
def calib_set():
	global mgset, bgset, mgrset, bgrset, mgbset, bgbset, mmrset, bmrset, mmrgset, bmrgset
	mgset, bgset, mgrset, bgrset, mgbset, bgbset, mmrset, bmrset, mmrgset, bmrgset = chos_calib()

#load calib file on first run
#mgset, bgset, mgrset, bgrset, mgbset, bgbset = load_calib()

#load calib file on first run
mgset, bgset, mgrset, bgrset, mgbset, bgbset, mmrset, bmrset, mmrgset, bmrgset = load_calib()

main = Tk()
main.title("Easy Leaf Area")

Frame1 = Frame(main)
Frame1.grid (row= 1, column = 1, rowspan = 17)


runsingbut = Button(Frame1, text ="Analyze with current settings", command = test_LA)

saveresults = Button(Frame1, text ="Save analysis", command = single_LA)

SObut = Button(main, text ="Open output csv file", command = show_Output)

singbut = Button(Frame1, text = "Open an image", command = chos_file)
singlabel = Label(Frame1)
###############################
loadcalibbut= Button(Frame1, text = "Load calib File", command = calib_set)

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
addTocalibbut = Button (Frame1,text = "Add to calib File", command =addTocalib)
###############

minG =100
minGscale = Scale(Frame3, from_=0, to=255, label="Leaf minimum Green RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 250, variable = minG )
minGscale.set(25)

minR =200
minRscale = Scale(Frame3, from_=0, to=255, label="Scale minimum Red RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 250, variable = minR )
minRscale.set(225)

ratG =1.2
ratGscale = Scale(Frame3, from_=0.9, to=2, resolution = 0.02, label="Leaf Green Ratio: (G/R)", orient=HORIZONTAL, tickinterval = 0.5, length = 200, variable = ratG )
ratGscale.set(1.05)

ratGb =1.35
ratGbscale = Scale(Frame3, from_=0.8, to=2, resolution = 0.02, label="Leaf Green Ratio: (G/B)", orient=HORIZONTAL, tickinterval = 0.5, length = 200, variable = ratGb )
ratGbscale.set(1.07)

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
loadcalibbut.grid(row=16, column = 1, pady=5)
addTocalibbut.grid(row=17, column =1, pady=5)
C6.grid(row=15, column = 3, pady=5)
##############
minGscale.grid(row=1, column =3)
ratGscale.grid(row=2, column =3)
ratGbscale.grid(row=3, column =3)
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
