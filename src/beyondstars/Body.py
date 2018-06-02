# -*-coding:UTF-8 -*
from beyondstars import Constants
from beyondstars.Vector import Vector


class Body(object):
	
	# CONSTRUCTOR #
	
	def __init__(self, mass: float, diameter: float, position: Vector, velocity: Vector = Vector(), acceleration: Vector = Vector(), name: str = "Body"):
		self._name = name
		self._mass = mass  # kg
		self._diameter = diameter  # km
		self._position = position  # m
		self._velocity = velocity  # m/s
		self._acceleration = acceleration  # m/s²
	
	# BODY FUNCTIONS #
	
	def distance_with(self, other) -> float:
		if isinstance(other, Body):
			return self.position.distance_with(other.position)
	
	def gravitational_force(self, other) -> float:
		if isinstance(other, Body):
			return Constants.GRAVITATIONAL_CONSTANT * (self.mass * other.mass) / pow(self.distance_with(other), 2)
	
	# GETTERS & SETTERS #
	
	def get_name(self) -> str:
		"""
		Getter of NAME
		:return: The name of this body
		"""
		return self._name
	
	def set_name(self, name: str) -> None:
		"""
		Setter for NAME
		:param name: The name if this body
		"""
		if name is None or name == "":
			self._name = "Body"
		else:
			self._name = name
	
	name = property(get_name, set_name)
	
	def get_mass(self) -> float:
		return self._mass
	
	def set_mass(self, mass: float):
		self._mass = mass
	
	mass = property(get_mass, set_mass)
	
	def get_diameter(self) -> float:
		return self._diameter
	
	def set_diameter(self, diameter: float):
		self._diameter = diameter
	
	diameter = property(get_diameter, set_diameter)
	
	def get_position(self) -> Vector:
		return self._position
	
	def set_position(self, position: Vector):
		self._position = position
		
	position = property(get_position, set_position)
	
	def get_velocity(self) -> Vector:
		return self._velocity
	
	def set_velocity(self, velocity: Vector):
		self._velocity = velocity
		
	velocity = property(get_velocity, set_velocity)
	
	def get_acceleration(self) -> Vector:
		return self._acceleration
	
	def set_acceleration(self, acceleration: Vector):
		self._acceleration = acceleration
		
	acceleration = property(get_acceleration, set_acceleration)
	
	# SPECIAL FUNCTIONS #
	
	def __str__(self):
		return self.__repr__()
	
	def __repr__(self):
		return "{} [mass: {}kg, diameter: {}km, position: {}m, velocity: {}m/s, acceleration: {}m/s²]".format(self.name, self.mass, self.diameter, self.position.__repr__(), self.velocity.__repr__(), self.acceleration.__repr__())
