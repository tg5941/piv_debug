from openpiv.gpu import process
from openpiv import tools
import os
import imageio.v2 as io
import numpy as np
from tqdm import tqdm
import scipy.io as sio
from natsort import natsorted
import matplotlib.pyplot as plt

def PIV_single_test(batch_n, gen_loc, im_loc, file_name, params):
    if not os.path.exists(gen_loc+'Shifts/'+file_name):
        os.makedirs(gen_loc+'Shifts/'+file_name)
    
    directory_l = im_loc+file_name+'/Left'
    png_files_l = list_png_files(directory_l)
    
    directory_r = im_loc+file_name+'/Right'
    png_files_r = list_png_files(directory_r)
    
    batch_s = int(np.floor((len(png_files_l)-1)/batch_n))
    # batch_s = 5
    
    n_l = directory_l +'/'+png_files_l[0]
    print(n_l)
    print(len(png_files_l))
    
    im1_l = (io.imread( directory_l+'/'+png_files_l[0] ))
    im1_r = (io.imread( directory_r+'/'+png_files_r[0] ))
    
    im2_l = (io.imread( directory_l+'/'+png_files_l[1]))
    im2_r = (io.imread( directory_r+'/'+png_files_r[1]))
    
    side1_1 = im1_l.copy()
    side2_1 = im1_r.copy()
    
    side1_2 = im2_l.copy()
    side2_2 = im2_r.copy()
    
    print(type(params))
    PIV_mask = np.ones_like(side1_1)
    PIV_mask[(side1_1 == 0) | (side2_1 == 0)] = 0
    #params['mask'] = PIV_mask
    
    x, y, D1, D2, mask, D3 = process.gpu_piv(side1_1, side1_2, **params)
    print(D1.shape)
    
    #Show image to check selected region
    fig, ax = plt.subplots(1,3,figsize=(7.5, 9), dpi=300, tight_layout=True)
    ax[0].imshow(im1_l,cmap='gray')
    ax[1].imshow(im1_r,cmap='gray')
    ax[2].imshow(np.sqrt(D1**2 + D2**2),cmap='gray')

    plt.show()

    return side1_1, side2_1, D1, batch_s, directory_l, directory_r, png_files_l, png_files_r, PIV_mask

def list_png_files(directory):
    # List to store the png file names
    png_files = []
    
    # Iterate over all the files in the given directory
    for file_name in os.listdir(directory):
        
        # Check if the file ends with .png
        if file_name.endswith('.png'):
            png_files.append(file_name)

    #png_files.sort()
    sorted_filenames = natsorted(png_files)
    
    return sorted_filenames
    
def worker(gpu_id,cnt_in, batch_ran,index_range,batch_s,D1,directory_l,directory_r,png_files_l,png_files_r,gen_loc,dist,file_name,side1_1,side2_1,params,PIV_mask):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    from openpiv.gpu import process
    from openpiv import tools
    
    u1 = np.empty(( D1.shape[0], D1.shape[1],batch_s-1))
    v1 = np.empty_like(u1)
    
    u2=u1.copy()
    v2=v1.copy()
    
    cnt = cnt_in
    if int(gpu_id) == 0:
        for iii in range(*batch_ran):
            for ii in tqdm(range(*index_range)):
                im2_l = (io.imread( directory_l+'/'+png_files_l[cnt]))
                im2_r = (io.imread( directory_r+'/'+png_files_r[cnt]))
                side1_2 = im2_l.copy()
                side2_2 = im2_r.copy()
                #print(directory_l+'/'+png_files_l[ii])
                _, _, u1[:,:,ii-1], v1[:,:,ii-1], _, _ = process.gpu_piv(side1_1, side1_2, **params)
                x, y, u2[:,:,ii-1], v2[:,:,ii-1], _, _ = process.gpu_piv(side2_1, side2_2, **params)
                cnt = cnt + 1
                # print('Done' + str(gpu_id))
            # collect arrays in dictionary
            savedict = {
                'shiftx_1' : u1,
                'shifty_1' : v1,
                'shiftx_2' : u2,
                'shifty_2' : v2,
                'X'        : x,
                'Y'        : y,
                'mask'     : PIV_mask
            }
        
            if not os.path.exists(gen_loc +'Shifts/'):
                # Create the directory if it does not exist
                os.makedirs(gen_loc +'Shifts/')
            save_name = '%d'%(dist) + file_name[8:]+'_b%d.mat'%(iii) 
            # save to disk
            sio.savemat(gen_loc +'Shifts/'+file_name+'/'+save_name, savedict)
            print('Shifts/'+file_name+'/'+save_name+'\n')
    else:
        for iii in range(*batch_ran):
            for ii in range(*index_range):
                im2_l = (io.imread( directory_l+'/'+png_files_l[cnt]))
                im2_r = (io.imread( directory_r+'/'+png_files_r[cnt]))
                side1_2 = im2_l.copy()
                side2_2 = im2_r.copy()
                #print(directory_l+'/'+png_files_l[ii])
                _, _, u1[:,:,ii-1], v1[:,:,ii-1], _, _ = process.gpu_piv(side1_1, side1_2, **params)
                x, y, u2[:,:,ii-1], v2[:,:,ii-1], _, _ = process.gpu_piv(side2_1, side2_2, **params)
                cnt = cnt + 1
                # print('Done' + str(gpu_id))
            # collect arrays in dictionary
            savedict = {
                'shiftx_1' : u1,
                'shifty_1' : v1,
                'shiftx_2' : u2,
                'shifty_2' : v2,
                'X'        : x,
                'Y'        : y,
                'mask'     : PIV_mask
            }
        
            if not os.path.exists(gen_loc +'Shifts/'):
                # Create the directory if it does not exist
                os.makedirs(gen_loc +'Shifts/')
            save_name = '%d'%(dist) + file_name[8:]+'_b%d.mat'%(iii) 
            # save to disk
            sio.savemat(gen_loc +'Shifts/'+file_name+'/'+save_name, savedict)
            print('Shifts/'+file_name+'/'+save_name+'\n')

    return