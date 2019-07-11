var mac_addr = d_name;
var passwd = undefined;


$(function () {
    
    check_device_registered();
    initial();
    slider_handler();
    sensor_handler();
});

function check_device_registered(){
    if(!registered){
        window.setTimeout(check_device_registered,100);
    }else{
        //if device is already registered,query d_id
        query_d_id(d_name, function(response){
            bind_device(do_id, d_name, response);
        });
    }
}

function initial(){

    function register_callback(result, password){
        // console.log('rc result', result);
        registered = true;
        //for default parameter is not supported by es5
        passwd = (typeof password != 'undefined') ? password : '';
        console.log('main.js:rc regietered');
    }
    var profile = {};
    profile['d_name'] = d_name;
    profile['dm_name'] = 'Remote_control_' + odm_name;
    profile['df_list'] = [];

    /*
	$('.slidecontainer').each(function(index){
        console.log(index);
        console.log($(this).attr('name'));
        profile['df_list'].push($(this).attr('name'));
       
    });
    */
    idf_list.forEach(function(df){
        profile['df_list'].push(df);
    });

    console.log('profile: ', profile);

    profile['is_sim'] = false;

    csmapi.set_endpoint(iottalk_server + "/csm");
    csmapi.register(mac_addr, profile, register_callback);

}

function slider_handler(){

    $('input[type="range"]').rangeslider({
        // Feature detection the default is `true`.
        // Set this to `false` if you want to use
        // the polyfill also in Browsers which support
        // the native <input type="range"> element.
        polyfill: false,

        // Default CSS classes
        rangeClass: 'rangeslider',
        disabledClass: 'rangeslider--disabled',
        horizontalClass: 'rangeslider--horizontal',
        verticalClass: 'rangeslider--vertical',
        fillClass: 'rangeslider__fill',
        handleClass: 'rangeslider__handle',

        // Callback function
        onInit: function() {
            this.output = $( '<output class="column has-text-centered">' ).insertAfter( this.$range ).html( this.$element.val() );
        },
        // Callback function
        onSlide: function(position, value) {    
            //console.log('onSlide:',position,value);
            this.output.html(value);
        },
        // Callback function
        onSlideEnd: function(position, value) {
            console.log('onSlideEnd:',this.identifier,value);
            //pushback(value)
            console.log(this.$element);
            console.log(this.$element.get(0).parentNode.parentNode.attributes.name);
            var idf = this.$element.get(0).parentNode.parentNode.attributes.name.value;
            push(idf,parseFloat(value));
        }
    });
}

// Shared function
function push (idf_name, data, callback) {
    console.log('push idf_name ', idf_name, data);

    if (!(data instanceof Array)) {
        data = [data];
    }

    var ajax_callback = function(result){

        if (result){// http request success
           console.log('Successed: '+ result);
        }else{// http request failed
           console.log('failed: '+ result.status +','+ result.responseText);
        } 

        if(callback){
            console.log(typeof(callback));
            callback();//push callback
        }
    }
    csmapi.push(mac_addr, passwd, idf_name, data, ajax_callback);

}