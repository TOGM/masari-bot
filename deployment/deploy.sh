sudo apt-get -y install python3-pip
pip install --upgrade pip
python3 -m pip install -U discord.py
python3 -m pip install -U requests
cd ~
git clone https://github.com/togm/masari-bot.git masaribot
sudo cp -a ~/masaribot/deployment/masaribot.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable masaribot
sudo systemctl start masaribot
