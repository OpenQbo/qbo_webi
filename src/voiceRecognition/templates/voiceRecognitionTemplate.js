var oldText="";
var text="";

function startEverything(){


    //We have to leave this line in orther to make the iframe works
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

        jQuery("#test2").attr('disabled', 'disabled');
        jQuery("#save").attr('disabled', 'disabled');
        jQuery("#outputConsole").html("");

        input = {"lang":jQuery("#new_lang").val(),"model":jQuery(this).val()};
        jQuery.post("/voiceRecognition/getFile",input,function(data){

            if(jQuery("#languageModel").val() != ""){
                jQuery("#divTextArea").show();
                jQuery("#buttons_voiceRecog").show();
               
                jQuery("iframe").contents().find("body").html("");
 
                //jQuery("#textArea").html("");
//                arrayWords = data.split("\n");

//                for(i=0;i<arrayWords.length;i++){            
//                    jQuery("iframe").contents().find("body").append(arrayWords[i]+"</br>");
//                }


        data = data.replace(/\n/g,"</br>");
        jQuery("iframe").contents().find("body").append(data);


            }else{
                jQuery("#divTextArea").hide();
                jQuery("#buttons_voiceRecog").hide();
            }
        });
    });


    //if text area is edited, we need to pass all the test again
    jQuery("iframe").contents().find("body").keydown(function(e){
        jQuery("#test2").attr('disabled', 'disabled');
        jQuery("#save").attr('disabled', 'disabled');        
    });
    

    jQuery("#test1").click(function(data){
        jQuery("#test2").attr('disabled', 'disabled');
        jQuery("#save").attr('disabled', 'disabled');
        sendAndCheck(1);
    });

    jQuery("#test2").click(function(data){
        jQuery("#save").attr('disabled', 'disabled');
        sendAndCheck(2);
    });

    jQuery("#save").click(function(data){
        jQuery('*').css('cursor', 'progress');
        input = {"text":text,"lang":jQuery("#new_lang").val(),"model":jQuery("#languageModel").val()};
        jQuery.post("/voiceRecognition/saveToFile",input,function(data){
           jQuery('*').css('cursor', '');
           jQuery("#outputConsole").html("${language['saved_ok']}"); 
        });
    });




}




function sendAndCheck(numTest){
        //We get the text
        a = jQuery("iframe").contents().find("body").html();
        a = a.replace(/<span style\="color\:black;">/g,"");
        a = a.replace(/<span style="color:red;">/g,"");
        a = a.replace(/<\/span>/g,"");
        a = a.replace(/<div><br><\/div>/g,"<br>");
        a = a.replace(/<div>/g,"<br>");

        a = a.replace(
            new RegExp( "\\s*<br>\\s*", "g" ),
            "<br>");

        a = a.replace(
            new RegExp( "(<br>)+", "g" ),
            "<br>");


        a = a.replace(/<br>\[/g,"\n\n[");
        a = a.replace(/<br>/g,"\n");


        a = a.replace(/<\/div>/g,"");
        a = a.replace(/&nbsp;/g," ");
        a = a.replace(/<font color="#ff0000">/g,"");
        a = a.replace(/<font color="#000000">/g,"");
        a = a.replace(/<\/font>/g,"");


        oldText = a;

        jQuery('*').css('cursor', 'progress');

        input = {"text":oldText,"lang":jQuery("#new_lang").val()};
        jQuery.post("/voiceRecognition/test"+numTest,input,function(data){
        jQuery('*').css('cursor', '');

            //data will have a list of words not allowed
            if(data == ""){
                //success
                jQuery("iframe").contents().find("body").html("");

                arrayContent = oldText.split("\n");
                for(i=0;i<arrayContent.length;i++){
                    jQuery("iframe").contents().find("body").append(arrayContent[i]+"</br>");
                }


                if(numTest==1){
                    jQuery("#test2").removeAttr("disabled");
                    jQuery("#outputConsole").html("${language['test1_ok']}");
                }else if(numTest==2){
                    jQuery("#save").removeAttr("disabled");
                    jQuery("#outputConsole").html("${language['test2_ok']}");
                }

            }else{
                if(numTest==1){
                    jQuery("#outputConsole").html("${language['test1_wrong']}");
                }else if(numTest==2){
                    jQuery("#outputConsole").html("${language['test2_wrong']}");
                }


                //fail
                jQuery("iframe").contents().find("body").html("");
                arrayContent = oldText.split("\n");

                arrayError = data.split("::");
                for(i=0;i<arrayContent.length;i++){
                    arrayWords = arrayContent[i].split(" ");
                    line="";
                    for(j=0;j<arrayWords.length;j++){

                        if( arrayError.indexOf(arrayWords[j].toUpperCase()) != -1  ){
                            line=line+"<span style='color:red;'>"+arrayWords[j]+"</span> ";
                        }else{
                            line=line+"<span style='color:black;'>"+arrayWords[j]+"</span> ";
                        }
                    }
                    jQuery("iframe").contents().find("body").append(line+"</br>");
                }

            }
            text=oldText;
            oldText="";
        });

}




