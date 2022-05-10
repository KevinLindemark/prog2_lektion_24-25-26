# prog2_lektion_24-25-26

# create and activate python virtual environment
python -m venv .venv

source .venv/bin/activate

# install packages for python
pip install -r requirements.txt 

# install packages that is needed for i2c
sudo apt-get update

sudo apt-get install python3-smbus python3-dev i2c-tools

# detect if i2c device is found
sudo i2cdetect -y 1
