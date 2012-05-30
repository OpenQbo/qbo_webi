var listCheck=new Array();

function startEverything(){



    jQuery("#soundCheckImg").attr("src","sysChecks/static/img/loading.gif");

    jQuery("#leftAudioButton").click(function(data){       

        jQuery("#stopLeftAudioButton").show();
        jQuery("#leftAudioButton").hide();

        jQuery.post('/checkers/index/soundCheck/play/left',function(data) {
            jQuery("#stopLeftAudioButton").hide();
            jQuery("#leftAudioButton").show();
            jQuery("#menuLeftAudio").show();
        });
    });





    jQuery("#rightAudioButton").click(function(data){

        jQuery("#stopRightAudioButton").show();
        jQuery("#rightAudioButton").hide();

        jQuery.post('/checkers/index/soundCheck/play/right',function(data) {
            jQuery("#stopRightAudioButton").hide();
            jQuery("#rightAudioButton").show();
            jQuery("#menuRightAudio").show();
        });
    });


    jQuery("#centerAudioButton").click(function(data){

        jQuery("#stopCenterAudioButton").show();
        jQuery("#centerAudioButton").hide();

        jQuery.post('/checkers/index/soundCheck/play/center',function(data) {
            jQuery("#stopCenterAudioButton").hide();
            jQuery("#centerAudioButton").show();
            jQuery("#menuCenterAudio").show();
        });
    });



    // Yes buttons
    jQuery("#yesButtonLeft").click(function(data){
        listCheck['left'] = true;
        jQuery("#checkLeft").show();
        finalCheck();
        jQuery("#leftOk").show();
        jQuery("#leftWrong").hide();
    });

    jQuery("#yesButtonRight").click(function(data){
        listCheck['right']=true;
        jQuery("#checkRight").show();
        finalCheck();
        jQuery("#rightOk").show();
        jQuery("#rightWrong").hide();
    });

    jQuery("#yesButtonCenter").click(function(data){
        listCheck['center']=true;
        jQuery("#checkCenter").show();
        finalCheck();
        jQuery("#centerOk").show();
        jQuery("#centerWrong").hide();
    });


    // No buttons
    jQuery("#noButtonLeft").click(function(data){
        listCheck['left'] = false;
        jQuery("#checkLeft").show();
        finalCheck();
        jQuery("#leftOk").hide();
        jQuery("#leftWrong").show();
    });

    jQuery("#noButtonRight").click(function(data){
        listCheck['right']=false;
        jQuery("#checkRight").show();
        finalCheck();
        jQuery("#rightOk").hide();
        jQuery("#rightWrong").show();
    });

    jQuery("#noButtonCenter").click(function(data){
        listCheck['center']=false;
        jQuery("#checkCenter").show();
        finalCheck();
        jQuery("#centerOk").hide();
        jQuery("#centerWrong").show();
    });










}


//We check if the three types of sound are correct or not
function finalCheck(){

    check = false;
    try{
        check = listCheck['left'] && listCheck['right'] && listCheck['center'] ;

        if (check == true){
           jQuery("#soundCheckImg").attr("src","sysChecks/static/img/ok.png");
        }else if(check == false){ //the other option was undefined
           jQuery("#soundCheckImg").attr("src","sysChecks/static/img/wrong.png");  
        }
    }catch(e){
        check = false;        
    }

}


