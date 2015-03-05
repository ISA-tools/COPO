from django.test import TestCase
#from django.test import Client
import unittest
#from selenium import webdriver

# Create your tests here.

class EnaTest(unittest.TestCase):
    def setUp(self):
        pass


    def test_experiment(self):
        #driver = webdriver.Firefox()
        #driver.get("/copo")
        self.assertEqual(200, 200)

