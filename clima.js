(function(ext) {
    // Cleanup function when the extension is unloaded
	var espera_comando = 100;
    ext._shutdown = function() {};

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };

    ext.get_temp = function(location, callback) {
        $.ajax({
              url: '{[host]}/clima.json',
              dataType: 'json',
              success: function( weather_data ) {
                  // Got the data - parse it and return the temperature
                  temperature = weather_data;
                  //callback(temperature);
                  window.setTimeout(function() {callback(temperature);}, espera_comando); //executa e espera o tempo do parametro 
              }
        });

/*
        $.ajax({
              url: '{[host]}/clima.json',
              dataType: 'jsonp',
              success: function( weather_data ) {
                  // Got the data - parse it and return the temperature
                  temperature = weather_data;
                  //callback(temperature);
                  window.setTimeout(function() {callback(temperature);}, espera_comando); //executa e espera o tempo do parametro 
              }
        });

*/        
        
        
    };

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['R', 'current temperature in city %s', 'get_temp', 'Boston, MA'],
        ]
    };

    // Register the extension
    ScratchExtensions.register('Weather extension', descriptor, ext);
})({});