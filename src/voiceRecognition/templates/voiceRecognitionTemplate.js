

function startEverything(){


    jQuery('.rte-zone').rte("css url", "toolbox images url");

    jQuery("#new_lang").change(function() {

        input = {"lang":jQuery(this).val()};
        jQuery.post("/voiceRecognition/getModels",input,function(data){

            array = data.split("::");

            list="<option value=''>${language['choose_model']}</option>";
            for(i=0;i<array.length;i++){
                list = list+"<option value='"+array[i]+"'>"+array[i]+"</option>";
            }

            jQuery("#languageModel").html(list);

        });

    });


    jQuery("#languageModel").change(function() {
        input = {"lang":jQuery("#new_lang").val(),"model":jQuery(this).val()};
        jQuery.post("/voiceRecognition/getFile",input,function(data){

            if(jQuery("#languageModel").val() != ""){
                jQuery("#divTextArea").show();
                jQuery("#buttons").show();
                
                //jQuery("#textArea").html("");
                arrayWords = data.split("\n");

                for(i=1;i<arrayWords.length;i++){            
                    jQuery("iframe").contents().find("body").append(arrayWords[i]+"</br>");
                }

            }else{
                jQuery("#divTextArea").hide();
                jQuery("#buttons").hide();
            }
        });
    });


    //if text area is edited, we need to pass all the test again
    jQuery("#textArea").change(function(){
        jQuery("#test2").attr('disabled', 'disabled');
        jQuery("#save").attr('disabled', 'disabled');        
    });
    

    var oldText="";
    jQuery("#test1").click(function(data){


        a = jQuery("iframe").contents().find("body").html();
        a = a.replace(/<br>/g,"\n");
        jQuery("#aux").html(a);
//        oldText=jQuery("iframe").contents().find("body").text();
        oldText=jQuery("#aux").text();

alert(oldText);
        jQuery('*').css('cursor', 'progress');

        input = {"text":oldText,"lang":jQuery("#new_lang").val()};
        jQuery.post("/voiceRecognition/test1",input,function(data){
            jQuery('*').css('cursor', 'auto');
            //data will have a list of words not allowed
            if(data == ""){ 
                //success
                jQuery("#test2").attr('disabled', '');
            }else{
                //fail
                arrayContent = oldText.split(" ");
                arrayError = data.split("::");

            }
        });
    });




}
