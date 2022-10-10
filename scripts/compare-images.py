#!/usr/bin/env python
"""Compare two aligned images of the same size.

Usage: python compare.py first-image second-image

# note: use to get 
"""

import sys

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
from scipy import spatial
from os import listdir
from os.path import isfile, join
import csv
import matplotlib.pyplot as plt
import numpy as np

def get_filenames(mypath):
    return [ f for f in listdir(mypath) if isfile(join(mypath,f)) and not f[0]=='.' ]

def write_csv(data, filename):
    it = 1
    with open(filename,'wb') as file:
        file.write( 'it,rms\n')
        for num in data:
            file.write(str(it) + ',' + str(num))
            file.write('\n')
            it+=1

    # with open(filename, "wb") as csv_file:
    #     writer = csv.writer(csv_file, delimiter=',')
    #     for line in data:
    #         print line
    #         #writer.writerow(str(line))

def compare_images(img1, img2):
    # normalize to compensate for exposure difference
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = 0 #norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def cosine_sim(img1, img2):
    img1 = normalize(img1)
    img2 = normalize(img2)
    set1 = np.array(img1).ravel()
    #print set1.shape

    set2 = np.array(img2).ravel()
    #print set2.shape
    return 1 - spatial.distance.cosine(set1, set2)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

def plot(lst):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(lst, color='lightblue', linewidth=3)
    plt.show()

def do_comparison(img1):
    
    compare_vals = []
    for file2 in file2list:
        img2 = to_grayscale(imread(file2dir + file2).astype(float))
        # crop img2

        img2 = img2[5:31,7:29]
        #print np.array(img2).shape
        
        #print np.array(img1).shape

        # compare
        #n_m, n_0 = compare_images(img1, img2)
        #compare_vals.append(n_m)
        # cosine distance
        #img2 = np.random.rand(32,32)
        cos_sim = cosine_sim(img1, img2)
        #print cos_sim
        #break
        compare_vals.append(cos_sim)
        
        #print "Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size
        # print "Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size
    write_csv(compare_vals, "cos_sim_crp.csv")
    
    #plot(compare_vals)
    

def do_rnd(img1):
    compare_vals = []
    for i in range(0,2000):
        img2 = np.random.rand(26,22)
        cos_sim = cosine_sim(img1, img2)
        #print cos_sim
        #break
        compare_vals.append(cos_sim)
    print np.mean(compare_vals)

def do_blnk(img1):
    compare_vals = []
    #for i in range(0,2000):
    img2 = np.ones((26,22))*0.5
    
    cos_sim = cosine_sim(img1, img2)
    #print cos_sim
    #break
    compare_vals.append(cos_sim)
    print np.mean(compare_vals)    
        
def main():
    # read file to compare with
    file1 = "../../pics/clooney32x32.jpg"
    # read all generated files
    file2dir = "../run_data/clooney_gen/clooney_gen_first_run/"
    file2list = get_filenames(file2dir)

    #file1, file2 = sys.argv[1:1+2]
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = to_grayscale(imread(file1).astype(float))
    img1 = img1[3:29,5:27]
    #compare_vals = do_comparison(img1)
    #do_rnd(img1)
    do_blnk(img1)


    print "done"
if __name__ == "__main__":
    main()