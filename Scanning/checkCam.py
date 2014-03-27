import cv2.cv as cv
def count_cameras():
    for i in range(50):
        temp_camera = cv.CreateCameraCapture(i)
        print temp_camera
        temp_frame = cv.QueryFrame(temp_camera)
        del(temp_camera)
        if temp_frame==None:
            del(temp_frame)
            print"NONE", i #MacbookPro counts embedded webcam twice
        else: print "YES", i

if __name__ == "__main__":
    count_cameras()
