Easy-Leaf-Area
==============
Privacy Policy

No data is collected or reported to Easy Leaf Area, but Apple and Google now require a Privacy Policy.  

We take your privacy very seriously. We do not collect, use, or disclose your personal information when you use our applications. By using these apps, you consent to the terms of this Privacy Policy.

Easy Leaf Area Free and Canopy Cover Free require camera and location access in order to calculate leaf area, canopy cover, and location locally on your device.  No data is collected or reported to Easy Leaf Area.

Contact Us
If you have any questions or concerns about this Privacy Policy or our practices with respect to your personal information, please contact me at heaslon@gmail.com. 

April 11 2023 - Easy Leaf Area is now available in the App Store for iPhone
https://apps.apple.com/us/app/easy-leaf-area/id6447322411

April 14 2023 - Canopy Cover is now available in the App Store for iPhone
https://apps.apple.com/us/app/canopy-cover/id6447323877

Easy Leaf Area App tutorial: https://www.youtube.com/watch?v=HePyToRoa84&t
Canopy Cover App tutorial: https://www.youtube.com/watch?v=oNxopqB1qY0&t

2023 updates completed for Python scripts.  These updates should fix compatibility issues with Python 3, windows 10 or 11, and Mac OS.  

Android apps compatible with newer phones will be released later this year.


Easy Leaf Area Free and Canopy Cover Free are now available for android devices.
https://play.google.com/store/apps/details?id=com.heaslon.EasyLeafArea

https://play.google.com/store/apps/details?id=com.heaslon.canopycover

WHAT IS EASY LEAF AREA?
Easy leaf area is free, open source, software that rapidly measures leaf area in digital images (photographs or scanner images).  Easy leaf area uses the RGB value of each pixel to identify leaf and scale regions in each image.  After analysis, each highlighted image is written in tiff format to the 'write folder'.  A file named 'leafarea.csv' with image names, leaf pixel counts, scale pixel counts, and leaf area in cm^2 is also written to the 'write folder'. Multiple leaves can be measured in the same image (see MULTIPLE LEAVES section).

GETTING STARTED:
This program analyzes single jpeg or tiff images or batches of images for leaf area.  Images must have a red scale of known area in the image in the same plane as the leaves for the program to use as a reference scale.  

Windows (2024 updated): ela.exe no longer works on Windows 10 or Windows 11.  You will need to install python and run the script.  I would suggest using elaWin2023.py compatible with Python 3.  Use ChatGPT for instructions on installing Scipy, Numpy, Pillow

Windows (old instructions):
Download EasyLeafArea.zip and unzip the folder.  https://github.com/heaslon/Easy-Leaf-Area/blob/master/EasyLeafArea.zip .  To download the file click 'view the full file'.  To begin the program, Run ela.exe or ela.py (requires installation of Python® 2.7 ("Python" is a registered trademark of the Python Software Foundation”), Scipy, and Numpy, but you can modify the script to suit your needs).

Mac (2024 updated): the mac executable may no longer work on modern macs.  You will need to install python and run the script.  I would suggest using elaMac2024.py compatible with Python 3.  Use ChatGPT for instructions on installing Scipy, Numpy, Pillow

Mac (old instructions):
Download mac executable 'ela'  https://github.com/heaslon/Easy-Leaf-Area/blob/master/ela . To download the file click 'view the full file'.  Double click the file to launch easy leaf area.  If the file will not launch due to your security settings follow the instructions here: https://support.apple.com/kb/PH14369?locale=en_US .  If the file opens as a text file, follow the instructions here: http://macosx.com/threads/change-a-plain-text-file-to-unix-executable-file.318118/ .

Windows and Mac:
Open a single image by clicking the ‘Open an image’ button and navigating to and selecting the image.  Adjust the ‘Scale area’ slider to the actual area of your red scale (It is set to 4.0 cm^2 when the program opens).  Clicking ‘Auto settings’ will move the sliders on the right based on data in the image and measure leaf area.  To calibrate ‘Auto settings’ see the AUTO SETTINGS CALIBRATION section below.  After processing, the scale areas in the image should be red and the leaf areas green.  If the automatic settings failed to identify all leaf area or scale area or identified background objects as scale or leaf area, you can manually adjust the settings sliders (See section on IMAGE ANALYSIS SETTINGS) on the right and click on the ‘Analyze with current settings’ button to rerun the analysis. Scale and leaf areas should be recolored based on your manual settings.  If small groups of background pixels are misidentified as leaf area, they can be removed by selecting a ‘minimum leaf size’ greater than zero (WARNING: if there are many groups of misidentified background pixels, this can significantly add to processing time).  Alternatively, if you only have one leaf per image, you can check ‘Only one leaf component’ and only the largest green component will be measured.  To save the output ‘.tiff’ image and the pixel counts and leaf areas to a ‘.csv’ file, click on ‘Save analysis’.  You can always click on “Save analysis’ first if you are confident that your settings will work.  Only one image can be opened at a time, so you do not need to close one image before opening another.

BATCH PROCESSING:
To batch analyze images for leaf area, first find settings that work for a few images you want to batch analyze or check use auto settings.  When you are happy with the settings, select the source folder with images to analyze.  Also select the write folder where highlighted output ‘.tiff’images and the ‘.csv’ output files will be saved.
***known bug***  If you open a single image with the ‘Open an image’ button after selecting the write folder, the write folder will change to the directory of the image you just opened.  You will have to reselect the write folder before running a batch if you don't want images saved to the most recently opened directory.  
Click ‘Start batch with current settings’ and images should start loading and processing.  Each image should take 0.5-5 seconds to analyze depending on the size of the image and the processing speed selected. 

MUTLIPLE LEAVES:
Multiple leaves can be measured in the same image, if a minimum leaf size (pixels) greater than 0 is selected.  During analysis, connected component analysis determines the size of groups of green leaf pixels.  Groups of green pixels larger than the minimum size will be recolored and the size of each group output to the ‘.csv’ file when data is saved. You can also opt to write the number of pixels in each group on the output image by checking the ‘label pixels’ box in the top center of the program. Setting the ‘minimum leaf size’ setting at 0 skips the connected component analysis.  

IMAGE ANALYSIS SETTINGS:
The top five sliders (See DEFINITIONS) can be adjusted to increase or decrease the pixels identified by the program as leaf (green) or scale (red).  Adjusting the sliders will not change the analysis until you click the ‘Analyze with current settings’ or ‘Save analysis’ button.  If you don’t know what settings will work well for your images, use the ‘auto settings’ button on the left before manually adjusting sliders.  
See definitions below if you are not sure what each of the sliders does.

AUTO SETTINGS CALIBRATION:
The auto setting calibration was derived from a set of Arabidopsis images, but you can change the auto settings calibration to work better for your image set.  You will need to manually adjust slider settings to select all of your leaf area and scale area then add these settings to ‘newcalib.csv’ by clicking on the ‘Add to calib file’ button. If ‘newcalib.csv’ does not exist in the current directory, it will be created.  After adding manual settings from at least 5 images in your image set, you can implement the new calibration by clicking on the ‘Load calib file’ button.  If you would like to make this calibration the new default calibration, rename it ‘calib.csv’ and copy it to the same directory as leafarea.exe (or leafarea.py if you are running the script).  This calibration will automatically load the next time you start Easy Leaf Area. 

If the calibration performs poorly, plot the 1st and 4th, 2nd and 5th, and 3rd and 6th, 7th and 9th, and 8th and 10th columns in the the calibration file.  Delete rows with outliers, save your calibration file, and click on the ‘Load calib file’ button again.  If the calibration still performs poorly, you probably need to add settings from more images in your image set to the calibration.  

DEFINITIONS:
'leaf minimum Green RGB value' refers to the G in the RGB value of each pixel.  Lowering 'leaf minimum Green RGB value' highlights darker green pixels.  Lowering 'Leaf Green Ratio's highlights more yellow-green and grey-green pixels.

'Scale minimum Red RGB value' refers to the R in the RGB value of each pixel.  Lowering 'Scale minimum Red RGB value' highlights darker red pixels.  Lowering 'Scale Red Ratio' highlights more grey-red pixels.

'Flip image horizontal' flips the output images horizontally.
'Rotate image 180 deg' turns the output images upside down.

‘Scale area (cm^2)’ is used to set the area of your red scale in cm^2.
'Select processing Speed' resizes images prior to processing to increase processing speed.  A processing speed of 1 does not resize images, but will take longer to process.

QUESTIONS:
If you have any questions about Easy leaf area, you can contact the author, Hsien Ming Easlon, at heaslon@gmail.com.  Make sure you include ‘easy leaf area’ in the subject line.


Easy Leaf Area license
Copyright © 2012, 2013, University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the Easy Leaf Area Developers nor the names of any contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


SciPy license
Copyright © 2001, 2002 Enthought, Inc.
All rights reserved.

Copyright © 2003-2013 SciPy Developers.
All rights reserved.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Numpy license
Copyright © 2005-2013, NumPy Developers.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the NumPy Developers nor the names of any contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Python License (Python-2.0)
Python License, Version 2 (Python-2.0)
PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------
1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.
2. Subject to the terms and conditions of this License Agreement, PSF
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use Python
alone or in any derivative version, provided, however, that PSF's
License Agreement and PSF's notice of copyright, i.e., "Copyright (c)
2001, 2002, 2003, 2004, 2005, 2006 Python Software Foundation; All Rights
Reserved" are retained in Python alone or in any derivative version
prepared by Licensee.
3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.
4. PSF is making Python available to Licensee on an "AS IS"
basis. PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.
5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.
7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee. This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.
8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.
BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0
-------------------------------------------
BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1
1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an
office at 160 Saratoga Avenue, Santa Clara, CA 95051, and the
Individual or Organization ("Licensee") accessing and otherwise using
this software in source or binary form and its associated
documentation ("the Software").
2. Subject to the terms and conditions of this BeOpen Python License
Agreement, BeOpen hereby grants Licensee a non-exclusive,
royalty-free, world-wide license to reproduce, analyze, test, perform
and/or display publicly, prepare derivative works, distribute, and
otherwise use the Software alone or in any derivative version,
provided, however, that the BeOpen Python License is retained in the
Software, alone or in any derivative version prepared by Licensee.
3. BeOpen is making the Software available to Licensee on an "AS IS"
basis. BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.
4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY
DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
5. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.
6. This License Agreement shall be governed by and interpreted in all
respects by the law of the State of California, excluding conflict of
law provisions. Nothing in this License Agreement shall be deemed to
create any relationship of agency, partnership, or joint venture
between BeOpen and Licensee. This License Agreement does not grant
permission to use BeOpen trademarks or trade names in a trademark
sense to endorse or promote products or services of Licensee, or any
third party. As an exception, the "BeOpen Python" logos available at
http://www.pythonlabs.com/logos.html may be used according to the
permissions granted on that web page.
7. By copying, installing or otherwise using the software, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.
CNRI OPEN SOURCE LICENSE AGREEMENT (for Python 1.6b1)
--------------------------------------------------
IMPORTANT: PLEASE READ THE FOLLOWING AGREEMENT CAREFULLY.
BY CLICKING ON "ACCEPT" WHERE INDICATED BELOW, OR BY COPYING,
INSTALLING OR OTHERWISE USING PYTHON 1.6, beta 1 SOFTWARE, YOU ARE
DEEMED TO HAVE AGREED TO THE TERMS AND CONDITIONS OF THIS LICENSE
AGREEMENT.
1. This LICENSE AGREEMENT is between the Corporation for National
Research Initiatives, having an office at 1895 Preston White Drive,
Reston, VA 20191 ("CNRI"), and the Individual or Organization
("Licensee") accessing and otherwise using Python 1.6, beta 1
software in source or binary form and its associated documentation,
as released at the www.python.org Internet site on August 4, 2000
("Python 1.6b1").
2. Subject to the terms and conditions of this License Agreement, CNRI
hereby grants Licensee a non-exclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display
publicly, prepare derivative works, distribute, and otherwise use
Python 1.6b1 alone or in any derivative version, provided, however,
that CNRIs License Agreement is retained in Python 1.6b1, alone or
in any derivative version prepared by Licensee.
Alternately, in lieu of CNRIs License Agreement, Licensee may
substitute the following text (omitting the quotes): "Python 1.6,
beta 1, is made available subject to the terms and conditions in
CNRIs License Agreement. This Agreement may be located on the
Internet using the following unique, persistent identifier (known
as a handle): 1895.22/1011. This Agreement may also be obtained
from a proxy server on the Internet using the
URL:http://hdl.handle.net/1895.22/1011".
3. In the event Licensee prepares a derivative work that is based on
or incorporates Python 1.6b1 or any part thereof, and wants to make
the derivative work available to the public as provided herein,
then Licensee hereby agrees to indicate in any such work the nature
of the modifications made to Python 1.6b1.
4. CNRI is making Python 1.6b1 available to Licensee on an "AS IS"
basis. CNRI MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, CNRI MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR
FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON 1.6b1
WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE
SOFTWARE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING PYTHON 1.6b1,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY
THEREOF.
6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.
7. This License Agreement shall be governed by and interpreted in all
respects by the law of the State of Virginia, excluding conflict of
law provisions. Nothing in this License Agreement shall be deemed
to create any relationship of agency, partnership, or joint venture
between CNRI and Licensee. This License Agreement does not grant
permission to use CNRI trademarks or trade name in a trademark
sense to endorse or promote products or services of Licensee, or
any third party.
8. By clicking on the "ACCEPT" button where indicated, or by copying,
installing or otherwise using Python 1.6b1, Licensee agrees to be
bound by the terms and conditions of this License Agreement.
ACCEPT
CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2
--------------------------------------------------
Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam,
The Netherlands. All rights reserved.
Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.
STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
