# same_characters = 6 #number of characters that define if two images are in the same group / type
# image_dict = {img : [imreadUnicode(img)] for img in glob.glob("./Supporter_cards/*.png")}



# for key in image_dict:
#     group = key.split('_')[2][0]
#     image_dict[key].append(group)
# a = glob.glob("./Supporter_cards/*.png")
# print(a)
# for img in glob.glob("Supporter_cards/*.png"):
#     print(img)
    
    
    
    
import glob, os
import cv2, numpy as np

def imreadUnicode(file):
    npFile = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npFile, cv2.IMREAD_UNCHANGED) # img = array
    return img

path = './Supporter_cards'
Supporter_cards = dict()

for a in glob.glob(os.path.join(path, '*')):
    key = a.replace('.', '/').replace('\\', '/')
    key = key.split('/')
    Supporter_cards[key[-2]] = imreadUnicode(a)

Supporter_cards_now = dict()
for i in Supporter_cards.keys():
    Supporter_cards_now[i] = 0
print(Supporter_cards_now)
    
    # img = imreadUnicode(infile)
    # my_key = i                 # or put here whatever you want as a key
    # image_dict[my_key] = img

#print image_dict
# print(len(image_dict))
# print(image_dict[0]) # this is the value associated with the key 0
# print(Supporter_cards.keys()) # this is the list of all keys
# print(image_dict["SSR_오구리_캡"])
# print(image_dict.values()) # this is the list of all keys
# print(type(image_dict.keys()[0])) # this is <type 'int'>
# print(type(image_dict.values()[0])) # this is <type 'numpy.ndarray'>
    
    
    
    
    
    
    
    
    # a = imreadUnicode(img)
    # cv2.imshow("123", a)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
# for value in **image_dict:
#     # print("Image name = \"",key,"\" => ",image_dict[key][0], ", group =\"" + image_dict[key][1] + "\"")
    
#     # cv2.imshow(key, image_dict[key]) #show the image, don't use it when you're reading too many pictures
#     cv2.imshow("123", value)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# https://stackoverflow.com/questions/60408517/how-to-clustering-multiple-images-by-the-name-in-python