import cv2
from OpenCV_imread import imreadUnicode
import glob

# same_characters = 6 #number of characters that define if two images are in the same group / type
image_dict = {img : [imreadUnicode(img)] for img in glob.glob("./Supporter_cards/*.png")}



# for key in image_dict:
#     group = key.split('_')[2][0]
#     image_dict[key].append(group)
a = glob.glob("./Supporter_cards/*.png")
print(a)
for img in glob.glob("Supporter_cards/*.png"):
    print(img)
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