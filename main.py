import os
import numpy as np
from matplotlib import pyplot as plt
import imageio
import cv2



#file_loc = input("Enter location = ")
#Folder_loc = "1"

class Light_field_refocus:
  def __init__(self):
    self.blank_image = 0
    self.get_folder_loc()

    
  @classmethod  
  def get_loc(self):
    global folder_loc
    folder_loc = input("Enter folder location")

  @classmethod    
  def directory(self,path,extension):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
      if file.endswith(extension): # eg: '.txt'
        count += 1
    return count

  @classmethod 
  def sub_num(self):
    files = self.directory(folder_loc,"png")
    sq_root = np.sqrt(files)
    if (sq_root * sq_root == files ):
      i = np.floor(sq_root/2)
      i = i * sq_root + i
      return int(sq_root)
    else:
      print("Number of subaperture images not a perfect square") 

  @classmethod   
  def cen_img_ind(self):
    files = self.directory(folder_loc,"png")
    sq_root = np.sqrt(files)
    if (sq_root * sq_root == files ):
      i = np.floor(sq_root/2)
      i = i * sq_root + i
      return int(i)
    else:
      print("Number of subaperture images not a perfect square")


  @classmethod 
  def sub_view(self): 
    num = self.sub_num()
    blank_image = np.zeros((512*num,512*num,3), np.uint8)
    path = self.sub_img_tuple()
    count = 0
    for i in range(num):
      for j in range(num):
        if(count<10):
          blank_image[i*(512):512*(i+1),j*(512):512*(j+1),:] = path[i,j]
        else:
          path[i,j] = cv2.imread(folder_loc + "/input_Cam0" + str(count) + ".png")
          blank_image[i*(512):512*(i+1),j*(512):512*(j+1),:]=path[i,j]
        count +=1
        #plt.imshow(path[i,j])
        #plt.show()
    #print(len(path))    
    #savemat("LF.mat", path)
    cv2.imwrite("sub_view_img.png",blank_image)

  @classmethod 
  def central_view(self):
    i = self.cen_img_ind()
    if(i<10):
      img = cv2.imread(folder_loc + "/input_Cam00" + str(int(i)) + ".png")
      cv2.imwrite("central_view.png",img)
    else:
      img = cv2.imread(folder_loc + "/input_Cam0" + str(int(i)) + ".png")
      cv2.imwrite("central_view.png",img)


  @classmethod 
  def sub_img_tuple(self):
    num = self.sub_num()
    
    path = {}
    
    count = 0
    for i in range(num):
      for j in range(num):
        if(count<10):
          path[i,j] = cv2.imread(folder_loc + "/input_Cam00" + str(count) + ".png")
        elif (count>=10):
          path[i,j] = cv2.imread(folder_loc + "/input_Cam0" + str(count) + ".png")
        count +=1
    #cv2.imwrite("path.png",path[8,8])
    return path


  @classmethod 
  def fft_img_tuple(self):
    num = self.sub_num()
    path = self.sub_img_tuple()
    dim = path[0,0].shape
    LF_sep = {}
    a = path[0,0]
    #print(dim[0]==dim[1])
    #b1 = np.empty(shape=(dim[0] , dim[1], dim[2]),dtype='complex')
   
    if (dim[0]==dim[1]):
      w = np.hanning(dim[0])
      w= np.sqrt(np.outer(w,w))
      for i in range(num):
        for j in range(num):
          #print(num,i,j)
          b1 = np.empty(shape=(dim[0] , dim[1], dim[2]),dtype='complex')
          b1[:,:,0] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,0]))*w) 
          b1[:,:,1] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,1]))*w)
          b1[:,:,2] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,2]))*w)
          LF_sep[i,j] = b1
          if i==0 & j==0:
            #print(LF_sep[0,0].shape)
            cv2.imwrite("LF.png",np.real(np.fft.ifft2(LF_sep[0,0][:,:,0])))
    elif (dim[0]>dim[1]):
      w = np.hanning(dim[0])
      dif = dim[0] - dim[1]
      path[i,j] = np.pad(path[i,j], [(0, 0), (0, dif)], mode='constant', constant_values=0)
      for i in range(num):
        for j in range(num):
          b1 = np.empty(shape=(dim[0] , dim[1], dim[2]),dtype='complex')
          b1[:,:,0] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,0]))) 
          b1[:,:,1] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,1])))
          b1[:,:,2] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,2])))
          LF_sep[i,j] = b1

    elif (dim[1]>dim[0]):
      w = np.hanning(dim[1])
      dif = dim[1] - dim[0]
      path[i,j] = np.pad(path[i,j], [(0, dif), (0, 0)], mode='constant', constant_values=0)
      for i in range(num):
        for j in range(num):
          b1 = np.empty(shape=(dim[0] , dim[1], dim[2]),dtype='complex')
          b1[:,:,0] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,0]))) 
          b1[:,:,1] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,1])))
          b1[:,:,2] = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(path[i,j][:,:,2])))
          LF_sep[i,j] = b1
    return LF_sep


  @classmethod   
  def shift_var(self,slope):
    num = self.sub_num()
    voffset_vec = {}
    for i in range(num):
      voffset_vec[i]= (i - np.floor(num/2)) * slope
    uoffset_vec = voffset_vec
    return [voffset_vec, uoffset_vec]
      
  @classmethod   
  def refocus(self,slope):
    num = self.sub_num()
    [voffset_vec, uoffset_vec] = self.shift_var(slope)
    LF_sep = self.fft_img_tuple()
    dim = LF_sep[0,0].shape



    LF_reshape = np.empty(shape=(num*num,dim[0],dim[1],dim[2]),dtype='long')
    #LF_reshape = 0
    Nr = np.fft.ifftshift(np.linspace(-np.fix(dim[0]/2) , np.ceil(dim[0]/2)-1 , dim[0]))
    Nc = np.fft.ifftshift(np.linspace(-np.fix(dim[1]/2) , np.ceil(dim[1]/2)-1 , dim[1]))   
    xF, yF = np.meshgrid(Nr,Nc)
    count=0
    for j in range(num):
      for i in range(num):
        voffset = voffset_vec[i]
        uoffset = uoffset_vec[j]
        #in_img = LF_sep[i,j]

        x0 = -uoffset
        y0 = -voffset
        H = np.exp(1J*2*np.pi*(x0*xF/dim[0]+y0*yF/dim[1]))
        #H=np.real(H)
        IF_img = np.empty(shape=(dim[0],dim[1],dim[2]))
        
        IF_img[:,:,0] = np.real(np.fft.ifft2(LF_sep[i,j][:,:,1]*H))
        IF_img[:,:,1] = np.real(np.fft.ifft2(LF_sep[i,j][:,:,1]*H))
        IF_img[:,:,2] = np.real(np.fft.ifft2(LF_sep[i,j][:,:,2]*H))

        x0 = np.round(int(x0))
        y0 = np.round(int(y0))

        if (x0>0):
            IF_img[:,dim[0]-np.abs(x0):dim[0],:] = 0
        elif (x0>0):
            IF_img[:,0:abs(x0),:] = 0

        if (y0>0):
            IF_img[dim[0]-np.abs(x0):dim[0],:,:] = 0
        elif (y0>0):
            IF_img[0:abs(x0),:,:] = 0


        LF_reshape[count,:,:,:] = IF_img
        count+=1
    #print(LF_reshape.shape)

    IF_img_1 = np.empty(shape=(1,dim[0],dim[1],dim[2]))


    #print(dim)

    IF_img_2 = np.nanmedian(LF_reshape,0)

    #print(IF_img_2.shape)

    #print(voffset_vec)
    #print(uoffset_vec)
    cv2.imwrite("refocused.png",IF_img_2)


 
        

  

   

