
var ipLocal="192.168.4.104";
var imgPort="8080";
var quality=50;
var widthCamera=250;
var heightCamera=250;


var defaultImg="http://"+ipLocal+":"+imgPort+"/snapshot?topic=/stereo/right/image_raw?quality="+quality+"?width="+widthCamera+"?height="+heightCamera;

var recognizeObjImg = "http://"+ipLocal+":"+imgPort+"/snapshot?topic=/qbo_stereo_selector/viewer?quality="+quality+"?width="+widthCamera+"?height="+heightCamera;

var recognizeObjFace = "http://"+ipLocal+":"+imgPort+"/snapshot?topic=/qbo_face_tracking/viewer?quality="+quality+"?width="+widthCamera+"?height="+heightCamera;


//imagen a visualizar
var cameraURL=defaultImg;

var fps=24;

var ctx;
var img = new Image();
var canvas;
var loop;
