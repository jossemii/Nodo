cat gateway.py 
python3
sudo docker ps
curl -sSL https://get.docker.com | sh
sudo apt-key fingerprint 0EBFCD88
curl -sSL https://get.docker.com | sh
sudo apt-key fingerprint 0EBFCD88
sudo nano /etc/systemd/system/gateway.service 
sudo systemctl status nginx
python3
sudo systemctl status gateway
sudo ufw
sudo ufw --help
sudo ufw app list
sudo systemctl status gateway
python3
cd /etc/systemd/system/
ls
nano gateway.service 
cd /home/pi/
ls
gunicorn --bind 0.0.0.0:8080 -w 4 gateway:run
source env/bin/activate
gunicorn --bind 0.0.0.0:8080 -w 4 gateway:run
nano /etc/systemd/system/gateway.service 
/home/pi/env/bin/gunicorn --workers 4 --bind unix:gateway.sock -m 007 gateway:run
/home/pi/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:run
/home/pi/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:gateway
deactivate
/home/pi/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:gateway
/home/pi/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:app
sudo /home/pi/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:gateway
rm -rf env/
pip3 install flask gunicorn
sudo pip3 install flask gunicorn
sudo gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:gateway
gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:gateway
gunicorn --workers 4 --bind unix:gateway.sock -m 007 gateway:gateway
gunicorn --workers 4 --bind unix:gateway.sock -m 007 gateway:app
sudo gunicorn --workers 4 --bind unix:gateway.sock -m 007 gateway:app
sudo gunicorn --workers 4 --bind 0.0.0.0:8080 -m 007 gateway:app
sudo apt-get install docker
sudo docker ps
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository    "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt upgrade
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository    "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo add-apt-repository    "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo reboot
                                                          python3
cd /etc/systemd/system/
ls
nano gateway.service
cat gateway.service
cd /etc/nginx/sites-available/
ls
cat gateway 
sudo systemctl status nginx
git log
cat gateway.service
ls
cat gateway 
ls
tail -f app.log 
ls
nano gateway.py 
cat gateway.py 
nano gateway.py 
cat gateway.py 
nano gateway.py 
docker ps
docker ps -a
nano gateway.py 
git add .
git log
git commit -m ".."
git config --global user.email "josemi.bnf@gmail.com"
git config --global user.name "josemibnf"
git commit -m ".."
git log
git push
git log
git pull
git log
sudo systemctl status nginx
sudo systemctl status gunicorn
sudo systemctl status gateway
sudo systemctl restart gateway.service 
sudo systemctl status gateway
sudo systemctl 
sudo systemctl enable gateway.service 
sudo systemctl status gateway
sudo systemctl enable gateway.service 
sudo systemctl status gateway
sudo systemctl reload-or-restart gateway.service 
sudo systemctl status gateway
sudo systemctl enable gateway
sudo systemctl status gateway
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             raspi-config
sudo raspi-config
systemctl status gateway.service 
tail -f app.log 
gunicorn -w 4 --bind localhost:9000 gateway:app
python3
sudo raspi-
sudo raspi-config 
