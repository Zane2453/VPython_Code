var mac_addr = 'Remote_control_' + odm_name;
var passwd = undefined;

$(function () {

    // var ip = 'http://'+location.hostname;
        var do_id = "{{in_do_id}}";
        var p_id = "{{p_id}}";
        var odm_name = "{{odm_name}}";
        var odf_list = JSON.parse('{{ odf_list | tojson }}');
        console.log('odf_list', odf_list, typeof(odf_list) );
        var registered = false;
        var d_name = p_id + '.Control_' + odm_name;

        $( window ).on( "load",  function () {
            //check_iframe_loaded();
            check_device_registered();

        });

        function check_device_registered(){

            if(!registered){
                window.setTimeout(check_device_registered,100);
            }else{
                //if device is already registered,query d_id
                query_d_id();
            }
        }

        //用d_name來query d_id
        function query_d_id(){
            var form_data = new FormData();
            form_data.append('d_name', d_name);

            var d_id = my_ajax(iottalk_ip, ccm_port, '/get_d_id_from_d_name',form_data);
            bind_device(d_id);
        }   
        
        //bind device
        function bind_device(d_id){
            var device_save_info = [ do_id, d_name, d_id];
            var form_data = new FormData();
            form_data.append('device_save_info', JSON.stringify(device_save_info));

            my_ajax(iottalk_ip, ccm_port, '/bind_device',form_data);
        }


    initial();
    slider_handler();

});

function initial(){

    function register_callback(result, password = ''){
        // console.log('rc result', result);
        registered = true;
        passwd = password;
        console.log('main.js:rc regietered');
    }
    var profile = {};
    profile['d_name'] = d_name;
    profile['dm_name'] = 'Remote_control_' + odm_name;
    profile['df_list'] = ['RangeSlider1','RangeSlider2'];

    /*
    df_list.forEach(function(element){
        profile['df_list'].push(element[0]);
    });
	*/

    console.log('profile : df_list', profile['df_list']);

    profile['is_sim'] = false;

    csmapi.set_endpoint(ip+":9999");
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
    /*
    $('.range-slider').on('change',function(){
        //初始值是0、1時，介面顯示會有問題，所以初始值設0、100，再除以100
        var value = ($(this).val() / 100);
        var idf = $(this).parent().parent().attr('name');
        $(this).parent().siblings('.value_label').text('val: ' + value);
        push(idf,parseFloat(value));
    });
    */

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