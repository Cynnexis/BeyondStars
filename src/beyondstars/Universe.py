# -*-coding:UTF-8 -*
import time
from threading import Thread, Lock

from beyondstars.Body import Body
from beyondstars.ThreadState import ThreadState
from beyondstars.Time import Time


class Universe(object):
	
	# CONSTRUCTOR #
	
	def __init__(self, bodies=None, name: str="Universe", start_now: bool=False):
		if bodies is None:
			bodies = []
		
		self._name = name
		self._lock = Lock()
		self._state = ThreadState.INITIALIZING
		self._last_update = Time.get_current_millis()
		self._simulation = Thread(name="Universe.run", target=Universe.run, args=(self,))
		self._bodies = bodies
		self._updates = {}
		self._history = {}
		
		self._simulation.start()
		
		if start_now:
			self.start()
	
	def __del__(self):
		if self._lock.locked():
			self._lock.release()
		self._state = ThreadState.STOPPED
	
	# UNIVERSE FUNCTION #
	
	def start(self) -> None:
		"""
		Start the simulation
		"""
		self.state = ThreadState.STARTED
	
	def pause(self) -> None:
		"""
		Pause the simulation
		"""
		self.state = ThreadState.PAUSED
		
	def resume(self) -> None:
		"""
		Resume the simulation after "pause". It has the same effect as start()
		"""
		self.state = ThreadState.STARTED
	
	def stop(self) -> None:
		"""
		Stop the simulation. Once stopped, the simulation can neither be resumed nor restarted.
		"""
		self.state = ThreadState.STOPPED
	
	def run(self) -> None:
		"""
		The simulation. DO NOT CALL IT FROM THE OUTSIDE OF A THREAD
		"""
		# Wait to the "START" flag
		while self._state == ThreadState.INITIALIZING:
			time.sleep(0.1)
		
		while self._state in [ThreadState.STARTED, ThreadState.PAUSED]:
			while self._state == ThreadState.PAUSED:
				time.sleep(0.1)
			
			if self._state == ThreadState.STARTED:
				self.update()
				time.sleep(0.01)
				#print(self.__repr__())
	
	def update(self) -> int:
		"""
		Update the bodies for the current time. Update the position, velocity and acceleration
		:return: The number of milliseconds to execute this function
		"""
		a = Time.get_current_millis()
		self._lock.acquire(blocking=True)
		self.filter_bodies(lock=False)
		
		for b in self._bodies:
			# Updating elapsed time
			last_update = self._updates.get(b, self._last_update)
			current_millis = Time.get_current_millis()
			time_elapsed = current_millis - last_update
			
			# Update position
			b.position.x += b.velocity.x * (time_elapsed / 1000)
			b.position.y += b.velocity.y * (time_elapsed / 1000)
			b.position.z += b.velocity.z * (time_elapsed / 1000)
			
			# Update velocity
			b.velocity.x += b.acceleration.x * (time_elapsed / 1000)
			b.velocity.y += b.acceleration.y * (time_elapsed / 1000)
			b.velocity.z += b.acceleration.z * (time_elapsed / 1000)
			
			# Update last update (which is now)
			self._updates[b] = Time.get_current_millis()
			
			# Add this version of b into its own history
			self._history[b].append(b)
		
		self._last_update = Time.get_current_millis()
		
		self._lock.release()
		b = Time.get_current_millis()
		
		return b - a
	
	def filter_bodies(self, lock: bool = False) -> None:
		"""
		Filter the BODIES attribute. All the none body objects are deleted.
		Configure UPDATES & HISTORY attributes as well.
		"""
		if lock:
			self._lock.acquire(blocking=True)
		
		# Delete all unwanted object from the list
		self._bodies = [b for b in self._bodies if isinstance(b, Body)]
		
		# Search for bodies that are not connected to an update in UPDATES
		for b in self._bodies:
			if self._updates.get(b, None) is None:
				self._updates[b] = self._last_update
		
		# Search for bodies that are not connected to an history
		for b in self._bodies:
			if self._history.get(b, None) is None:
				self._history[b] = [b]
		
		if lock:
			self._lock.release()
	
	def save_bodies_as_csv(self, filename: str):
		if not filename.endswith(".csv"):
			filename += ".csv"
		
		f = open(filename, "w")
		
		# Write header
		f.write("Body,Mass (Kg),Diameter (Km),x (m),y (m),z (m),vx (m/s),vy (m/s),vz (m/s),ax (m/s²),ay (m/s²),az (m/s²)\n")
		
		# Write data
		self._lock.acquire(blocking=True)
		for b in self._bodies:
			f.write("\"{}\",{},{},{},{},{},{},{},{},{},{},{}\n".format(b.name, b.mass, b.diameter,
			                                                           b.position.x,
			                                                           b.position.y,
			                                                           b.position.z,
			                                                           
			                                                           b.velocity.x,
			                                                           b.velocity.y,
			                                                           b.velocity.z,
			                                                           
			                                                           b.acceleration.x,
			                                                           b.acceleration.y,
			                                                           b.acceleration.z))
		
		self._lock.release()
		f.close()
	
	# GETTER & SETTER #
	
	def get_name(self) -> str:
		"""
		Getter of NAME
		:return: The name of this universe
		"""
		return self._name
	
	def set_name(self, name: str) -> None:
		"""
		Setter for NAME
		:param name: The name if this universe
		"""
		if name is None or name == "":
			self._name = "Universe"
		else:
			self._name = name
	
	name = property(get_name, set_name)
	
	def get_state(self) -> ThreadState:
		"""
		Getter of STATE
		:return: Return the current state of the simulation
		"""
		self._lock.acquire(blocking=True)
		value = self._state
		self._lock.release()
		return value
	
	def set_state(self, state: ThreadState) -> None:
		"""
		Setter of STATE. Update the simulation
		:param state: The new state
		"""
		self._lock.acquire(blocking=True)
		
		# Check if the transition is possible
		error = AssertionError("Cannot change state.")
		if self._state == ThreadState.INITIALIZING:
			if state == ThreadState.PAUSED:
				raise error
		elif self._state == ThreadState.STARTED:
			if state == ThreadState.INITIALIZING:
				raise error
		elif self._state == ThreadState.PAUSED:
			if state == ThreadState.INITIALIZING:
				raise error
		elif self._state == ThreadState.STOPPED:
			if state in [ThreadState.INITIALIZING, ThreadState.STARTED, ThreadState.PAUSED]:
				raise error
			
		# Change the state
		self._state = state
		
		self._lock.release()
	
	state = property(get_state, set_state)
	
	def get_bodies(self) -> list:
		self._lock.acquire(blocking=True)
		value = self._bodies
		self._lock.release()
		return value
	
	def set_bodies(self, bodies: list) -> None:
		self._lock.acquire(blocking=True)
		self._bodies = bodies
		self._lock.release()
	
	def add_bodies(self, *args) -> None:
		self._lock.acquire(blocking=True)
		for a in args:
			if isinstance(a, Body):
				self._bodies.append(a)
		self._lock.release()
	
	bodies = property(get_bodies, set_bodies)
	
	def get_updates(self) -> dict:
		"""
		Getter for UPDATES
		:return: Get the last update time of the given body
		"""
		self._lock.acquire(blocking=True)
		value = self._updates
		self._lock.release()
		return value
	
	def set_updates(self, updates: dict) -> None:
		"""
		Setter for UPDATES
		:param updates: The last update of the given body
		"""
		self._lock.acquire(blocking=True)
		self._updates = updates
		self._lock.release()
	
	updates = property(get_updates, set_updates)
	
	def get_history(self) -> dict:
		"""
		Getter for HISTORY
		:return: The list of all previous body before update(), for the given body
		"""
		return self._history
	
	def set_history(self, history: dict) -> None:
		"""
		Setter for HISTORY
		:param history: The list of all previous body before update(), for the given body
		"""
		self._history = history
	
	history = property(get_history, set_history)
	
	# SPECIAL FUNCTIONS #
	
	def __getitem__(self, item):
		return self.bodies[item]
	
	def __setitem__(self, key, value):
		self.bodies[key] = value
	
	def __delitem__(self, key):
		del self.bodies[key]
		
	def __str__(self):
		return self.__repr__()
	
	def __repr__(self):
		content: str = " --- {} --- \n".format(self.name)
		self._lock.acquire(blocking=True)
		for b in self._bodies:
			content += "\t{}\n".format(b.__repr__())
		self._lock.release()
		return content
