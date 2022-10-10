#
# generate average spatial frequency 
#

import image_fft as fft
import visualize_csom_weights as viz
import numpy as np
import pylab as py

def get_img_array(generate, tmpfilename):
    if gen:
        path = '/Users/tr1445tj/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/weights/tmp'
        filename = 'C4_CIFAR_C1(rf(3-3)_inc(1-1)_som(12-3)_block(3-3)_span(0-0))C2(rf(36-9)_inc(12-3)_som(20-10)_(block(12-3)_span(24-6))C3(rf(40-20)_inc(20-10)_som(24-12)_block(20-10)_span(100-50))C4(rf(48-24)_inc(24-12)_som(16-8)_block(24-12)_span(264-132)).dat'
        maxlayer = 4
        # get the array
        image_array = viz.get_weight_image_array(path, filename, maxlayer)
        #image_array = np.random.rand(2,2,10,10)
        # write to file
        fileobj = open(tmpfilename, 'w')
        np.save(fileobj, image_array)
        fileobj.close()
        return image_array
    else:
        fileobj = open(tmpfilename, 'r')
        image_array = np.load(fileobj)
        fileobj.close()
        return image_array

if __name__ == '__main__':
    gen = False
    image_array = get_img_array(gen, 'tmp.npy')
    
    som_rows = image_array.shape[0]
    som_cols = image_array.shape[1]
    fft_data_avg = [] #np.array((som_rows))
    fft_data_cols = [] #np.array((som_cols))

    for row in range(som_rows):
        for col in range(som_cols):
            img = image_array[row][col]
            psd1D, psd2D = fft.get_psd(img)
            #print psd1D
            fft_data_cols.extend([psd1D])
        # do avg and store
        #print np.asarray(fft_data_cols)
        fft_data_avg.extend( [np.mean(np.asarray(fft_data_cols), axis=0)])
    py.figure(1)
    py.clf()
    fig_rows = 2
    fig_cols = 4
    
    for i in range(len(fft_data_avg)):
        #py.subplot(len(fft_data_avg), 1, i) 
        py.subplot(fig_rows, fig_cols, i+1) 
        py.ylim( (pow(10,-4),pow(10,2)) )
        py.semilogy( fft_data_avg[i] )
        if i>fig_cols-1: py.xlabel('Spatial Frequency')
    py.show()
    # print fft_data_avg[0]
    # TODO generate plots
    # plot 