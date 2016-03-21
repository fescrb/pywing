# Imports
from __future__ import print_function

import numpy
from numpy.random import randint
from enum import Enum

__all__ = ["common", "plot"]

class result(Enum):
	CRIT  = 16
	HIT   = 8
	EVADE = 4
	FOCUS = 2
	BLANK = 1
	
def result_str(res):
	str = ""
	if res & result.BLANK:
		str += "BLANK"
	if res & result.FOCUS:
		if len(str):
			str += "|"
		str += "FOCUS"
	if res & result.HIT:
		if len(str):
			str += "|"
		str += "HIT"
	if res & result.CRIT:
		if len(str):
			str += "|"
		str += "CRIT"
	if res & result.EVADE:
		if len(str):
			str += "|"
		str += "EVADE"
	return str

# DICE CLASSES DEFINITIONS

__attack_die_faces__ = [result.CRIT, result.HIT, result.HIT, result.HIT, result.FOCUS, result.FOCUS, result.BLANK, result.BLANK]
__evade_die_faces__ = [result.EVADE, result.EVADE, result.EVADE, result.FOCUS, result.FOCUS, result.BLANK, result.BLANK, result.BLANK]
	

class die:
	def __init__ (self):
		self.rerolled = False
	def __str__(self):
		return result_str(self.result)
	@staticmethod
	def __roll_die__(face_list):
		return face_list[randint(0, 8)]
	def equals(self, result):
		return self.result & result
	def change(self, to):
		self.result = to

class attack_die(die):
	def __init__(self):
		die.__init__(self)
		self.__roll__()
	def __roll__(self):
		self.result = self.__roll_die__(__attack_die_faces__)
	def reroll(self):
		if not self.rerolled:
			self.__roll__()
			self.rerolled = True
			return True
		return False

class evade_die(die):
	def __init__(self):
		die.__init__(self)
		self.__roll__()
	def __roll__(self):
		self.result = die.__roll_die__(__evade_die_faces__)
	def reroll(self):
		if not self.rerolled:
			self.__roll__()
			self.rerolled = True
			return True
		return False

# DICE LIST METHOD DEFINITIONS

def count_relevant_results(dice_list, relevant_results):
	count = 0
	for i in range(len(dice_list)):
		if dice_list[i].result & relevant_results:
			count += 1
	return count

def roll_attack_dice(number):
	dice_results = []
	for i in range(number):
		dice_results.append(attack_die())
	return dice_results

def roll_evade_dice(number):
	dice_results = []
	for i in range(number):
		dice_results.append(evade_die())
	return dice_results

# DICE LIST MODIFICATION DEFINITITONS

class perform(Enum):
	FOR_ALL = 7
	ONCE = 1

class change:
	def __init__(self, rule, from_result, to_result):
		self.rule = rule
		self.from_result = from_result
		self.to_result = to_result
	def modify_dice_list(self, dice_list):
		for i in range(len(dice_list)):
			if dice_list[i].equals(self.from_result):
				dice_list[i].change(self.to_result)
				if self.rule == perform.ONCE:
					return dice_list
		return dice_list

class reroll:
	def __init__(self, rule, from_result):
		self.rule = rule
		self.from_result = from_result
	def modify_dice_list(self, dice_list):
		for i in range(len(dice_list)):
			if dice_list[i].equals(self.from_result):
				if dice_list[i].reroll() and self.rule == perform.ONCE:
					return dice_list
		return dice_list
	
# Debug
def __print_dice_list(dice_list):
	for i in range(len(dice_list)):
		print(dice_list[i], end=" ")
	print("")
	
def get_dice_chances(number_of_dice, dice_roll_function, relevant_results, enemy_modifications, friendly_modifications):
	relevant_counts = numpy.zeros((8)) 
	num_iterations = 200000
	for i in range(num_iterations):
		dice_list = dice_roll_function(number_of_dice)
		# Perform modifications
		for j in range(len(enemy_modifications)):
			dice_list = enemy_modifications[j].modify_dice_list(dice_list)
		for j in range(len(friendly_modifications)):
			dice_list = friendly_modifications[j].modify_dice_list(dice_list)
		relevant_count_for_this_roll = count_relevant_results(dice_list, relevant_results)
		relevant_counts[relevant_count_for_this_roll] += 1	
	chances = numpy.zeros((8))
	for i in range(len(chances)):
		chances[i] = float(relevant_counts[i]) / float(num_iterations)
	return chances

def get_hit_chances(number_of_dice, enemy_modifications=[], friendly_modifications=[]):
	return get_dice_chances(number_of_dice, roll_attack_dice, result.HIT | result.CRIT, enemy_modifications, friendly_modifications)

def get_evade_chances(number_of_dice, enemy_modifications=[], friendly_modifications=[]):
	return get_dice_chances(number_of_dice, roll_evade_dice, result.EVADE, enemy_modifications, friendly_modifications)

def get_crit_chances(number_of_dice, enemy_modifications=[], friendly_modifications=[]):
	return get_dice_chances(number_of_dice, roll_attack_dice, result.CRIT, eenemy_modifications, friendly_modifications)

def hits_vs_evade(hit_chances, evade_chances):
	chances = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	for i in range(1, len(hit_chances)):
		for j in range(i):
			chances[i - j] = chances[i - j] + (hit_chances[i] * evade_chances[j])
	total = 0.0
	for i in range(1, len(chances)):
		total = total + chances[i]
	chances[0] = 1.0 - total
	return chances
	
def average_chance(chance_list):
	avg = 0.0
	for i in range(1, len(chance_list)):
		avg = avg + (i * chance_list[i])
	return avg