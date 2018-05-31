sudo apt-get -y install python3-pip
pip install --upgrade pip
python3 -m pip install -U discord.py
python3 -m pip install -U requests
git clone https://github.com/humankite/discord-poolbot.git poolbot
sudo cp -a ~/poolbot/deployment/masaribot.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable poolbot
sudo systemctl start poolbot
