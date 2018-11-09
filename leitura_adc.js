(function(ext) {    
	
	var espera_comando = 100;
	var ip_ponte = "{[host]}/";
    ext._shutdown = function() {};

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };

//===================================================================================
// bloco saida digital, obs: alterar descritor do bloco para parametro
	ext.saida_digital = function(valorsaida, callback) {        
	  try {	
        $.ajax({
              url: ip_ponte  + "/led/sd_13:" + valorsaida,    // http://localhost:3000/eco/alo         
              success: function( dado_sensor ) {
                  resposta = dado_sensor;
                  window.setTimeout(function() {callback(resposta);}, espera_comando); //executa e espera o tempo do parametro                                    
              }
			  
        });
	      }
	      catch(err)
		  {
            //Console.log ("erro: " + err.message);
		  }
	
    };	
//===================================================================================	

//===================================================================================
// bloco servo, obs: alterar descritor do bloco para parametro
	ext.comando_servo = function(valorsaida, callback) {        
	  try {	
        $.ajax({
              url: ip_ponte  + "servo:" +valorsaida,    // http://localhost:3000/eco/alo         
              success: function( dado_sensor ) {
                  resposta = dado_sensor;
                  window.setTimeout(function() {callback(resposta);}, espera_comando); //executa e espera o tempo do parametro
              }
			  
        });
	      }
	      catch(err)
		  {
            //Console.log ("erro: " + err.message);
		  }
	
    };	
//===================================================================================	

//===================================================================================
// bloco leitura ADC 0, obs: alterar descritor do bloco para parametro
	ext.comando_adc = function(callback) {        
	  try {	
        $.ajax({
              url: ip_ponte  + "ana0",     
              success: function( dado_sensor ) {
                  resposta = dado_sensor;
				  window.setTimeout(function() {callback(resposta);}, espera_comando); //executa e espera o tempo do parametro                  
                  
                  
              }
			  
        });
	      }
	      catch(err)
		  {
            Console.log ("erro: " + err.message);
		  }
	
    };	
//===================================================================================	

    // Block and block menu descriptions
    var descriptor = {
        blocks: [         		    
			['w', 'Saida Digital 13 = %s', 'saida_digital', '1'],
			['w', 'Servo Pino 9 %s', 'comando_servo', '90'],
			['R', 'Ler Analogica 0', 'comando_adc'],
			
			
        ]
    };

    // Register the extension
    ScratchExtensions.register('Robo ORI', descriptor, ext);
})({});
