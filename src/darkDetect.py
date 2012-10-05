#!/usr/bin/env python
import roslib
roslib.load_manifest('qbo_webi')
import sys
import rospy
import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time

class image_converter:

  def __init__(self):
    #self.image_pub = rospy.Publisher("image_topic_2",Image)
    self.pub = rospy.Publisher('/dark_detect', String)

    #cv.NamedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/stereo/left/image_mono",Image,self.callback)
    self.okCounter = 0
    self.startCounter = 300
    self.t1 = time.time()
    self.detectedMsgsSent = 0

  def callback(self,data):
    t2 = time.time()
    diffTime = t2 - self.t1
    self.t1 = t2
    if self.startCounter > 0:
        self.startCounter -= 1
    try:
      cv_image = self.bridge.imgmsg_to_cv(data, "mono8")
    except CvBridgeError, e:
      print e

    #(cols,rows) = cv.GetSize(cv_image)
    #if cols > 60 and rows > 60 :
      #cv.Circle(cv_image, (50,50), 10, 255)

    mean = 0
    stdv = 0
    (mean, stdv) = cv.AvgSdv(cv_image)

    #print 'mean, stdv and diffTime: ',mean[0], stdv[0], diffTime

    #cv.ShowImage("Image window", cv_image)
    #cv.WaitKey(3)

    if mean[0]<50 or stdv[0]<23 or diffTime > 0.05:
        self.okCounter = 0
    else:
        self.okCounter += 1

    if self.okCounter > 10:
        print 'ok'
        #return True
        if (self.detectedMsgsSent < 5):
            self.detectedMsgsSent += 1
            self.pub.publish(String('Light detected!'))
    else:
        pass
        print 'dark'
        #return False

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    #rospy.spin()
    while ic.detectedMsgsSent < 5:
        time.sleep(1.0)
  except KeyboardInterrupt:
    print "Shutting down"
  #cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
