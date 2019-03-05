$( window ).on( "load",  function () {
    check_device_registered();
    turn_on_project();
    create_QRcode();
});

window.onunload = function(){
    csmapi.deregister(mac_addr, null);
    delete_project();
};

window.onbeforeunload = function(){
    csmapi.deregister(mac_addr, null);
    delete_project();
    return null;
};
window.onclose = function(){
    csmapi.deregister(mac_addr, null);
    delete_project();
};
window.onpagehide = function(){
    csmapi.deregister(mac_addr, null);
    delete_project();
};

function check_device_registered(){
    console.log('d_name:',d_name);
    if(d_name != null){
        query_d_id(d_name, function(response){
            bind_device(odo_id, d_name, response, function(response){
                get_proj_exception();
            });
        });
    }else{
        setTimeout(check_device_registered, 100);
    }
}

function turn_on_project(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    my_ajax(iottalk_ip, ccm_port, '/turn_on_project', form_data);
}

function create_QRcode(){
    let QRcode_url = "https://chart.googleapis.com/"
                +"chart?chs=250x250&cht=qr&choe=UTF-8&chl="
                +url;
    $('#qrcode').attr('src',QRcode_url);
    $('#hidden_link').on('click',function(){
        window.open(url);
    });
}

/*
function check_vp_reset(){
    var form_data = new FormData();
    form_data.append('p_id', project_info.p_id);
    var response = my_ajax(cyberphysic_server_ip, cyberphysic_server_port, '/is_reset', form_data);
    
    if(response.is_reset){
        //reload iframe and bind device
        console.log("vp is_reset resp:",response);
        $('#device-iframe').get(0).contentWindow.location.reload();
        setTimeout(check_iframe_loaded,1000);
    }
    setTimeout(check_vp_reset,1000);
}
*/

function get_proj_exception(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    my_ajax(iottalk_ip, ccm_port, '/get_exception_status', form_data, function(response){
        console.log("get_exception_status:",response);
        if(response.redraw == true){
            setTimeout(get_proj_exception,100);
        }  
    });
}

function delete_project(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    $.ajax({
        url: cyberphysic_server_ip + ":" + cyberphysic_server_port + '/delete_project',
        type: 'DELETE',
        data: form_data,
        cache: false,
        processData: false,
        contentType: false,
        async: async,
        dataType: 'json',
        error:function(e){
            console.log(url, ' error, e= ',e);
        },
        success:function(response){
            console.log(url, ' success, response=', response);
        },
    });
}
