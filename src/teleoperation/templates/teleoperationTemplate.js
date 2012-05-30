var keys = {};
var leftButtonDown = false;
var imgPort="8081";


var loop;

var quality=50;
var widthCamera=640;
var heightCamera=480;



var fps=24;

var ctx;
var img = new Image();
var canvas;

var action;
var countdown;
var bool_drawing=false;
var recording = false;
var watching = false;
var training = false;
var auxTime4Coundown;

var name2Learn;

var objectORface="object";


var msgWebCamWatching = "Watching";
var msgWebCamTraining = "Training...";
var msgWebCam = "";
var msgWebCamRec = "Rec";

var cameraURL=""


function startEverything(){


    output = {image:"live_leftEye", quality: quality, width: widthCamera, height: heightCamera};
    jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
        defaultImg = "http://"+ipLocal+":"+imgPort+data;
        cameraURL=defaultImg;
        setTimeout('jQuery("#iframeTeleoperation").attr("src",cameraURL);',2000);
    });
    



    originX=jQuery("#video2").offset().left;
    originY=jQuery("#video2").offset().top;


    jQuery(document).mousemove(function(e){
		 jQuery("#output3").html(e.pageX+" "+e.pageY);
// originX=jQuery("#video").offset().left;
// originY=jQuery("#video").offset().top;
//		 jQuery("#output").html(originX+" "+originY);

    });

    jQuery("#video2").draggable({
	    drag: function() {


   			originX=jQuery("#video").offset().left+(jQuery("#video").width()/2);
    			originY=jQuery("#video").offset().top+(jQuery("#video").height()/2);

			x = jQuery("#video2").offset().left+(jQuery("#video2").width()/2);
                        y = jQuery("#video2").offset().top+(jQuery("#video2").height()/2);

			trueX = x-originX;
			trueY = y-originY;			

			jQuery("#output").html("centro de video = "+originX+" "+originY);
			jQuery("#output2").html("centro de video2 "+x+" "+y+"                       "+trueX*-1+" "+trueY);

			input = {"yaw":trueX*-1,"pitch":trueY};
            jQuery.post('/teleoperation/head',input, function(data){
            });


                      
	    },
            stop: function() {
		jQuery("#video2").offset({"top":jQuery("#video").offset().top,"left":jQuery("#video").offset().left});		
 		input = {"yaw":0,"pitch":0};
                jQuery.post('/teleoperation/head',input, function(data){
                });



            }
    });

	//Buttons detection
	jQuery("#foward").click(function(){
		jQuery.post('/teleoperation/foward',function(data){
		});
	});


	//Keys detector
	jQuery(document).keydown(function (e) {
		keys[e.which] = true;
		printKeys();
	});

	jQuery(document).keyup(function (e) {
		delete keys[e.which];
		printKeys();
	});



    //Change view events
    jQuery("#radioLeft").click(function(){
        output = {image:"live_leftEye", quality: quality, width: widthCamera, height: heightCamera};
        jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
            cameraURL = "http://"+ipLocal+":"+imgPort+data;
            jQuery("#iframeTeleoperation").attr("src","");
            jQuery("#iframeTeleoperation").attr("src",cameraURL);
        });
    });
    jQuery("#radioRight").click(function(){
        output = {image:"live_rightEye", quality: quality, width: widthCamera, height: heightCamera};
        jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
            cameraURL = "http://"+ipLocal+":"+imgPort+data;
            jQuery("#iframeTeleoperation").attr("src","");
            jQuery("#iframeTeleoperation").attr("src",cameraURL);
        });
    });
    jQuery("#radio3d").click(function(){
            output = {image:"live_3d", quality: quality, width: widthCamera, height: heightCamera};
            jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
                cameraURL = "http://"+ipLocal+":"+imgPort+data;
                jQuery("#iframeTeleoperation").attr("src","");
                jQuery("#iframeTeleoperation").attr("src",cameraURL);
           });
    });



}


function printKeys() {
	var keypressed = '';
	for (var i in keys) {
		if (!keys.hasOwnProperty(i)) continue;
		keypressed += i + ' ';
	}

          if (keypressed.indexOf("87") != -1  && keypressed.indexOf("65") != -1 ) {                
                input = {"line":0.2,"angu":1};
                jQuery.post('/teleoperation/move',input,function(data){
                });
          }else if (keypressed.indexOf("87") != -1  && keypressed.indexOf("68") != -1 ) {
                input = {"line":0.2,"angu":-1};
                jQuery.post('/teleoperation/move',input,function(data){
                });
          }else if (keypressed.indexOf("83") != -1  && keypressed.indexOf("65") != -1 ) {
                input = {"line":-0.2,"angu":1};
                jQuery.post('/teleoperation/move',input,function(data){
                });
          }else if (keypressed.indexOf("83") != -1  && keypressed.indexOf("68") != -1 ) {
                input = {"line":-0.2,"angu":-1};
                jQuery.post('/teleoperation/move',input,function(data){
                });
          }else if (keypressed.indexOf("68") != -1 ) {
                input = {"line":0,"angu":-1};
                jQuery.post('/teleoperation/move',input,function(data){
                });

          }else if (keypressed.indexOf("65") != -1) {
                input = {"line":0,"angu":1};
                jQuery.post('/teleoperation/move',input,function(data){
                });
          }else if (keypressed.indexOf("87") != -1 ) {
                input = {"line":0.2,"angu":0};
                jQuery.post('/teleoperation/move',input,function(data){
                });

          }else if (keypressed.indexOf("83") != -1) {
                input = {"line":-0.2,"angu":0};
                jQuery.post('/teleoperation/move',input,function(data){
                });                    
          }else{

		//paramos
		input = {"line":0,"angu":0};
                jQuery.post('/teleoperation/move',input,function(data){
                }); 
		
	  }


        

}




