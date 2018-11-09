 (function(ext) {
  
        // Cleanup function when the extension is unloaded
        ext._shutdown = function() {};        // Status reporting code
        // Use this to report missing hardware, plugin or unsupported browser
        ext._getStatus = function() {
            return {status: 2, msg: 'Installed'};        
        };
        
        var descriptor = {
            blocks: [
                [' ', 'hello world', 'helloWorld']
            ]
        };
        
        //The Hello world function
        ext.helloWorld = function(){
        	alert('Hello World!')
         try {
           $.get("{[host]}/verde2", function(data, status){
                //console.log(data);
                //console.log(status);
                alert("Foiii-{[host]}");            
           });             
         } catch (e) {
           console.log(e);
           alert(e.message);
         }
                  
        alert('Hello World!-Fim')         
         
        };

        ScratchExtensions.register('Hello World', descriptor, ext);
    })({});