# CyberPhysic  

A platform for user to scan QRcode and play vpython by automatically create iottalk project and bind devices.

server example: https://hu.iottalk.tw  

 
Server Configuration
------------
#.  Edit ``CyberPhysic/static/config.js``

    
    #.  set cyberphysic_server to your domain name, ``Ex: https://hu.iottalk.tw``

#.  Edit ``CyberPhysic/config.py`` if you want to change CyberPhysic port

        default is 8888
  
  
HTTPS configuration (nginx)
------------
  
#.  use your machine with public ip
#.  download this repository  
#.  apply a domain name   
#.  install nginx
#.  vim ``/etc/nginx/sites-availble/default`` 

        #.  set <domain name>: domain name you applied
        #.  set <port>: your CyberPhysic port
     
::

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }
    server{
        server_name <domain_name>;
        location / {
            proxy_set_header Host $host;
            proxy_pass http://localhost:<port>;
    
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            client_max_body_size 2048M;
        }
        location /resources {
            rewrite /resources/(.*)   /$1 break;
            proxy_pass                http://127.0.0.1:8888/static;
            proxy_set_header          Host $host;
        }
    }    
    
    
    
6.  install certbot

::  

    python3 -m venv ~/my_venv
    source my_venv/bin/activate
    pip install certbot
    pip install -U letsencrypt-nginx
  
  
  
7.  enable certificate

::

/home/{your_username}/my_venv/bin/certbot --nginx -d <your_domain_name>


8.  exit venv:


    ``deactivate``  OR   ``source deactivate``


9.  reload nginx

::

    sudo service nginx reload
    
10. start server

::

    cd CyberPhysic
    ./startup.sh

11. Go to website
    ``https://<your domain name>``


Add new Vpython
------------

#.  put your vpython file (.py) under ``CyberPhysic/vp/py``    

        Note: file name is your vpython device model name which cannot be duplicate with other device models in iottalk server

#.  open browser and go to http://hu.iottalk.tw:7788/dfm , create new output device model (and odf if needed):

        Ex. ODM: Universe, ODF: Gravity, Speed
     
    
        If you want to control by smartphone, 
        please just use existing ODF Acceleration_O, Gyroscope_O or Orientation_O 
    
    
#.  create new input device model with IDFs in [RangeSlide1, RangeSlider2]:
    
    #.  Device Model name: Remote_control_<ODM name>
        
    Ex. IDM: Remote_control_Universe, IDF: [RangeSlider1, RangeSlider2]
    
        If you want to control by smartphone, 
        please just use existing IDF Acceleration-I, Gyroscope-I or Orientation-I. 
        This will push the raw data of acceleraiton, gyroscope or orientation. 
        Ex. IDM: Remote_control_Ball-collision, IDF: Acceleration-I.
        
#.  Done. Go back to CyberPhysic homepage and start to play.
