if(navigator.userAgent.indexOf("MSIE")>=0) navegador=0; // IE
else navegador=1; // Demas


jQuery('#sysCheckAccordion').accordion({ 
        change: function(event, ui){
                var clicked = jQuery(this).find('.ui-state-active').attr('id');
                //jQuery('#'+clicked).load('/chekers/'+clicked); //Cambiar por funcion AJAX que llama a '/chekers/'+clicked

                // Obtengo el XML y separo sus nodos
                var resp=respuesta; //Parsear JSON o XML o lo que sea
                var javascript=respuesta.jsElement; //El código javascript
                var css=respuesta.cssElement; //El código css
                var html=respuesta.htmlElement; //El código HTML

                //Metemos el HTML en el div correspondiente
                

                // Creo el nuevo JS
                var etiquetaScript=document.createElement("script");
                document.getElementsByTagName("head")[0].appendChild(etiquetaScript);
                etiquetaScript.text=javascript;

                // Creo el nuevo CSS
                var etiquetaStyle=document.createElement("style");
                document.getElementsByTagName("head")[0].appendChild(etiquetaStyle);

                if(navegador==0)
                {
                    var contenidoCSS=css.split("{");
                    var ultimaEtiquetaStyle=document.styleSheets[document.styleSheets.length-1];
                    ultimaEtiquetaStyle.addRule(contenidoCSS[0], "{"+contenidoCSS[1]);
                }
                else
                {
                    var contenidoCSS=document.createTextNode(css);
                    etiquetaStyle.appendChild(contenidoCSS);
                }
        }
});
