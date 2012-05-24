var keys = {};

function startEverything(){
    jQuery("#iframeTeleoperation").mousemove(function(e){


        x = jQuery("#iframeTeleoperation").offset().left;
        y = jQuery("#iframeTeleoperation").offset().top;


        finalX=e.pageX-x;
        finalY=e.pageY-y;

      var pageCoords = "( " + finalX + ", " + finalY + " )";
      var clientCoords = "( " + e.clientX + ", " + e.clientY + " )";

      jQuery("#output").html("( e.pageX, e.pageY ) : " + pageCoords+ "   " + clientCoords+ "        "+x+" "+y);


    });


    jQuery.post('/mjpegServer/start', function(data){
                        //Getting images
                        output = {image:"live_leftEye", quality: quality, width: widthCamera, height: heightCamera};
                        jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
                                defaultImg = "http://"+ipLocal+":"+imgPort+data;
                                cameraURL=defaultImg;

				setTimeout('jQuery("#iframeTeleoperation").attr("src",cameraURL);',2000);

				loop=setInterval("checkTab()",100);
                        });
    });




	jQuery("#foward").click(function(){
		jQuery.post('/teleoperation/foward',function(data){
		});
	});





jQuery(document).keydown(function (e) {
	keys[e.which] = true;
	printKeys();
});

jQuery(document).keyup(function (e) {
	delete keys[e.which];
	printKeys();
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




//We need one way to know whether we are in this tab or not in order to stop mjpeg_server

function checkTab(){
        //We check wether we are in the tab that is showing the canvas y we just left, so we have to stop everthing
        if( $("#ui-tabs-3").hasClass('ui-tabs-hide') ){
                clearInterval(loop);

                //stop mjpeg server
                $.post('/mjpegServer/stop', function(data) {
                       if(data=="ERROR"){
                       }
                });
        }

}
