import os, sys


#from Tkinter import Frame, Tk, Label, Button, Scale, HORIZONTAL, Checkbutton, IntVar
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageStat, ImageDraw, ImageFont
from PIL import TiffImagePlugin

from PIL import ImageTk

import scipy
from scipy import ndimage
#import matplotlib.pyplot as plt


def Show_pic(pic):	
	
	im = pic.copy()
	im.thumbnail((800,800), Image.ANTIALIAS)

	imtk=ImageTk.PhotoImage(im)

	label = Label(image=imtk, height =600, width = 800)
	label.image= imtk
	label.grid(row =5, rowspan=50, column =2)
	main.update()
	

def brightness(curFile):
   im = Image.open(curFile).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]
#def con_comp(concom, minPart)

def Pixel_check(curFile, dirF, file, keepdata):
	pic = Image.open(curFile)
	pic2= Image.open(curFile)
	picr= Image.open(curFile)
	#if (rotPic.get()):
	#	print "Rotating picture 180"
	#	pic = pic.rotate(180)
	#if (flipPic.get()):	
	#	print "Flipping picture"
	#	pic = pic.transpose(Image.FLIP_LEFT_RIGHT)
	imgdata = pic.load()
	print file," loaded"
	
	
	#Show_pic(pic)
	
	speedP=speedPscale.get()		
	xsize, ysize = pic.size
	xsize=xsize/speedP
	ysize=ysize/speedP
	pic=pic.resize((xsize,ysize))
	pic2=pic2.resize((xsize,ysize))
	picr=picr.resize((xsize,ysize))
	xsize, ysize = pic.size
	print xsize,"x", ysize
	minG=minGscale.get()
	minR=minRscale.get()
	ratG=ratGscale.get()
	ratGb=ratGbscale.get()
	ratR=ratRscale.get()
	print minG, minR, ratG, ratR
	pixels = pic.load() # create the pixel map
	leafpix = []
	scalepix = []
	backpix = []
	leafonly = pic2.load()
	scaleonly = picr.load()
	if (noRed.get()):
		minR = 255
		ratR = 2
	for i in range(pic.size[0]):    # for every pixel:
		for j in range(pic.size[1]):
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
	flat = scipy.misc.fromimage(pic2,flatten=1)
	flatr= scipy.misc.fromimage(picr,flatten=1)
	
	blobs, leaves = ndimage.label(flat)
	blobsr, scales = ndimage.label(flatr)	
	print "Number of blobs: ", leaves
	scalehist=ndimage.measurements.histogram(blobsr, 1,scales,scales) 
	cnt=1
	gcnt=0
	parcnt=0
	rCnt=0
	largescale = []
	if (noRed.get()<1):
		for s in scalehist:
		#	print s
		
			if s>1000:
				cnti=0
				cntj=0
				gcnt=0
				parcnt=parcnt+1
				print "big enough", cnt, s
				for i in range(pic.size[0]):    # for every pixel:
					for j in range(pic.size[1]):
						#gcnt= blobs[j,i]
						#print gcnt
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

	blobhist=ndimage.measurements.histogram(blobs, 1,leaves,leaves) 
	#print blobhist
	minPsize=minPscale.get()
	if minPsize>10:
		cnt=1
		gcnt=0
		parcnt=0
		gCnt=0
		largeleaf = []
		for s in blobhist:
		#	print s
			if s>minPsize:
				cnti=0
				cntj=0
				gcnt=0
				parcnt=parcnt+1
				print "big enough", cnt, s
				for i in range(pic.size[0]):    # for every pixel:
					for j in range(pic.size[1]):
						#gcnt= blobs[j,i]
						#print gcnt
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
			#print "Green blob", gcnt
		#print largeleaf
		leafprint= ', '.join(map(str, largeleaf))
	else:
		print "NO CONNECTED COMPONENT ANALYSIS"
		for i in leafpix:
			pixels[i] = (0,255,0)
		leafprint = "No connected component analysis"
	
	print gCnt, rCnt

	
	
	percarea = float(gCnt)/(xsize*ysize)*100
	print (xsize*ysize)
	print percarea
	
	#leafarea = float(gCnt)/float(rCnt)*0.1
	if rCnt < 1:
		leafarea= 0
	else:		
		leafarea = float(gCnt)/float(rCnt)*0.1
	################################################

		
	Show_pic(pic)
	highlightfile = dirF+'/Canopyarea.csv'
	pixdata=file+', '+str(gCnt)+', '+str(rCnt)+', '+'%.2f' % leafarea+','+'%.2f' % percarea+','+leafprint+'\n'

	return gCnt, rCnt, pic, pixdata, leafarea, percarea
def single_LA(keepdata):
	print "Measuring..."
	global chosfile
	global dirF
	
	#get absolute path
	dirF = os.path.dirname(chosfile)

	pic = Image.open(chosfile)
	xsize, ysize = pic.size
	file = os.path.basename(chosfile)
	imagebright = brightness(chosfile)
	(gCnt, rCnt, pic, pixdata, leafarea, percarea) = Pixel_check(chosfile, dirF, file, keepdata)
		#Math	
	#if rCnt < 1:
	#	leafarea= 0
	#else:		
	#	leafarea = float(gCnt)/float(rCnt)*0.1
		
		
	#if rCnt <2:
	#	rCnt = 0
	
	
	filelabel= Label (main, height =1, width=60)

	
	speedP=speedPscale.get()		
	xsize=xsize/speedP
	ysize=ysize/speedP
	filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
	filelabel.grid (row =1, column =2)
	Pixlabel = Label(main, height = 1, width = 80)
	Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "m^2"+ "    Percent Cover: "+ '%.2f' % percarea+ "%")

	Pixlabel.grid(row =2, column =2)
	highlightfile = dirF+'/Canopyarea.csv'
	if keepdata:
		try:
			with open(highlightfile, "a") as f:
				f.write("filename,total green pixels,red pixels (0.1 m^2),leaf area m^2, % cover, Component green pixels:")
				f.write("\n")
		except:
			open (dirF+'/Canopyarea.csv', "w")
			print "creating new output file"
			with open(highlightfile, "a") as f:
				f.write("filename,total green pixels,red pixels (0.1 m^2),leaf area m^2, % cover, Component green pixels:")
				f.write("\n")
		save_Output(highlightfile, file, pixdata, pic, dirF)
	print imagebright

	print "Finished processing image"

def run_LA():
	print "Measuring..."
	global dirS
	global dirF
	global chosfile

	keepdata=1
	#get absolute path
	dirS = os.path.abspath(dirS)
	dirF = os.path.abspath(dirF)
	#get list of files in dirS
	filesInCurDir = os.listdir(dirS)
	try:
		with open(dirF+'/Canopyarea.csv', "a") as f:
			f.write("filename,total green pixels,red pixels (0.1 m^2),leaf area m^2, % cover, Component green pixels:")
			f.write("\n")
	except:
		open (dirF+'/Canopyarea.csv', "w")
		with open(dirF+'/Canopyarea.csv', "a") as f:
			f.write("filename,total green pixels,red pixels (0.1 m^2),leaf area m^2, % cover, Component green pixels:")
			f.write("\n")
	

	for file in filesInCurDir:
		
		curFile = os.path.join(dirS, file)
		#open picture and load file
		try:
			pic = Image.open(curFile)
			xsize, ysize = pic.size
		except:
			continue
		Show_pic(pic)
		
		chosfile = curFile
		if (autocheck.get()):
			auto_Settings()
		(gCnt, rCnt, pic, pixdata, leafarea, percarea)  = Pixel_check(curFile, dirF, file, keepdata)
		#Math	
		#if rCnt < 1:
		#	rCnt+=1
		#leafarea = float(gCnt)/float(rCnt)*4.0
		
		
		#if rCnt <2:
		#	rCnt = 0
			
		filelabel= Label (main, height =1, width=60)
		
		speedP=speedPscale.get()		
		xsize=xsize/speedP
		ysize=ysize/speedP
		filelabel.configure (text = file+" "+str(xsize)+ "x"+str(ysize))
		filelabel.grid (row =1, column =2)
		Pixlabel = Label(main, height = 1, width = 80)
		#Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "cm^2")
		Pixlabel.configure (text = "Leaf pixels: "+ str(gCnt)+ "   Scale pixels: "+ str(rCnt)+ "    Leaf area: "+ '%.2f' % leafarea+ "m^2"+ "    Percent Cover: "+ '%.2f' % percarea+ "%")
		Pixlabel.grid(row =2, column =2)
		#write file name, pixel info, and leaf area to text file
		highlightfile = dirF+'/Canopyarea.csv'

		save_Output(highlightfile, file, pixdata, pic, dirF)

	print "Finished processing images"
	
def S_dir():
	global dirS
	dirS = askdirectory()
	Slabel.configure(text = dirS)
def F_dir():
	global dirF
	dirF = askdirectory()
	Flabel.configure(text = dirF)
def check_Sett():
	print "Batch processing"
	run_LA()
def chos_file():
	global chosfile
	chosfile = askopenfilename(filetypes=[("JPEG", "*.jpg; *.jpe; *.jpeg"), ("TIFF", "*.tiff; *.tif")])

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
	print "loaded   "+chosfile
def sing_Meas():
	print "Measuring image"
	keepdata=0
	single_LA(keepdata)
def show_Output():
	global dirF
	print dirF
	print "Opening output file in default application"
	outputfile = 'start '+dirF+'/Canopyarea.csv'
	os.system(outputfile)

def save_Output(highlightfile, file, pixdata, pic, dirF):
	print "save output"

	with open(highlightfile, "a") as f:
		f.write(pixdata)
	tifffile = file.replace('.jpg', '.tiff')
	pic.save(dirF+'/highlight'+tifffile)
def auto_Settings():		
	global chosfile

	pic = Image.open(chosfile)
	
	#imgdata = pic.load()
	speedP=8		
	xsize, ysize = pic.size
	xsize=xsize/speedP
	ysize=ysize/speedP
	pic=pic.resize((xsize,ysize))
	xsize, ysize = pic.size
	print xsize,"x", ysize
	ratG=2
	ratGb=1.8
	minG = 75
	cnt =0
	lpcntb = 0
	lpcnt =0
	pixels = pic.load() # create the pixel map
	print"Conservative settings:"

	
	minGscale.set(15)	
	ratGscale.set(1.04)
	ratGbscale.set(1.04)
	#minPscale.set(300)
	#ratGbscale.set(-0.122*bravg*bravg+1.057*bravg-0.427)
	###################################################################
	ratR=2
	minR = 150
	cnt =0
	lpcntb = 0
	lpcnt =0
	print"Conservative settings scale:"
	print "minR, ratR"
	scalepix=[]
	if (noRed.get()<1):
		while cnt <200:
			print minR, ratR
			print lpcnt
			scalepix=[]
			for i in range(pic.size[0]):    # for every pixel:
				for j in range(pic.size[1]):
					r, g, b = pixels[i,j]
					#pixels[i,j] = (i, j, 100) # set the colour accordingly
					if g*ratR < r and b*(ratR)< r  and r> minR:
					#if r*ratG < g and b*ratGb<g  and g> minG:
						scalepix.append((r,g,b))
					
			cnt=len(scalepix)
			lpcnt=lpcnt+1
			if lpcnt <3:
				ratR = 0.96*ratR
				#ratGb = 0.939*ratGb
			#if lpcnt >7:
			#	ratR = 2
			#	minR = 0.99*minR
			if lpcnt >3:
				cnt =201
				scalepix=[]
				print "NO RED SCALE FOUND"
	ravg=0
	gravg=0
	bravg=0
	cnt=len(scalepix)
	if cnt>0: 
		for i in scalepix:
			r, g, b = i
			if g<1: g=r
			if b<1: b=r
			ravg=ravg+r
			gravg= gravg+(float(r)/float(g))
			bravg= bravg+(float(r)/float(b))
		
		ravg=float(ravg)/float(cnt)
		gravg=float(gravg)/float(cnt)
		bravg=float(bravg)/float(cnt)
		gravg=(gravg+bravg)/2
		print "ravg rRatioAvg"
		print ravg, gravg
		gravg=0.134*gravg+0.782
		if gravg <1.011: gravg=1.01
		minRscale.set(1.412*ravg-140.6)	
		ratRscale.set(gravg)
	else:
		minRscale.set(255)	
		ratRscale.set(2)
	#ratGbscale.set(0.334*bravg+0.534)

def auto_Sing():		
	auto_Settings()
	sing_Meas()
	
main = Tk()
main.title("Canopy Area")


Frame1 = Frame(main)
Frame1.grid (row= 1, column = 1, rowspan = 15)


runsingbut = Button(Frame1, text ="Analyze with current settings", command = lambda: single_LA(0))

saveresults = Button(Frame1, text ="Save analysis", command = lambda:single_LA(1))

SObut = Button(main, text ="Open output csv file", command = show_Output)

singbut = Button(Frame1, text = "Open an image", command = chos_file)
singlabel = Label(Frame1)


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
Frame3.grid (row= 1, column = 3, rowspan = 7)


minG =100
minGscale = Scale(Frame3, from_=0, to=255, label="Leaf minimum Green RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 200, variable = minG )
minGscale.set(25)

minR =200
minRscale = Scale(Frame3, from_=0, to=255, label="Scale minimum Red RGB value:", orient=HORIZONTAL, tickinterval = 50, length = 200, variable = minR )
minRscale.set(225)

ratG =1.2
ratGscale = Scale(Frame3, from_=1, to=2, resolution = 0.01, label="Leaf Green Ratio: (G/R)", orient=HORIZONTAL, tickinterval = 0.5, length = 150, variable = ratG )
ratGscale.set(1.05)

ratGb =1.35
ratGbscale = Scale(Frame3, from_=1, to=2, resolution = 0.01, label="Leaf Green Ratio: (G/B)", orient=HORIZONTAL, tickinterval = 0.5, length = 150, variable = ratGb )
ratGbscale.set(1.07)

ratR =1.3
ratRscale = Scale(Frame3, from_=1, to=2, resolution = 0.01, label="Scale Red Ratio: (R/G & R/B)", orient=HORIZONTAL, tickinterval = 0.5, length = 150, variable = ratR )
ratRscale.set(1.95)

speedP =1
speedPscale = Scale(Frame3, from_=1, to=8, resolution = 1, label="Processing Speed:", orient=HORIZONTAL, tickinterval = 1, length = 150, variable = speedP )
speedPscale.set(4)

minPsize =500
minPscale = Scale(Frame3, from_=1, to=5000, resolution = 10, label="Minimum Leaf Size (pixels):", orient=HORIZONTAL, tickinterval = 1000, length = 200, variable = minPsize )
minPscale.set(301)
#flipPic = IntVar()

#C1 = Checkbutton(Frame1, text = "Flip image horizontal", variable = flipPic)
#flipPic.get()

#FieldPic = IntVar()
#CField = Checkbutton(Frame1, text = "Canopy auto settings algorithm", variable = FieldPic)
#FieldPic.get()

noRed = IntVar()
C2 = Checkbutton(Frame1, text = "No Red Scale", variable = noRed)
C2.select()
noRed.get()

delBack = IntVar()
C3 = Checkbutton(Frame1, text = "Delete background", variable = delBack)
delBack.get()

labpix = IntVar()
C5 = Checkbutton(main, text = "Label Pixels", variable = labpix)
labpix.get()


autosetbut = Button(Frame1, text ="Auto settings", command = auto_Sing)

autocheck = IntVar()
C4 = Checkbutton(Frame1, text = "Use auto settings", variable = autocheck)
autocheck.get()



singbut.grid(row=1, column =1, pady=5)
autosetbut.grid(row=2, column =1, pady=5)
#CField.grid(row=3, column =1, pady=5)
runsingbut.grid(row=4, column =1, pady=5)
saveresults.grid(row=5, column =1, pady=5)
#C1.grid(row=6, column =1, pady=5)
C2.grid(row = 7, column =1, pady=5)
C3.grid(row=8, column = 1, pady=5)

Batchlabel.grid(row=9, column=1, pady=10)
Sbut.grid(row=10, column=1, pady=5)
Slabel.grid(row=11, column=1, pady=5)
Fbut.grid(row=12, column=1, pady=5)
Flabel.grid(row=13, column=1, pady=5)
CSbut.grid(row=14, column=1, pady=5)
C4.grid(row=15, column = 1, pady=5)



minGscale.grid(row=1, column =3)
ratGscale.grid(row=2, column =3)
ratGbscale.grid(row=3, column =3)
minRscale.grid(row=4, column =3)
ratRscale.grid(row=5, column =3)
speedPscale.grid(row=6, column=3)
minPscale.grid(row=7, column = 3)




filelabel= Label (main, height =1, width=100)

filelabel.configure (text = " ")
filelabel.grid (row =1, column =2)
SObut.grid(row=3, column =2)
C5.grid(row=4, column = 2)
main.mainloop()