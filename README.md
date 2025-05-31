# Kilter Board Grade Predictor
A project aimed at creating an ML model that can predict the grade of a kilter board climb.



# Dataset
## climbs.csv
A csv containing climbs for the KB1 board:
Columns: 
- Name: Name of the climb
- Setter: Username of the setter
- Angle: the original angle of the climb
- V Grade: boulder grade for the original climb
- Holds: an array of tuples ((x, y), [hold type])
  - The x, y are the distance from the bottom left corner (I believe it is inches)
  - The holds are not in a perfect grid, some are placed inbetween other holds.
## climbs\_clean.csv
Contains about 1000 climbs that have been climbed by many people.

- Name: Name of the climb
- Setter: Username of the setter
- Ascensionist Count: How many people have sent the climb on the app
- Angle: the original angle of the climb
- V Grade: boulder grade for the original climb
- Holds: an array of tuples ((x, y), [hold type])

## Download Kilter Board DB 
Contains the whole kilter database, including products, climbs, users...
~~~bash 
pip install boardlib
boardlib database kilter kilter.db
~~~





