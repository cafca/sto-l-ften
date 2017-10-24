# Stoßlüften Climate Control

Stoßlüften Climate Control gives you fully automatic instructions for venting
a room using an Arduino, the DHT11 temperature and humidity sensor and some
light processing with Python Pandas.

- Plots temperature, humidity and their respective change rates
- Detects sudden temperature drops and awaits humidity stabilisation before
instructing you to close window again
- Additional notice when original temperature is restored
- Voice output using macOS "say" command

# Usage

Find the Arduino code in `./DHT11/DHT11.ino`. Make sure you have the DHT11
library installed before compiling. Connect via USB to enable serial connection.

Install Python dependencies

    $ pip install -r requirements.txt

Start the serial data receiver

    $ python temp.py

It will keep running in the background. Open a new terminal window and start
the plotting and climate control script.

    $ python plot.py

Data will be collected in `data/my_room.json`. Change the DATAFILE value in
temp.py to change to a different file.

# Lizenz

MIT, see LICENSE file.
