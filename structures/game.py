from abc import ABCMeta, abstractmethod
from json import loads, dumps

__all__ = ['ParseException', 'Storeable', 'Point', 'Unit', 'Player', 'Action']

class ParseException(Exception):
	def __init__(self, message):
		self.message = message
	def __repr__(self):
		return 'Parse Error: ' + message

class Storeable(metaclass=ABCMeta):
	@abstractmethod
	def store(self) -> str:
		"Stores self to string"
		return

	@staticmethod
	@abstractmethod
	def restore(self, src: str):
		"Restores self from string"

#jObj - parsed json object

class Point(Storeable):
	def __init__(self, *args, jObj=None, x=0, y=0):
		assert len(args) == 0, ' only named arguments'
		if jObj == None:
			self.x, self.y = x, y
		else:
			if 'x' not in jObj or 'y' not in jObj:
				raise ParseException('failed to parse point from ' + repr(jObj))
			self.x = jObj['x']
			self.y = jObj['y']
		assert type(self.x) == int and type(self.y) == int, 'incorrect types'
	
	def store(self):
		return '{"x":%d, "y":%d}' % (self.x, self.y)
	
	@staticmethod
	def restore(src):
		return Point(jObj=loads(src))

class Unit(Storeable):
	def __init__(self, *args, jObj=None, id='Invalid id', position=Point(x=0, y=0), health=0):
		assert len(args) == 0, ' only named arguments'
		if jObj == None:
			self.position, self.id, self.health = position, id, health
		else:
			if 'id' not in jObj or 'position' not in jObj or 'health' not in jObj:
				raise ParseException('failed to parse unit from ' + repr(jObj))
			self.position, self.id, self.health = Point(jObj=jObj['position']), jObj['id'], jObj['health']
		assert type(self.id) == str and type(self.health) == int and type(self.position) == Point, 'incorrect types'
	
	def store(self):
		return '{"id":%s, "position":%s, "health":%d}' % (self.id, self.position.store(), self.health)
	
	@staticmethod
	def restore(src):
		return Unit(jObj=loads(src))

class Player:
	def __init__(self, name, base, units):
		self.name, self.base, self.units = name, base, units
   
class Response(Storeable):
	def __init__(self, *args, jObj=None, result=True, cause=''):
		assert len(args) == 0, ' only named arguments'
		if jObj == None:
			self.result, self.cause = result, cause
		else:
			if 'result' not in jObj or 'cause' not in jObj:
				raise ParseException('failed to parse response from ' + repr(jObj))
			self.result, self.cause = jObj['result'], jObj['cause']
		assert type(self.result) == bool and type(self.cause) == str, 'incorrect types'
	
	def store(self):
		return '{"result":%s, "cause":%s}' % (str(self.result).lower(), self.cause)
	
	@staticmethod
	def restore(src):
		return Point(jObj=loads(src))

class Action(Storeable):
	def __init__(self, *args, jObj=None, id='Invalid action', position=Point(x=0, y=0)):
		assert len(args) == 0, ' only named arguments'
		if jObj == None:
			self.id, self.position = id, position
		else:
			if 'id' not in jObj or 'position' not in jObj:
				raise ParseException('failed to parse action from ' + repr(jObj))
			self.id, self.position = jObj['id'], Point(jObj=jObj['position'])
		assert type(self.id) == str and type(self.position) == Point, 'incorrect types'
	
	def store(self):
		return '{"id":%s, "position":%s}' % (self.id, self.position.store())
	
	@staticmethod
	def restore(src):
		return Point(jObj=loads(src))
	
