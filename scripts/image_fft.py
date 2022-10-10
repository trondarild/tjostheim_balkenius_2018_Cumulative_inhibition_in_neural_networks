# Copied from:


from PIL import Image
import numpy as np
import scipy.fftpack as fp
#import pyfits
import pylab as py
import radialProfile

ix = "0002"
in_fn = lambda(ix): '../run_data/clooney_gen/clooney_gen_first_run/clooney_regen_' + ix + '.png'
out_fn = lambda(ix): '../run_data/clooney_gen/fft/clooney_fft_' + ix + '.png'
#fn = '../../pics/cifar_train/49999.png'
data = [ 
    #np.array(Image.open("../../pics/clooney32x32.jpg").convert("L")),\
    np.array(Image.open("../run_data/weight_img/C4-noise.png").convert("L"))\
    #, np.array(Image.open(in_fn(ix_start)).convert("L")),\
    #, np.array(Image.open(in_fn('0950')).convert("L")),\
    #, np.array(Image.open(in_fn(ix_end)).convert("L")) ]
    , np.array(Image.open(in_fn('1')).convert("L"))\
    , np.array(Image.open(in_fn('2')).convert("L"))\
    , np.array(Image.open(in_fn('3')).convert("L"))\
    , np.array(Image.open(in_fn('4')).convert("L"))\
    ]

def get_psd(image):
    # Take the fourier transform of the image.
    F1 = fp.fft2(image)

    # Now shift the quadrants around so that low spatial frequencies are in
    # the center of the 2D fourier transformed image.
    F2 = fp.fftshift( F1 )

    # Calculate a 2D power spectrum
    psd2D = np.abs( F2 )**2

    # Calculate the azimuthally averaged 1D power spectrum
    psd1D = radialProfile.azimuthalAverage(psd2D)
    
    return psd1D, psd2D

def gen_figures(data, pltix):


    image = data

    # Take the fourier transform of the image.
    #F1 = fp.fft2(image)

    # Now shift the quadrants around so that low spatial frequencies are in
    # the center of the 2D fourier transformed image.
    #F2 = fp.fftshift( F1 )

    # Calculate a 2D power spectrum
    #psd2D = np.abs( F2 )**2

    # Calculate the azimuthally averaged 1D power spectrum
    #psd1D = radialProfile.azimuthalAverage(psd2D)
    
    psd1D, psd2D = get_psd(image)
    # Now plot up both
    #

    py.subplot(pltix[0])
    py.imshow( np.log10( psd2D ))

    #py.figure(2)
    #py.clf()
    py.subplot(pltix[1])
    py.semilogy( psd1D )
    py.xlabel('Spatial Frequency')
    #py.ylabel('Power Spectrum')

    #py.figure(3)
    py.subplot(pltix[2])
    #py.clf()
    #py.imshow( np.log10( image ), cmap='Greys')
    py.imshow( image , cmap='gray')


fig = py.figure(1)
py.clf()
gen_figures(data[0], [331, 332, 333])
gen_figures(data[1], [334, 335, 336])
gen_figures(data[2], [337, 338, 339])
py.tight_layout()
fig.savefig('../figures/spatial-freq.eps', format='eps', dpi=1000)
py.show()
