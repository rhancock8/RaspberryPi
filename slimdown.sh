ts=`date +%d_%m_%Y-%H_%M_%S`
df -h | tee disk_before-${ts}.txt

sudo apt-get remove --purge libreoffice* -y
sudo apt-get remove --purge wolfram-engine -y
sudo apt-get remove -—purge chromium-browser -y
sudo apt-get remove --purge scratch2 -y
sudo apt-get remove --purge minecraft-pi  -y
sudo apt-get remove --purge sonic-pi  -y
sudo apt-get remove --purge dillo -y
sudo apt-get remove --purge gpicview -y
sudo apt-get remove --purge penguinspuzzle -y
sudo apt-get remove --purge oracle-java8-jdk -y
sudo apt-get remove --purge openjdk-7-jre -y
sudo apt-get remove --purge oracle-java7-jdk -y 
sudo apt-get remove --purge openjdk-8-jre -y

sudo apt-get clean
sudo apt-get autoremove -y

apt purge xserver* lightdm* raspberrypi-ui-mods vlc* lxde* chromium* desktop* gnome* gstreamer* gtk* hicolor-icon-theme* lx* mesa* -y

sudo apt-get clean
sudo apt-get autoremove -y

apt-get dist-upgrade -y

ts=`date +%d_%m_%Y-%H_%M_%S`
df -h | tee disk_after-${ts}.txt
