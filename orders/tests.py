from django.test import TestCase, Client

# Create your tests here.
from .models import ProductSize
import os
import pathlib
import unittest

from selenium import webdriver

class ModelsTestCase(TestCase):
	def setUp(self):
		ps1 = ProductSize.objects.create(name="big")
		ps2 = ProductSize.objects.create(name="large")

	def testSizeCount(self):
		ps = ProductSize.objects.all()
		self.assertEqual(ps.count(), 2)


class PizzaTestCase(TestCase):

	def testIndex(self):
		c = Client()
		response = c.get("/")
		self.assertEqual(response.status_code, 200)


def fileUri(filename):
	return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()

class WebPageTests(unittest.TestCase):
	def testTitle(self):
		driver.get(fileUri("./templates/orders/index.html"))
		self.assertEqual(driver.title, "Home")
