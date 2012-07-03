import roslib
roslib.load_manifest('qbo_webi')
import cherrypy
import time
import sys
import rospy
import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image as RosImage
from cv_bridge import CvBridge, CvBridgeError
import cStringIO
import cv
import threading
import json

class image_converter:

  def __init__(self,imageData):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber(imageData['topic'],RosImage,self.callback)
    self.cv_image=None
    self.w=imageData['width']
    self.h=imageData['height']
    self.quality=imageData['quality']
    self.img_lock=threading.Lock()

  def callback(self,data):
    with self.img_lock:
      try:
        self.cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
      except CvBridgeError, e:
        print e

  def getImage(self,wait=False):
    if wait:
      i=0
      while not self.cv_image and i<10:
        i+=1
        time.sleep(0.1)
    image=cv.CreateMat(self.h, self.w, cv.CV_8UC3)
    cv.SetZero(image)
    if not self.cv_image:
      pass
    else:
      with self.img_lock:
        cv.Resize(self.cv_image,image)
    return cv.EncodeImage(".jpeg", image, [cv.CV_IMWRITE_JPEG_QUALITY, self.quality]).tostring()

  def stop(self):
    self.image_sub.unregister()



class MjpegGrabber():

    def __init__(self):
        self.subscribedTopics={}
        self.boundary="--streammjpeg--"
        rospy.on_shutdown(self.stopAll)

    def stopAll(self):
        self.subscribedTopics={}

    @cherrypy.expose
    def stream(self,topic,quality='90',width='320',height='240',rate='30',t=''):
        cherrypy.response.headers['Content-Type'] = "multipart/x-mixed-replace;boundary=--"+self.boundary
        imageInfo={}
        imageInfo['topic']=topic
        imageInfo['quality']=int(quality)
        imageInfo['width']=int(width)
        imageInfo['height']=int(height)

        return self.content(imageInfo,float(rate))
    stream._cp_config = {'response.stream': True}

    @cherrypy.expose
    def snapshot(self,topic,quality='90',width='320',height='240',t=''):
        imageInfo={}
        imageInfo['topic']=topic
        imageInfo['quality']=int(quality)
        imageInfo['width']=int(width)
        imageInfo['height']=int(height)
        imageInfoStr=json.dumps(imageInfo)

        if imageInfoStr not in self.subscribedTopics.keys():
            self.subscribedTopics[imageInfoStr]=image_converter(imageInfo)
        imgData=self.subscribedTopics[imageInfoStr].getImage(wait=True)

        cherrypy.response.headers['Content-Type'] = 'image/jpeg'
        cherrypy.response.headers['Content-Length']='%d' % (len(imgData))
        cherrypy.response.headers['X-Timestamp']='%f' % (time.time())

        return imgData

    @cherrypy.expose
    def stop(self,topic,quality='90',width='320',height='240',rate='30.0',t=''):
        imageInfo={}
        imageInfo['topic']=topic
        imageInfo['quality']=int(quality)
        imageInfo['width']=int(width)
        imageInfo['height']=int(height)
        imageInfoStr=json.dumps(imageInfo)
        print 'stopping ',imageInfoStr
        if imageInfoStr in self.subscribedTopics:
            self.subscribedTopics[imageInfoStr].stop()
            del self.subscribedTopics[imageInfoStr]
            return 'Stoped'
        else:
            return 'Topic not found'

    def content(self,imageInfo,rate=30.0):
        imageInfoStr=json.dumps(imageInfo)

        if imageInfoStr not in self.subscribedTopics:
            print 'nuevo topic'
            self.subscribedTopics[imageInfoStr]=image_converter(imageInfo)
        else:
            print 'topic existente'

        imageRate=rospy.Rate(rate)
        while imageInfoStr in self.subscribedTopics:
            imgData=self.subscribedTopics[imageInfoStr].getImage()
            intermediateheader="Content-Type: image/jpeg\r\nContent-Length: %d\r\nX-Timestamp: %f\r\n\r\n" % (len(imgData),time.time())
            #print 'wait for rate ok'
            imageRate.sleep()
            #time.sleep(1./rate)
            #print 'end wait for rate ok'
            yield "\n\r--"+self.boundary+"\r\n"+intermediateheader+imgData+"\r\n"+self.boundary+"\n\r"
        print 'End of content'
        #yield "\n\r--"+self.boundary+"\r\n"+intermediateheader+imgData+"\r\n"+self.boundary+"\n\r"

