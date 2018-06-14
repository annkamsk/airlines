from datetime import datetime, timedelta
from telnetlib import EC

from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.test import TestCase, Client, LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from urllib3.util import timeout

from flights.models import Crew, Flight, Airplane, Airport


class CrewTestCase(TestCase):
    def setUp(self):
        c1 = Crew.objects.create(captain_name="Anna", captain_surname="Kramarska")
        c2 = Crew.objects.create(captain_name="Bartosz", captain_surname="Wojno")
        c3 = Crew.objects.create(captain_name="Ola", captain_surname="Grzyb")

        a1 = Airport.objects.create(name="Warsaw")
        a2 = Airport.objects.create(name="Modlin")

        air1 = Airplane.objects.create(licenseChars="ak385833", capacity=100)
        air2 = Airplane.objects.create(licenseChars="bw386385", capacity=50)

        Flight.objects.create(startingAirport=a1, landingAirport=a2, startingTime=datetime.now(),
                              landingTime=datetime.now() + timedelta(hours=12), airplane=air1, crew=c1)

        Flight.objects.create(startingAirport=a2, landingAirport=a1, startingTime=datetime.now(),
                              landingTime=datetime.now() + timedelta(hours=6), airplane=air2, crew=c2)

    def test_successful_crew_assign(self):
        c = Client()
        crew_id = Crew.objects.get(captain_surname="Grzyb").id
        flight_id = Flight.objects.get(crew=Crew.objects.get(captain_surname="Kramarska")).id
        response = c.post('/assign-crew/', {'flight': flight_id, 'crew': crew_id})
        self.assertEqual(response.json()['result'], 'successful')

    def test_unsuccessful_crew_assign(self):
        c = Client()
        crew_id = Crew.objects.get(captain_surname="Wojno").id
        flight_id = Flight.objects.get(crew=Crew.objects.get(captain_surname="Kramarska")).id
        response = c.post('/assign-crew/', {'flight': flight_id, 'crew': crew_id})
        self.assertEqual(response.json()['result'], 'busy')

    def test_get_crews(self):
        c = Client()
        response = c.get('/crews/')
        self.assertEqual(response.json()[0]['captain_surname'], "Kramarska")


class SeleniumTestCase(StaticLiveServerTestCase):

    def create_flights(self):
        c1 = Crew.objects.create(captain_name="Anna", captain_surname="Kramarska")
        c2 = Crew.objects.create(captain_name="Bartosz", captain_surname="Wojno")
        c3 = Crew.objects.create(captain_name="Ola", captain_surname="Grzyb")

        a1 = Airport.objects.create(name="Warsaw")
        a2 = Airport.objects.create(name="Modlin")

        air1 = Airplane.objects.create(licenseChars="ak385833", capacity=100)
        air2 = Airplane.objects.create(licenseChars="bw386385", capacity=50)

        Flight.objects.create(startingAirport=a1, landingAirport=a2, startingTime=datetime.now(),
                              landingTime=datetime.now() + timedelta(hours=12), airplane=air1, crew=c1)

        Flight.objects.create(startingAirport=a2, landingAirport=a1, startingTime=datetime.now(),
                              landingTime=datetime.now() + timedelta(hours=6), airplane=air2, crew=c2)

    def create_users(self):
        get_user_model().objects.create_user('temp', 'temp@temp.com', 'temporary')
        get_user_model().objects.create_user('temp2', 'temp2@temp.com', 'temporary')

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.create_users()
        self.create_flights()

    def tearDown(self):
        self.selenium.quit()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/auth/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('temp')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('temporary')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.selenium.find_element_by_class_name("data")

    def test_add_passenger(self):
        self.test_login()
        self.selenium.get('%s%s' % (self.live_server_url, '/flight/1/'))
        name_input = self.selenium.find_element_by_id('id_name')
        name_input.send_keys("Anna")
        surname_input = self.selenium.find_element_by_id('id_surname')
        surname_input.send_keys("Kramarska")
        tickets_input = self.selenium.find_element_by_name('nrOfTickets')
        tickets_input.send_keys(10)
        self.selenium.find_element_by_id('buy').click()

    def test_assign_crew(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_id('crews-link').click()

        # login
        user_input = self.selenium.find_element_by_id('user')
        user_input.send_keys('temp')
        pass_input = self.selenium.find_element_by_id('password')
        pass_input.send_keys('temporary')
        self.selenium.find_element_by_id('log').click()
        self.selenium.find_element_by_xpath('//button[text()="Logout"]')

        # assigning crew
        flight = self.selenium.find_element_by_id('flight')
        flight.send_keys(1)
        crew = self.selenium.find_element_by_id('crew')
        crew.send_keys('1')
        self.selenium.find_element_by_id('assign').click()
