apt update && apt upgrade –y
cd /usr/src/
wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-13-current.tar.gz
tar xf asterisk-*-current.tar.gz
rm asterisk-13-current.tar.gz
cd asterisk-*/
apt install build-essential openssl libxml2-dev libncurses5-dev uuid-dev sqlite3 libsqlite3-dev pkg-config libjansson-dev git
./configure
make && make install
make samples
make config
/etc/init.d/asterisk start
cd /etc
mv asterisk asterisk.orig
git clone https://github.com/GoTrunk/asterisk-config.git asterisk
cd asterisk
git checkout dynamic-ip
asterisk –rx "core restart now"

