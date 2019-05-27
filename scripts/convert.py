import os
from os import walk, getcwd
from PIL import Image
import hashlib
import json

classes = ["evzone"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = "data/evzones_dataset/evzones/ann/"
imgpath = "data/evzones_dataset/evzones/img"
outpath = "data/evzones_dataset/evzones/ann_txt/"

cls = "evzone"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()

list_file = open('%s/%s_list.txt'%(wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print("\n---- files  ----")
print(txt_name_list)
print("---- end files ----\n")

img_name = ''
""" Process """
for txt_name in txt_name_list:

    img_name = txt_name.replace('.json', '')

    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path + "\n")

    with open(txt_path, "r") as read_file:
        data = json.load(read_file)

    objects = data['objects'] #annotated bbox(es)
    size = data['size']

    """ Open output text files """
    txt_outpath = outpath + txt_name.replace('jpg.json', 'txt')
    txt_outfile = open(txt_outpath, "w")
    print("Output:" + txt_outpath + "\n")

    
    """ Convert the data to YOLO format """
    ct = 0
    for obj in objects:
        
        ct = ct + 1
        # [[left, top], [right, bottom]]
        
        xmin = obj['points']['exterior'][0][0]
        xmax = obj['points']['exterior'][1][0]
        ymin = obj['points']['exterior'][0][1]
        ymax = obj['points']['exterior'][1][1]        

        w= size['width'] 
        h= size['height'] 

        print(w, h)

        b = (float(xmin), float(xmax), float(ymin), float(ymax))
        bb = convert((w,h), b)

        print(bb)

        txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')  

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write( str('%s/%s/%s\n'%(wd, imgpath, img_name ) ) )
                
list_file.close()       
