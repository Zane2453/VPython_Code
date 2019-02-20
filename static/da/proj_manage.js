/*
    [TODO]
    create project and create connection done by server, not html
*/
$( window ).on( "load",  function () {
    check_project_name_is_exist();
});

window.onunload = function(){
    csmapi.deregister(project_info.output_device_info.mac_addr, null);
    delete_project();
};

window.onbeforeunload = function(){
    csmapi.deregister(project_info.output_device_info.mac_addr, null);
    delete_project();
    return null;
};
window.onclose = function(){
    csmapi.deregister(project_info.output_device_info.mac_addr, null);
    delete_project();
};
window.onpagehide = function(){
    csmapi.deregister(project_info.output_device_info.mac_addr, null);
    delete_project();
};

function check_project_name_is_exist(){
    var proj_name = "CyberPhysic_"+project_info.output_device_info.dm_name+"_"+Math.floor((Math.random() * 100) + 1);
    var form_data = new FormData();
    form_data.append('project_name', proj_name);

    function callback(response){
        console.log(response);
        if(response.status == "ok"){
            if(response.is_exist){
                //project_name重複
                proj_name = "CyberPhysic_"+project_info.output_device_info.dm_name+"_"+Math.floor((Math.random() * 100) + 1);
                setTimeout(check_project_name_is_exist, 100, proj_name);
            }else{
                project_info.proj_name = proj_name;
                create_project(proj_name,"");
            }
        }
    }
    my_ajax(iottalk_ip, ccm_port, '/check_project_name_is_exist', form_data, callback);
    
}

function create_project(p_name,p_pwd){
    var form_data = new FormData();
    form_data.append('p_name', p_name);
    form_data.append('p_pwd', p_pwd);

    function callback(response){
        project_info.p_id = response;

        get_model_info(project_info.output_device_info.dm_name,"out");
        get_model_info("Remote_control_"+project_info.output_device_info.dm_name,"in");
        check_do_created();
    }

    my_ajax(iottalk_ip, ccm_port, '/new_project', form_data, callback);
}

function get_model_info(model_name,in_or_out){
    var model_info = {'model_name':model_name, 'p_id':project_info.p_id};
    var form_data = new FormData();
    form_data.append('model_info', JSON.stringify(model_info));

    if(in_or_out == "out"){
        function callback(response){
            project_info.output_device_info.dm_id = response.model_id;

            //output device如果有多個device feature，odf全部取，不取idf
            feature_list = {
                'idf_list': [],
                'odf_list': response.odf,
                'model_name': response.model_name,
                'do_id': 0,
                'p_id': project_info.p_id,
            }
            save_device_object_info(feature_list, "out");
        }
    }else{
        function callback(response){
            project_info.idm_id = response.model_id;

            //input device smartphone只取Acceleration、Gyroscope、Orientation
            feature_list = {
                'idf_list': response.idf,
                'odf_list': [],
                'model_name': response.model_name,
                'do_id': 0,
                'p_id': project_info.p_id,
            }
            save_device_object_info(feature_list, "in");
        }
    }
    my_ajax(iottalk_ip, ccm_port, '/get_model_info', form_data, callback);
}

function save_device_object_info(feature_list, in_or_out){
    var form_data = new FormData();
    form_data.append('model_info', JSON.stringify(feature_list));

    my_ajax(iottalk_ip, ccm_port, '/save_device_object_info', form_data, function(response){
        if(response.responseText == "ok"){
            if(in_or_out == "out"){
                odo_created = true;
            }else{
                ido_created = true;
            }       
        }
    });
}

function check_do_created(){
    if(odo_created && ido_created){
        reload_data();
    }else{
        setTimeout(check_do_created,300);
    }
}

function reload_data(){
    var form_data = new FormData();
    form_data.append('p_id', project_info.p_id);

    function callback(response){
        console.log(response);
        save_device_info(response);
        create_connection();
    }

    my_ajax(iottalk_ip, ccm_port, '/reload_data', form_data, callback);
}

function save_device_info(info){
    let in_device_info = info.in_device[0];
    let out_device_info = info.out_device[0];

    project_info.input_device_info.do_id = in_device_info.in_do_id;
    in_device_info.p_idf_list.forEach(function(idf_info){
        project_info.input_device_info.df_list.push({'id':idf_info[1],'name':idf_info[0]});
    });

    project_info.output_device_info.do_id = out_device_info.out_do_id;
    out_device_info.p_odf_list.forEach(function(odf_info){
        project_info.output_device_info.df_list.push({'id':odf_info[1],'name':odf_info[0]});
    });
}

function create_connection(){
    let promises = [];

    for(var i = 0; i < project_info.output_device_info.df_list.length; i++){
        var connection_info = ["Join "+(i+1).toString(),i,project_info.input_device_info.df_list[i].id,project_info.output_device_info.df_list[i].id];
        var setting_info = {'connect_info':connection_info,'p_id':project_info.p_id};
        
        var form_data = new FormData();
        form_data.append('setting_info', JSON.stringify(setting_info));
        var req = my_ajax(iottalk_ip, ccm_port, '/save_connection_line', form_data, (response)=>{
            project_info.na_id_list.push(response.na_id);
        });
        promises.push(req);
    }
    $.when.apply(null, promises).done(()=>{
        check_device_registered();
        turn_on_project();
        create_QRcode();

        //periodically send request to check reset flag
        // setTimeout(check_vp_reset,1000);
        console.log('project_info= ',project_info);
    });
}


function check_device_registered(){
    console.log('d_name:',project_info.d_name);
    if(project_info.d_name != null){
        query_d_id(project_info.d_name, function(response){
            bind_device(project_info.output_device_info.do_id, project_info.d_name, response, function(response){
                get_proj_exception();
            });
        });
    }else{
        setTimeout(check_device_registered, 100);
    }
}

function turn_on_project(){
    var form_data = new FormData();
    form_data.append('p_id', project_info.p_id);

    my_ajax(iottalk_ip, ccm_port, '/turn_on_project', form_data);
}

function create_QRcode(){
    var URL = "https://chart.googleapis.com/"
                +"chart?chs=250x250&cht=qr&choe=UTF-8&chl="
                +cyberphysic_server_ip+":"+cyberphysic_server_port+"/rc/"+ project_info.output_device_info.dm_name + "/" +project_info.p_id
                +"/"+project_info.output_device_info.dm_id
                +"/"+project_info.input_device_info.do_id;
    $('#qrcode').attr('src',URL);
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
    form_data.append('p_id', project_info.p_id);

    my_ajax(iottalk_ip, ccm_port, '/get_exception_status', form_data, function(response){
        console.log("get_exception_status:",response);
        if(response.redraw == true){
            setTimeout(get_proj_exception,100);
        }  
    });
}

function delete_project(){
    var form_data = new FormData();
    form_data.append('p_id', project_info.p_id);
    my_ajax(iottalk_ip, ccm_port, '/delete_project',form_data);
}
