"""Plot data and check for climate control events."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sh import say
from datetime import datetime, timedelta

# Contains JSON lines with time series data
DATAFILE = "./data/my_room.json"

# Temperature threshold for Stoßlüften start
SL_THRESHOLD = -0.09

# Humidity threshold for Stoßlüften end
SL_HUM_THRESHOLD = 0.01

# Parameters for voice command
VOICE_PARAMS = ['-v', 'Oliver']


class Plot(object):
    """Manage a Matplotlib plot."""

    def __init__(self):
        """Prepare Seaborn styles, interactive mode and Plot state."""
        sns.set()
        sns.set_style("white")
        sns.set_palette(sns.color_palette("Paired"))

        plt.ion()

        # Get current plot axes
        self.axes = plt.gca()

        # Start datetime of current Stoßlüften
        self.sl_start = datetime.now() - timedelta(minutes=1)

        self.target_temperature = 20.0

    def update(self):
        """Update data, compute percent change and smoothen values."""
        with open(DATAFILE) as f:
            self.df = pd.read_json(f, lines=True)

        # Create new columns with temperature and humidity percent change
        self.chdf = self.df.assign(
            tempchange=self.df.temperature.pct_change(periods=180).values,
            humchange=self.df.humidity.pct_change(periods=90).values
        )

        # Smoothen values
        for v in ['humidity', 'humchange', 'temperature', 'tempchange']:
            self.chdf[v] = self.chdf[v].rolling(window=30).mean()

        print(self.chdf.tail())

    def draw(self):
        """Draw plots using Pandas Dataframe plot method."""
        # Clear current axes
        plt.cla()

        # Select last hour of data
        cutoff = datetime.now() - timedelta(minutes=60)

        self.axes = self.chdf[lambda x: x.date > cutoff].plot(
            x='date',
            y=['humidity', 'humchange', 'temperature', 'tempchange'],
            subplots=True,
            sharex=True,
            ax=plt.gca())

    def pause(self):
        """Pause with mpl to prevent blocking."""
        plt.pause(5)

    def climate_control(self):
        u"""State machine for climate control / Stoßlüften."""
        # Current temperature percent change
        sl_temp = self.df.temperature.pct_change(periods=180).iloc[-1]

        # Current humidity percent change
        sl_hum = self.df.humidity.pct_change(periods=90).iloc[-1]

        print("SLT {}".format(sl_temp))
        print("SLH {}".format(sl_hum))

        # Stoßlüften underway, wait for humidity change to return to 0
        if self.sl_start is not None:
            if abs(sl_hum) < SL_HUM_THRESHOLD:
                td = (datetime.now() - self.sl_start).seconds / 60
                self.sl_start = None
                print("Venting finished")
                say("Achtung! Fenster schließen. {} minutes have passed.".format(int(td)), *VOICE_PARAMS)
            else:
                print("Current humchange target: {}".format(SL_HUM_THRESHOLD))
                # Weiter lüften
                pass

        # Check for Stoßlüften threshold to be reached
        elif sl_temp < SL_THRESHOLD:
            say("Stoßlüften aktiviert", *VOICE_PARAMS)
            self.sl_start = datetime.now()
            self.target_temperature = self.df.temperature.iloc[-180]
            print("New target temperature {} C".format(self.target_temperature))

        # Check for reaching the current target temperature
        if self.target_temperature is not None:
            print("Current target: {} C".format(self.target_temperature))
            if self.df.temperature.iloc[-1] >= self.target_temperature:
                self.target_temperature = None
                print("Temperature target reached")
                say("Temperature restored. Ready for next Stoßlüften cycle.", *VOICE_PARAMS)

    def run(self):
        """Run update cycle in paused loop."""
        try:
            while True:
                p.update()
                p.draw()
                p.climate_control()
                p.pause()
        except KeyboardInterrupt:
            print("\nGoodbye")


if __name__ == "__main__":
    p = Plot()
    p.run()
