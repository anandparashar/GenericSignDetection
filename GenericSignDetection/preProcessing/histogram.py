import math
import numpy as np
import cv2
import scipy.stats as stats

'''  Estimates edge threshold from image gradient

    img - Source image
    returns: Scalar threshold value

'''
def estimateThreshold(img):
    # Blur image and calculate Sobel gradient magnitude
    blurred = cv2.GaussianBlur(img, (3, 3), 1.5)
    grad_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0)
    grad_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1)

    if  (len(img.shape) > 2):
        grad_d = abs(grad_x)**2 + abs(grad_y)**2
        grad_d = np.sum(grad_d, axis=2)
        grad_d = np.sqrt(grad_d)
    else:
        grad_d = abs(grad_x ) + abs(grad_y)

    # Flatten and sort array
    gsorted = grad_d.flatten()
    gsorted.sort()

    # Threshold value will leave the upper 10% of edge pixels intact
    threshold = gsorted[ int(gsorted.size*0.94)]
    return threshold

''' Calculates a 32 bin histogram from a grayscale image 
    
    img - Source image
    
    returns: Array representing histogram
'''

'''
    Attempts to perform contrast and luminance correction on an image via an adaptive MSRCR algorithm
    
    img - Source image to correct
    kernSize - Size of the Gaussian kernel for the MSRCR reflectance calculation
    big_k - Kernel scalar
    little_k - Essentially an overall luminance scalar, keep it to values 0.9 and below
    dr_thresh - Dark region threshold, value between 0 and 1 representing the upper limit of dark pixels
                required to trigger contrast correction
                 
    Returns - A correct image if dr_tresh is breached or the original image if it is not
'''
def contrastCorrect(img, kernSize, big_k, little_k, dr_thresh):

    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype(np.float64)

    # Extract component channels
    lum, cb, cr = cv2.split(yuv)

    # Make sure there are no zero values with the luminance to avoid a divide by zero condition
    lum = np.where(lum > 0, lum, np.ones(lum.shape, dtype=np.float64))

    # Count the number of significantly dark pixels
    dark_count = len(lum[lum < 48])

    dark_ratio = float(dark_count)/lum.size

    # Calculate the skewness of the luminance channel
    skewness = stats.skew(lum, axis=None, bias=False)

    # Only apply if there's significant enough shade in the image

    if dark_ratio < dr_thresh:
        return img


    # C values and weights for gaussian filters
    cvals = [20, 80, 250]
    weights = [1.0/len(cvals) for i in range(0, len(cvals))]

    kerns = []

    # Build gaussian filters
    for c in cvals:
        kern = np.empty((kernSize, kernSize), dtype=np.float64)
        for y in range(0, kernSize):
            for x in range(0, kernSize):
                a_x = float(abs((kernSize-1)/2 + 1 - x))
                a_y = float(abs((kernSize-1)/2 + 1 - y))
                kern[y, x] = big_k*math.exp(-1*(float(a_x**2 + a_y**2)/(c**2)) )

        kern_sum = np.sum(kern)
        kerns.append(kern)

    reflectance = np.zeros(lum.shape, dtype=np.float64)

    # Calculate reflectance
    lum_log = np.log10(lum)

    for i in range(0, len(weights)):
        # filtered = cv2.GaussianBlur(lum, (kernSize, kernSize), cvals[i], cvals[i])
        filtered = cv2.filter2D(lum, cv2.CV_64F, kerns[i])
        reflectance += weights[i]*(lum_log - np.log10(filtered) )

    # Calculate mu
    mu = ((-1*skewness)/2.0 + little_k)

    # Calculate beta
    rmin = np.min(reflectance)
    rmax = np.max(reflectance)

    beta = ((reflectance - rmin)/(rmax - rmin))*mu

    # Calculate new luminance channel values
    lum_prime = (beta*(256 - 1))

    # Calculate chroma adjustment scalar
    cdeg = lum_prime/lum

    # Calculate new chroma values
    cb_prime = ((cdeg*(cb.astype(np.float64) - 128)) + 128)
    cr_prime = ((cdeg*(cr.astype(np.float64) - 128)) + 128)

    # Pack channels back together
    yuv_prime = cv2.merge( (lum_prime, cb_prime, cr_prime))
    yuv_prime = yuv_prime.astype(np.uint8)

    # Convert back to BGR
    bgr = cv2.cvtColor(yuv_prime.astype(np.uint8), cv2.COLOR_YCrCb2BGR)

    return bgr

