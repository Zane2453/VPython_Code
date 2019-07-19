"use strict";

var acc  = {};
var gyro = {};
var orient = {};

var push_interval = 150;

function sensor_handler(){
    let name_info = ['Acceleration-I','Gyroscope-I','Orientation-I'];
    
    if(idf_list.some(function(idf_name){
        return ($.inArray(idf_name, name_info) != -1)
    })){
        set_sensor_handler();
        requestAnimationFrame(update_layout);
        setInterval(push_sensor_value, push_interval);
    }
    
}


function set_sensor_handler(){
    console.log('set sensor handler');
    let sensor_info = {
        'Acceleration': 'acceleration',
        'Gyroscope': 'rotationRate',
    }

    function event_handler(event, name, type, data){
        let tmp = event[sensor_info[name]];
        if(name == 'Acceleration'){
            acc.x = tmp.x;
            acc.y = tmp.y;
            acc.z = tmp.z;
            console.log('acc:', acc);
        }else if(name == 'Gyroscope'){
            gyro.x = tmp.alpha;
            gyro.y = tmp.beta;
            gyro.z = tmp.gamma;
            console.log('gyro:', gyro);
        }else if(name == 'Orientation'){
            orient.x = event.alpha;
            orient.y = event.beta;
            orient.z = event.gamma;
            console.log('orient:', orient);
        }
    }

    window.addEventListener('devicemotion', function(event){
        event_handler(event, "Acceleration", "smartphone");
        event_handler(event, "Gyroscope", "smartphone");
    });

    window.addEventListener('deviceorientation', function(event){
        event_handler(event, 'Orientation', "smartphone");
    });

}

function push_sensor_value(){
    let name_info = [
        ['Acceleration-I', 'acc', acc, null],
        ['Gyroscope-I', 'gyr', gyro, null],
        ['Orientation-I', 'ori', orient, null],
    ];

    name_info.forEach(function(info){
        push_handler(info[0], info[1], info[2], info[3]);
    });

    function push_handler(name, btn_name, obj, type){

        if($.inArray(name, idf_list) == -1){
            return;
        }
        if(type == 'morsensor'){
            push(name, [obj]);
            return;
        }

        push(name, [obj.x, obj.y, obj.z]);
    }
}

function update_layout() {
    var text_info = [
        ['Acceleration', 'A', acc, null],
        ['Gyroscope', 'G', gyro, null],
        ['Orientation', 'O', orient, null],
    ];

    text_info.forEach(function(info){
        console.log('update info ',info);
        update_text(info[0],info[1],info[2],info[3]);
    });

    requestAnimationFrame(update_layout);

    function update_text(name, tag, obj, type){
        $('#'+tag+'x').text(Number.parseFloat(obj.x).toFixed(2));
        $('#'+tag+'y').text(Number.parseFloat(obj.y).toFixed(2));
        $('#'+tag+'z').text(Number.parseFloat(obj.z).toFixed(2));
    }
}
