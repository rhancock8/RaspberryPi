# EnviroPlus polling collateral

```bash  

# Login on console as user: pi

passwd root

vi /etc/ssh/sshd_config 

# Make sure PermitRootLogin and PasswordAuthentication are both set to yes

systemctl enable sshd
systemctl restart sshd

apt-get update
apt-get upgrade
reboot

chmod 755 slimdown.sh 
./slimdown.sh 

passwd --lock pi

chage -l root
chage -l pi
chage -m -1 -M -1 -W -1 -E -1 root

useradd enviro -m -d /opt/enviro -s /bin/bash
passwd enviro
chage -m -1 -M -1 -W -1 -E -1 enviro

echo "enviro ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/enviro

apt-get install python-numpy python-smbus python-pil python-setuptools

raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0

pip install enviroplus
python -m pip uninstall sounddevice

pip3 install enviroplus

apt-get install snmpd
apt-get update && sudo apt-get install snmp snmpd snmp-mibs-downloader

systemctl stop snmpd
# Add extend to the list of default snmpd params (after the -m)
vi /etc/default/snmpd 

vi /etc/snmp/snmp.conf 

adduser enviro spi
adduser enviro i2c
adduser enviro gpio
adduser enviro video

adduser Debian-snmp spi
adduser Debian-snmp i2c
adduser Debian-snmp gpio
adduser Debian-snmp video
systemctl enable snmpd
systemctl start snmpd

snmpwalk -v2c -c public 127.0.0.1  .1.3.6.1.3

crontab -l
@reboot /bin/bash /opt/scripts/startdisplayonboot.sh  &


```
