"""
Created on Wed Feb 17 13:27:55 2021

@author: William Callender

This program downloads data about the current progress of COVID-19 vaccinations
in the United States to project the total number of vaccinations going forward.
It does this by getting data about the number of vaccinations per day since
vaccines first became approved. It then runs linear regression over that data
to determine how fast the number of daily vaccinations is increasing. It
integrates this projection and accounts for the current number of people fully
vaccinated and the fact that both vaccines require 2 shots for full
vaccination. It shows this with some graphs and a crude projection for when the
US could be fully vaccinated.

It creates 2 csv files and 2 new optional png files every day.

The data is sourced (by default) from the Our World in Data COVID-19 repository
under the
[Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/).
This code is licensed likewise.

I cannot predict the future, and neither can this program. These projections
were created as a way for me to be less bored while inside, and should not be
used in place of projections provided by experts. They should be used merely
for entertainment purposes or for learning about coding, not for anything where
the accuracy of projections is important. By using this code you acknowledge
that I am not responsible for any harm caused by its misuse.
"""

# change this line to True to have the program always overwrite without asking
defaultReplace = False
# change the filename for the vaccination data
fname = 'vaccinations.csv'
# the url to download the raw data from
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
# should the program keep a log of its projections?
shouldLogProjections = True
# filename for the log, should end in .csv
logfile = 'projections.csv'
# should output plots as png?
saveFigs = True

import wget
from os import remove, path
import csv
from scipy.stats import linregress as linreg
from scipy.integrate import simps
from datetime import date, timedelta
from matplotlib import pyplot as plt
from numpy import linspace

replace = False
filename = fname
if path.exists(fname) and not defaultReplace:
    c = ''
    while c.lower() != 'y' and c != 'n':
        print(f'Should the existing {fname} be replaced by updated data? (y/n)')
        c = input()
    replace = c.lower() == 'y'
elif not path.exists(fname):
    print(f'No existing data at {fname}, downloading... ', end='')
    filename = wget.download(url, out=fname)
    print('done!')

if replace:
    try:
        remove(fname)
        print('Removed existing file')
        print('Downloading new data... ', end='')
        filename = wget.download(url, out=fname)
        print('done!')
    except FileNotFoundError:
        if not defaultReplace:
            print(f"Unexpected FileNotFoundError. Will continue with execution assuming file {fname} doesn't exist")
    except:
        print('Unknown error')
        raise

dates = []
dailyVaccinations = []
peopleFullyVaccinated = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] == 'USA':
            if not row[7] == '':
                dailyVaccinations.append(int(row[7]))
                dates.append(date.fromisoformat(row[2]))
            if not row[5] == '':
                peopleFullyVaccinated.append(int(row[5]))

peopleFullyVaccinatedToday = max(peopleFullyVaccinated)
days = [(d - dates[0]).days for d in dates]

res = linreg(days, dailyVaccinations)
m, b, r2 = (res.slope, res.intercept, res.rvalue**2)
samples = 1000
projectTo = 240
x = linspace(min(days), projectTo, samples)
yhat = [m*xi + b for xi in x]
# divide by 2 because shots require 2 doses :( but then add everyone who's already vaccinated :)
projectedVaccinations = [(simps(yhat[:i], x[:i]) / 2) + peopleFullyVaccinatedToday for i in range(1, len(x))]
crossover = 0
for i, v in enumerate(projectedVaccinations):
    if v > 330e6:
        crossover = min(days) + (i/samples)*projectTo
        break
crossoverDate = dates[0] + timedelta(days=crossover)
plt.scatter(days, dailyVaccinations, label='True daily vaccinations')
plt.plot(x, yhat, color='r', label=f'y = {round(m,3)}x + {round(b,3)}')
plt.legend()
plt.title(date.today())
if saveFigs:
    plt.savefig('Projected daily vaccinations ' + str(date.today()))
plt.show()
plt.close()
plt.plot(x[1:], projectedVaccinations, label='Projected Vaccinations')
plt.plot(x[1:], [330e6 for _ in range(len(projectedVaccinations))], label='Total US Population (330 million)')
plt.legend()
plt.title(date.today())
if saveFigs:
    plt.savefig('Projected total vaccinations ' + str(date.today()))
plt.show()
plt.close()
if crossover == 0:
    print('This projects not all US citizens will be vaccinated within the timeframe')
else:
    print('This projects all US citizens may be vaccinated by', crossoverDate.strftime('%B %d, %Y'))

if shouldLogProjections:
    todayAlreadyExists = False
    if not path.exists(logfile):
        print(f'Log not found at {logfile}, creating it')
        with open(logfile, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Current Date', 'Projected Full Vaccination Date'])
    else:
        with open(logfile, 'r') as f:
            reader = csv.reader(f)
            if list(reader)[-1][0] == str(date.today()):
                todayAlreadyExists = True
                print('Data from today already exists, not adding to log')
    if not todayAlreadyExists:
        with open(logfile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(date.today()), str(crossoverDate)])
            print(f'Appending data from today to {logfile}')