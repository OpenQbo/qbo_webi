
function startEverything(){



		jQuery.post('/mjpegServer/start', function(data){
			//Getting images
		 	output = {image:"rightEye", quality: quality, width: widthCamera, height: heightCamera};
	                jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
				defaultImg = "http://"+ipLocal+":"+imgPort+data;
				cameraURL=defaultImg;
	                });

			output = {image:"objects", quality: quality, width: widthCamera, height:heightCamera};
	                jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
	                        recognizeObjImg = "http://"+ipLocal+":"+imgPort+data;
        	        });

			output = {image:"faces", quality: quality, width: widthCamera, height:heightCamera};
	                jQuery.post('/mjpegServer/getUrlFrom',output,function(data) {
        	                recognizeFaceImg = "http://"+ipLocal+":"+imgPort+data;
	                });
		});


/*		jQuery( "input:submit, a, button" ).button();
		jQuery( "#radio" ).buttonset();*/


		//Camera settings
		//Inicializacion de vriables para refreshWebCam
        	canvas = document.getElementById('canvasWebcam');
	        ctx=canvas.getContext('2d');
		loop=setInterval(refreshWebCam,fps);


		jQuery("#training").click(function(){
			name2Learn =  jQuery("#face_object_name").val().toUpperCase();		
			if(name2Learn==""){
				jQuery("#answer").html("${language['error_no_name_written']}");
			}else{

				 //launch Nodes
        	                jQuery.post('/training/launchNodes',function(data) {	
					       if(objectORface == "object"){
	                		           cameraURL=recognizeObjImg;
        	        		       }else{
		        	                   cameraURL=recognizeFaceImg;
        		        	       }
	        		               auxTime4Coundown = new Date().getTime();
	                		       action="learning";
        		        	       countdown=3;
			                       bool_drawing=true;
					
				});
			}
		});

                jQuery("#guessing").click(function(){
			//launch Nodes
			jQuery.post('/training/launchNodes',function(data) {
				if(objectORface == "object"){
					cameraURL=recognizeObjImg;
				}else{
					cameraURL=recognizeFaceImg;
				}
                                auxTime4Coundown = new Date().getTime();
                                action="recognizing";
                                countdown=3;
                                bool_drawing=true;
                        });
		});

		jQuery("#radioFace").click(function(){
			jQuery.post('/training/selectFaceRecognition',function(data) {
				jQuery("#personORobject").html("person");
			});	
		});




		
		


}



















function refreshWebCam(){

        //We check wether we are in the tab that is showing the canvas y we just left, so we have to stop everthing
        if( jQuery("#ui-tabs-4").hasClass('ui-tabs-hide') ){
                clearInterval(loop);

                //stop mjpeg server
                jQuery.post('/mjpegServer/stop', function(data) {
                       if(data=="ERROR"){
                       }
                });
        }


        try{
        img.src=cameraURL;

        img.onload = function(){
                ctx.drawImage(img, 0, 0, img.width, img.height);
                if(bool_drawing){
                        //Painting countdown
                        if(countdown > -1){

                                if ( new Date().getTime() - auxTime4Coundown >= 1000 ){
                                        countdown = countdown - 1;
                                        auxTime4Coundown = new Date().getTime();
                                }
                                if(countdown != -1){
                                        ctx.font = "bold 36px sans-serif";
                                        ctx.fillStyle = "rgb(255, 0, 0)";
                                        ctx.fillText(countdown.toString(), 10, 200);

                                }else{
                                        countdown = -100;
                                        //alert("lanzadera");
                                        //Lanzamos la grabacion de fotogramas                           
                                        //ID_grabaFotogramas = setInterval(grabaFotogramas, delayBtwFotogramsCaptured);

                                        if(action=="learning"){
                                                recording=true;
                                                disableRadioBotton(true);
                                                startLearning();
                                        }else if(action=="recognizing"){
                                                watching=true;
                                                disableRadioBotton(true);
                                                startRecognition();
                                        }

                                }

                        }

                        if(recording && countdown==-100){
                                ctx.font = "bold 36px sans-serif";
                                ctx.fillStyle = "rgb(255, 0, 0)";
                                ctx.fillText(msgWebCamRec, 10, 200);
                        }else if(training && countdown==-100){
                                ctx.font = "bold 36px sans-serif";
                                ctx.fillStyle = "rgb(255, 0, 0)";
                                ctx.fillText(msgWebCamTraining, 10, 200);
                        }else if(watching && countdown==-100){
                                ctx.font = "bold 36px sans-serif";
                                ctx.fillStyle = "rgb(255, 0, 0)";
                                ctx.fillText(msgWebCamWatching, 10, 200);
                        }

                }
        }
        }catch(e){
        }

}


function startLearning(){
                                //lanzamos aprendizaje
                                output = { objectName : name2Learn };
                                jQuery.post('/training/startLearning' ,output, function(data) {
                                        recording=false;
                                        training=true;
                                        jQuery.post('/training/startTraining' , function(data) {

                                                training=false;
                                                bool_drawing=false;
						alert(data);
                                                if(data){
							jQuery("#answer").html("${language['learning_ok']}"+name2Learn);
                                                }else{//error
							jQuery("#answer").html("${language['learning_ko']}"+name2Learn); 
                                                }

                                                cameraURL=defaultImg;
                                                jQuery.post('/rosRecognizeObject/stopNode',function(data) {
                                                });
                                        });
                                });
}


function startRecognition(){
	 //start recognition
                                jQuery.post('/training/startRecognition',function(data) {
                                        cameraURL=defaultImg;
                                        watching=false;

                                        if(data!=""){
                                                jQuery("#answer").html("${language['this_is_a']}"+data.toLowerCase());
                                        }else{
                                                jQuery("#answer").html("${language['dontKnow']}");
                                        }

                                        //paramos nodo
                                        jQuery.post('/training/stopNode',function(data) {
                                        });


                                        cameraURL=defaultImg;
					disableRadioBotton(false);

                                })
                                .error(function() {


                                        //paramos nodo
                                        jQuery.post('training/stopNode',function(data) {
                                        });

                                        cameraURL=defaultImg;
				        disableRadioBotton(false);
                                });
}









function disableRadioBotton(disable){

	if(disable){
		jQuery("#radio").attr("disabled", "disabled");
	}else{
		jQuery("#radio").removeAttr("disabled");
	}	
}
