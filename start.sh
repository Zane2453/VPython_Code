#create a new screen session in detached mode
screen -d -m -S CyberPhysic
screen -S CyberPhysic -X screen -t "server" bash -c "python3 cyberphysic.py"
