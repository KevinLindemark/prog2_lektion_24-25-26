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
![09-05-2022-19-14-54](https://user-images.githubusercontent.com/58036568/167585130-e0a20b20-5d85-4b16-aeff-a074a73e686b.jpeg)
![09-05-2022-18-46-52](https://user-images.githubusercontent.com/58036568/167585138-aab13f8f-1aec-4c9a-987a-3312a1cc89b6.jpeg)
![09-05-2022-18-48-23](https://user-images.githubusercontent.com/58036568/167585143-f7368bd9-34d4-4b58-80c0-72176f08bfb6.jpeg)
![09-05-2022-19-10-59](https://user-images.githubusercontent.com/58036568/167585145-a39ba608-a483-4b85-bf49-5b059428a9bd.jpeg)
