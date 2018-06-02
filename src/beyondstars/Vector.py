# -*-coding:UTF-8 -*
from math import sqrt


class Vector(object):
	
	def __init__(self, x: float = 0, y: float = 0, z: float = 0):
		self._x = x
		self._y = y
		self._z = z
	
	# VECTOR FUNCTIONS #
	
	def length(self) -> float:
		return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))
	
	def distance_with(self, other) -> float:
		if isinstance(other, Vector):
			return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2) + pow(self.z - other.z, 2))
	
	def dot_product(self, other) -> float:
		if isinstance(other, Vector):
			result = 0
			result += self.x * other.x
			result += self.y * other.y
			result += self.z * other.z
			return result
	
	def cross_product(self, other):
		if isinstance(other, Vector):
			v = Vector()
			v.x = self.y * other.z - self.z * other.y
			v.y = self.z * other.x - self.x * other.z
			v.z = self.x * other.y - self.y * other.x
			return v
	
	# GETTERS & SETTERS #
	
	def get_x(self) -> float:
		return self._x
	
	def set_x(self, x: float):
		self._x = x
	
	x = property(get_x, set_x)
	
	def get_y(self) -> float:
		return self._y
	
	def set_y(self, y: float):
		self._y = y
	
	y = property(get_y, set_y)
	
	def get_z(self) -> float:
		return self._z
	
	def set_z(self, z: float):
		self._z = z
	
	z = property(get_z, set_z)
	
	# SPECIAL METHODS #
	
	def __add__(self, other):
		if isinstance(other, Vector):
			v = Vector()
			v.x = self.x + other.x
			v.y = self.y + other.y
			v.z = self.z + other.z
			return v
		if isinstance(other, int) or isinstance(other, float):
			v = Vector()
			v.x = self.x + other
			v.y = self.y + other
			v.z = self.z + other
			return v
	
	def __sub__(self, other):
		if isinstance(other, Vector):
			v = Vector()
			v.x = self.x - other.x
			v.y = self.y - other.y
			v.z = self.z - other.z
			return v
		if isinstance(other, int) or isinstance(other, float):
			v = Vector()
			v.x = self.x - other
			v.y = self.y - other
			v.z = self.z - other
			return v
	
	def __getitem__(self, item) -> float:
		if item == 0:
			return self.x
		elif item == 1:
			return self.y
		elif item == 2:
			return self.z
		else:
			raise IndexError
	
	def __setitem__(self, key, value):
		if key == 0:
			self.x = value
		elif key == 1:
			self.y = value
		elif key == 2:
			self.z = value
		else:
			raise IndexError
	
	def __delitem__(self, key):
		raise AttributeError("Cannot delete attribute in Vector")
	
	def __len__(self) -> int:
		return 3
	
	def __delattr__(self, item):
		raise AttributeError("Cannot delete attribute in Vector")
	
	def __eq__(self, other) -> bool:
		if isinstance(other, Vector):
			return self.x == other.x and self.y == other.y and self.z == other.z
		else:
			return False
	
	def __str__(self) -> str:
		return self.__repr__()
	
	def __repr__(self) -> str:
		return "({} ; {} ; {})".format(self.x, self.y, self.z)
