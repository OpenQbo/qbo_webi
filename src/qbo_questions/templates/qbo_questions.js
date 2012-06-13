


function startEverything(){


    //We take questions from the grammar 
    input = {"lang":"en","model":"questions"};
    jQuery.post("/voiceRecognition/getFile",input,function(data){
        questions_list = data.split("\n");

        stop_at_next_tag = false; //We only want the sentences after [senteces], when the next tag comes, i.e. [names], we skip it
        for(i in questions_list){
            if( questions_list[i] == "[sentences]" ){
                stop_at_next_tag = true;
            }else if ( stop_at_next_tag ){

                if(questions_list[i][0] == "[" || questions_list[i]==""){
                    break;
                }else{            
                    jQuery("#listQuestions").append("<option>"+questions_list[i]+"</option>");
                }
            } 
        }
    });


    jQuery.getJSON("/qbo_questions/getActualDialogue", function(data){
        fillTable(data);
    });

   


    jQuery("#addSentence").click(function(data){

        answer = jQuery("#answer").val().replace('"','\\"');

        param = {"question": jQuery("#listQuestions").val() , "answer": answer };
        jQuery.getJSON("/qbo_questions/addSentence",param,function(data){
           fillTable(data);
        });
    });


}



function fillTable(data){
     html = "";
        for (var key in data) {


            html = html + ' <tr> <td> '+ key +' <img id="'+key+':::" alt="Delete '+key+'"  class="delete_sentence" src="/qbo_questions/static/img/close.png"></img>  </td> <td> <ul> ';

            for (i=0;i<data[key].length;i++){

                aux_id = key.replace(/"/g,'&quot;')+":::"+data[key][i].replace(/"/g,'&quot;'); 

                

                html = html + '<li>'+data[key][i]+' <img id="'+aux_id+'" alt="Delete '+aux_id+'"  class="delete_sentence" src="/qbo_questions/static/img/close.png"></img>  </li>';
            }


            html = html+" </ul> </td> /tr> <hr />";


       }

        jQuery("#dialogue_table").html(html);


    //We define the delete sentence button behaviour
    jQuery(".delete_sentence").click(function(data){
        param = {"sentence2delete": jQuery(this).attr("id") };
        jQuery.getJSON("/qbo_questions/deleteSentence",param,function(data){
           fillTable(data);
        });
    });


}

