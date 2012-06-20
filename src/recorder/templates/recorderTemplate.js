function startEverything(){
    jQuery("#start_record").click(function(data){
        jQuery.post("recorder/record",function(data){
        if (data==1){
            jQuery("#button").attr("src","/recorder/static/img/stop.png");
            jQuery("#recording").attr("src","/recorder/static/img/recording.gif");
        }
        else{
           jQuery("#button").attr("src","/recorder/static/img/rec.png");
           jQuery("#recording").attr("src","/recorder/static/img/nothing.png");
        }
       });
    });

    jQuery.post("recorder/status",function(data){
    if (data==1){
       jQuery("#button").attr("src","/recorder/static/img/stop.png");
       jQuery("#recording").attr("src","/recorder/static/img/recording.gif");
    }
    else{
       jQuery("#button").attr("src","/recorder/static/img/rec.png");
       jQuery("#recording").attr("src","/recorder/static/img/nothing.png");
    }
   });
}
