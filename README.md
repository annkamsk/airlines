# airlines
Django app for flights control

## Assignment description

Our task is to develop a part of flight control system.
The airline company AirAnna uses airplanes. Each of them has its own id and a limit of passengers. 
Every flight is described with a starting and landing Airport, starting and landing time, used airplane and list of passengers.
Every passenger is identified by his/her first and last name. 
Every flight has a crew identified by a captain's name.

An application should:
* display list of flights - with filter and order options
* display details of the flight (including list of passengers) after selecting a flight
* allow to display crews with assigned flights for a selected date
* allow a logged-in user to sell flight tickets to new passengers and assign crews to the flights
* prepare a basic set of data for testing (at least 50 flights, 50 airplanes with at least 20 seats in each)
* handle errors - especially those created by user's action

Restrictions:
* One passenger can buy more than one ticket for each flight, but we cannot sell more tickets than there are seats available
* One airplane cannot make more than 4 flights a day
* After assigning a crew to a flight, it cannot be removed - only replaced by other crew
* Sites should be static 
* Data should be sent in JSON
* Prepare unit tests
* Prepare Selenium tests


