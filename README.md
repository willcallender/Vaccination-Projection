# Vaccination-Projection
Projects when the US will be fully vaccinated.

## How it works
This program downloads data about the current progress of COVID-19 vaccinations in the United States to project the total number of vaccinations going forward. It does this by getting data about the number of vaccinations per day since vaccines first became approved. It then runs linear regression over that data to determine how fast the number of daily vaccinations is increasing. It integrates this projection and accounts for the current number of people fully vaccinated and the fact that both vaccines require 2 shots for full vaccination. It shows this with some graphs and a crude projection for when the US could be fully vaccinated.

## Files it creates
It creates 2 csv files and 2 new optional png files every day.

## Dependencies
This program is dependent on the following modules not installed by default in python:
pywget
scipy
matplotlib

The file environment.yml is an exported anaconda environment that should work to run this script.
Alternatively, install.sh *should* install the dependenceis on Ubuntu, but I've only tested it on 20.04.

## Legal information
The data is sourced (by default) from the [Our World in Data COVID-19 repository](https://github.com/owid/covid-19-data) under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). This code is licensed likewise.

I cannot predict the future, and neither can this program. These projections were created as a way for me to be less bored while inside, and should not be used in place of projections provided by experts. They should be used merely for entertainment purposes or for learning about coding, not for anything where the accuracy of projections is important. By using this code you acknowledge that I am not responsible for any harm caused by its misuse.

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg