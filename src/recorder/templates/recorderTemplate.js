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

   
/*   jQuery(function() {
        jQuery( "#selectable" ).selectable({
            stop: function() {
                var result = $( "#select-result" ).empty();
                jQuery( ".ui-selected", this ).each(function() {
                    var index=jQuery( "#selectable li" ).index( this );
                    var videoName = jQuery( "#element"+index ).attr("name");
                    jQuery("#video_player").html('<video height="320" width="480" tabindex="0" controls="controls"><source id="video_player" src="'+videoName+'"></source></video>"');
                });
            }
        });
    });*/
   loop = setInterval("renew_list()",5000);
   renew_list();
}


function renew_list(){
    jQuery.post("recorder/video_list_html",function(data){
        insertData2Html(data);
    });
}


function deleteVideo(name){
    param = {"videoName":name};
    jQuery.post("recorder/deleteVideo",param,function(data){
       insertData2Html(data);
       jQuery("#video_player").html("");
    });
}


function insertData2Html(data){

    jQuery("#video_list").html(data);



    jQuery("#video_list").sortable('toArray');

/*

    jQuery( "#selectable" ).selectable({
            stop: function() {
                var result = $( "#select-result" ).empty();
                jQuery( ".ui-selected", this ).each(function() {
                    var index=jQuery( "#selectable li" ).index( this );
                    var videoName = jQuery( "#element"+index ).attr("name");
                    jQuery("#video_player").html('<video height="320" width="480" tabindex="0" controls="controls"><source id="video_player" src="'+videoName+'"></source></video> ');
                    jQuery(".BasuraIcon").attr("class","BasuraIcon ui-icon ui-icon-trash delete-buttons");
                });
            }
        });

    jQuery(".BasuraIcon").attr("class","BasuraIcon ui-icon ui-icon-trash delete-buttons");
*/

}


function playVideo(videoName){
     jQuery("#video_player").html('<video height="320" width="480" tabindex="0" controls="controls"><source id="video_player" src="'+videoName+'"></source></video> ');

}

tabUnload = function(){
   clearInterval(loop); 
};
