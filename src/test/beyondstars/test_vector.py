# -*-coding:UTF-8 -*

from unittest import TestCase

from beyondstars.Vector import Vector


class TestVector(TestCase):
	
	a = Vector(1, 2, 3)
	b = Vector(4, -5, 6)
	
	def test_dot_product(self):
		self.assertEqual(12, TestVector.a.dot_product(TestVector.b))
	
	def test_cross_product(self):
		self.assertEqual(Vector(27, 6, -13), TestVector.a.cross_product(TestVector.b))
