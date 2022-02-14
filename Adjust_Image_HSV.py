# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import cv2 # IMAGE PROCESSING
import numpy as np

def empty(a):
    pass

def put_text_on_image(img_in, text=None):
    '''
    Function to place text on an image indicating the type of transformation applied to image

    :param img_in: image for text placement
    :param text: indicates type of transformation applied to the image

    :return img_out: resulting image labeled with the transformation type
    '''
    img_out = cv2.putText(img_in, text, (20, 75), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 3)
    return img_out

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


# define path to image
path = r'/Users/jdhauswirth/PycharmProjects/pythonProjectHSV/resources/plant_400x400.png'

# create a window that will have sliders to adjust RGB baleus
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 440)

# these values are specific to the image  and will vary
# with every image.   Demo video I watched showed the actual numeric
# min max values on the track bar but on my mac I do not see values on window.
cv2.createTrackbar("Hue Min", "TrackBars",  28, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars",  91, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars",  43, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars",  33, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        # reading the original image
        img = cv2.imread(path)

        # convert to HSV image
        #
        # While in BGR, an image is treated as an additive result
        # of three base colors (blue, green and red), HSV stands
        # for Hue, Saturation and Value (Brightness). We can say that
        # HSV is a rearrangement of RGB in a cylindrical shape.
        # The HSV ranges are: 0 > H > 360 ⇒ OpenCV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
        print(h_min, h_max, s_min, s_max, v_min, v_max)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # create mask in the range of the colors defined by range
        mask = cv2.inRange(imgHSV, lower, upper)

        # create resulting image
        imgResult = cv2.bitwise_and(img, img, mask=mask)

        # hiding show of individual windows by commenting out
        # images will be shown below
        # cv2.imshow("Original", img)
        # cv2.imshow("HSV", imgHSV)
        # cv2.imshow("Mask", mask)
        # cv2.imshow("Result", imgResult)

        # this will create a 2x2 stack of 4 images summarizing the progress
        # from original, hsv, mask and the resulting image.

        # lay text over images indicating image type
        orig_w_txt = put_text_on_image(img, text='Orig')
        HSV_w_txt = put_text_on_image(imgHSV, text='HSV')
        mask_w_txt = put_text_on_image(mask, text='Mask')
        imgResult_w_txt = put_text_on_image(imgResult, text='Result')

        # create the panel composite stack of the images
        imgStack = stackImages(0.8, ([orig_w_txt, HSV_w_txt], [mask_w_txt, imgResult_w_txt]))
        cv2.imshow("Stacked Images for Color Detection - Use Track Bar sliders to adjust", imgStack)

        # write to PyCharm project folder for outputs
        #cv2.imwrite('/Users/jdhauswirth/PycharmProjects/pythonProjectHSV/outputs/img_HSV_stack.jpg', imgStack)

        # highlight output windows and press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        #cv2.destroyAllWindows()

