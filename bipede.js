(function(ext) {    
	
	var espera_comando = 100;
	var ip_ponte = "{[host]}/";
	//var ip_ponte = "http://192.168.0.10:3000/";
	// Cleanup function when the extension is unloaded
    ext._shutdown = function() {};

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };

//===================================================================================
// bloco andar, obs: alterar descritor do bloco para parametro
	ext.andar = function(direcao, velocidade, callback) {        
	  try {	
        $.ajax({
              url: ip_ponte  + "andar:" + direcao + ":" + velocidade,    // http://localhost:3000/eco/alo         
              success: function( dado_sensor ) {
                  // Got the data - parse it and return the temperature
                  resposta = dado_sensor;
				  formatado = resposta.substring(23,resposta.length-8);
                  //callback(formatado.replace(/\s/g, ""));
				  window.setTimeout(function() {callback(formatado.replace(/\s/g, ""));}, espera_comando); //executa e espera o tempo do parametro
              }
			  
        });
	      }
	      catch(err)
		  {
            //Console.log ("erro: " + err.message);
		  }
	
    };	


 //===================================================================================
// bloco moonwalker, obs: alterar descritor do bloco para parametro
ext.moon = function(lado, velocidade, callback) {        
    try {	
      $.ajax({
            url: ip_ponte  + "moon:" + lado + ":" + velocidade,    // http://localhost:3000/eco/alo         
            success: function( dado_sensor ) {
                // Got the data - parse it and return the temperature
                resposta = dado_sensor;
                formatado = resposta.substring(23,resposta.length-8);
                //callback(formatado.replace(/\s/g, ""));
                window.setTimeout(function() {callback(formatado.replace(/\s/g, ""));}, espera_comando); //executa e espera o tempo do parametro
            }
            
      });
        }
        catch(err)
        {
          //Console.log ("erro: " + err.message);
        }
  
  };
  

 //===================================================================================
// bloco inclinar, obs: alterar descritor do bloco para parametro
ext.inclinar = function(lado, velocidade, callback) {        
    try {	
      $.ajax({
            url: ip_ponte  + "incl:" + lado + ":" + velocidade,    // http://localhost:3000/eco/alo         
            success: function( dado_sensor ) {
                // Got the data - parse it and return the temperature
                resposta = dado_sensor;
                formatado = resposta.substring(23,resposta.length-8);
                //callback(formatado.replace(/\s/g, ""));
                window.setTimeout(function() {callback(formatado.replace(/\s/g, ""));}, espera_comando); //executa e espera o tempo do parametro
            }
            
      });
        }
        catch(err)
        {
          //Console.log ("erro: " + err.message);
        }
  
  };	     

//===================================================================================
// bloco levantar, obs: alterar descritor do bloco para parametro
ext.levantar = function(velocidade, callback) {        
    try {	
      $.ajax({
            url: ip_ponte  + "leva:" + velocidade,    // http://localhost:3000/eco/alo         
            success: function( dado_sensor ) {
                // Got the data - parse it and return the temperature
                resposta = dado_sensor;
                formatado = resposta.substring(23,resposta.length-8);
                //callback(formatado.replace(/\s/g, ""));
                window.setTimeout(function() {callback(formatado.replace(/\s/g, ""));}, espera_comando); //executa e espera o tempo do parametro
            }
            
      });
        }
        catch(err)
        {
          //Console.log ("erro: " + err.message);
        }
  
  };	       

//===================================================================================
// bloco posicao inicial, obs: alterar descritor do bloco para parametro
ext.iniciar = function(callback) {        
    try {	
      $.ajax({
            url: ip_ponte  + "inic:",    // http://localhost:3000/eco/alo         
            success: function( dado_sensor ) {
                // Got the data - parse it and return the temperature
                resposta = dado_sensor;
                formatado = resposta.substring(23,resposta.length-8);
                //callback(formatado.replace(/\s/g, ""));
                window.setTimeout(function() {callback(formatado.replace(/\s/g, ""));}, espera_comando); //executa e espera o tempo do parametro
            }
            
      });
        }
        catch(err)
        {
          //Console.log ("erro: " + err.message);
        }
  
  };	         

//===================================================================================	


    // Block and block menu descriptions
    var descriptor = {
        blocks: [         		               
            ['w', 'Andar para %m.Direcao e %m.Velocidade', 'andar', 'frente', 'lento'],
            ['w', 'Moonwalker para %m.Lado e %m.Velocidade', 'moon', 'direita', 'lento'],
            ['w', 'Inclinar para %m.Lado e %m.Velocidade', 'inclinar', 'direita', 'lento'],
            ['w', 'Levantar %m.Velocidade', 'levantar',  'lento'],
            ['w', ' Posicao Inicial ', 'iniciar']    
        ],
        menus: {
            Direcao: ['frente', 'tras'],     
            Velocidade: ['lento', 'rapido'], 
            Lado: ['direita', 'esquerda']        
        },

    };

    // Register the extension
    ScratchExtensions.register('Robo Bipede', descriptor, ext);
})({});