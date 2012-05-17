
function startEverything(){


/*		$( "input:submit, a, button" ).button();
		$( "#radio" ).buttonset();*/




		//Camera settings
		//Inicializacion de vriables para refreshWebCam
        	canvas = document.getElementById('canvasWebcam');
	        ctx=canvas.getContext('2d');
		loop=setInterval(refreshWebCam,fps);



};













function refreshWebCam(){


	//We check wether we are in the tab that is showing the canvas y we just left, so we have to stop everthing
	if( $("#ui-tabs-4").hasClass('ui-tabs-hide') ){
		clearInterval(loop);
	}

        img.src=cameraURL;
        img.onload = function(){
        //      ctx.clip();//call the clip method so the next render is clipped in last path
                ctx.drawImage(img, 0, 0, img.width, img.height);

                if(bool_drawing){
                        /*x = Math.min(x_act,  x0),
                        y = Math.min(y_act,  y0),
                        w = Math.abs(x_act - x0),
                        h = Math.abs(y_act - y0);

                        ctx.strokeStyle = '#f00'; // red
                        ctx.lineWidth   = 4;
                        ctx.strokeRect(x, y, w, h);*/

                        //Pintar countdown
                        if(countdown > -1){
                                if ( new Date().getTime() - auxTime4Coundown >= 1000 ){
                                        countdown = countdown - 1;
                                        auxTime4Coundown = new Date().getTime();
//                                      alert("ha pasado 1 seg");
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
                                                startLearning();
                                        }else if(action=="recognizing"){
                                                watching=true;
                                                startObjectRecognition();
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

}

