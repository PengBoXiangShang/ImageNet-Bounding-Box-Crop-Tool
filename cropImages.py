"""
Crops the images in subfolders of current directory according to annotations in 'Annotation' Folder and places then in 'Cropped'
Instructions: 
	1.In an empty directory, store this script and all the folders containing the images that will be processed
	2.In the same directory, add the \Annotation\ folder, containing a respective folder for each one in the directory, which in turn contain the annotation files
	3.run python cropImages.py
	4.Output will be in \Cropped\
"""
import os
from PIL import Image
import xml.etree.ElementTree as ET
import sys

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


rootdir = os.getcwd()
CroppedFolder = "Cropped"
Annotation = "Annotation"
if not os.path.exists(CroppedFolder):
    os.makedirs(CroppedFolder)
    print 'Created "/Cropped/" directory'

for directory in get_immediate_subdirectories(rootdir):	#loop over all dirs
		if directory != CroppedFolder and directory != Annotation:
			print "Processing Directory: " + directory
			if not os.path.exists(os.path.join(CroppedFolder, directory)):
    				print 'Created "/Cropped/' + directory + '" directory'
    				os.makedirs(os.path.join(CroppedFolder, directory))
			for filename in os.listdir(directory):
				basename =  os.path.splitext(filename)[0]
				try:
					file = open ( os.path.join( Annotation, directory, basename))
					# added by Peng, on 27-04-2018.
					print basename
					print '-------'
					print type(basename)
					raise RuntimeError
					root = ET.fromstring(file.read())
					file.close()
					xmin = int (root.find('object').find('bndbox').find('xmin').text)
					ymin = int (root.find('object').find('bndbox').find('ymin').text)
					xmax = int (root.find('object').find('bndbox').find('xmax').text)
					ymax = int (root.find('object').find('bndbox').find('ymax').text)

					# comment by Peng, on 27-04-2018.
					# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.find
					# find(match) Finds the first subelement matching match. match may be a tag name or path. Returns an element instance or None.
					# added by Peng, on 27-04-2018
					object_name = root.find('object').find('name').text
					print object_name
					print "-----------"
					category_name = basename.split('_', 1)[0]
					print category_name
					raise RuntimeError
					if object_name != category_name:
						continue

					img =  Image.open( os.path.join(directory, filename) )
					cropped = img.crop((xmin, ymin, xmax, ymax))
					cropped = cropped.resize((224, 224)) # added by Peng, on 25-04-2018.
					save_file = open (os.path.join(CroppedFolder, directory, filename), 'w')
					cropped.save(os.path.join(CroppedFolder, directory, filename), "JPEG")
					save_file.close()


				except Exception, e:
					print "Exception encountered at basename " + basename + " with path as " +  os.path.join( Annotation, directory, basename) 
					print "Unexpected error:", str(e)

