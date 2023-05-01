# this is likely not very optimized but it does the job

import csv

class Employee:
	def __init__(self, name:str, competence:str, team:str, area:str, function:str, tribe:str, competence_lead:str, team_lead:str, area_lead:str, function_lead:str, tribe_lead:str):
		self.name = name
		self.competence = competence
		self.team = team
		self.area = area
		self.function = function
		self.tribe = tribe
		self.competence_lead = competence_lead
		self.team_lead = team_lead
		self.area_lead = area_lead
		self.function_lead = function_lead
		self.tribe_lead = tribe_lead

	def __repr__(self):
		return self.name

def employeeFromDict(li: list[dict]) -> list[Employee]:
	return [
		Employee(
			l['Team Member'],
			l['Competence'],
			l['Team'],
			l['Area'],
			l['Function'],
			l['Tribe'],
			l['Competence Lead'],
			l['Team Lead'],
			l['Area Lead'],
			l['Function Lead'],
			l['Tribe Lead']
		) for l in li
	]

class Team:
	def __init__(self, name:str, lead:str, employees:list[Employee]):
		self.name = name
		self.lead = lead
		self.employees = employees

	def __repr__(self):
		return self.name

class Area:
	def __init__(self, name:str, lead:str, employees:list[Employee]):
		self.name = name
		self.lead = lead
		self.employees = employees
		self.teams = []
		teamNames: {str:list[Employee]} = {}

		for e in self.employees:
			if teamNames.get(e.team, ''):
				teamNames[e.team].append(e)
			else:
				teamNames[e.team] = [e]
				
		for elems in teamNames.values():
			self.teams.append(Team(elems[0].team, elems[0].team_lead, elems))

	def __repr__(self):
		return self.name

class Function:
	def __init__(self, name:str, lead:str, employees:list[Employee]):
		self.name = name
		self.lead = lead
		self.employees = employees
		self.areas = []
		areaNames = {}

		for e in self.employees:
			if areaNames.get(e.area, ''):
				areaNames[e.area].append(e)
			else:
				areaNames[e.area] = [e]
				
		for elems in areaNames.values():
			self.areas.append(Area(elems[0].area, elems[0].area_lead, elems))

	def __repr__(self):
		return self.name

class Competence:
	def __init__(self, name, competence, color):
		self.name = name
		self.competence = competence
		self.color = color

def generateColor(i):
	return ["#f1c232", "#e69138"][i]

class Tribe:
	def __init__(self, name:str, lead:str, employees:list[Employee]):
		self.name = name
		self.lead = lead
		self.employees = employees
		self.competence_leads = []
		self.functions = []
		functionsNames = {}

		for e in self.employees:
			if functionsNames.get(e.function, ''):
				functionsNames[e.function].append(e)
			else:
				functionsNames[e.function] = [e]
			if [e.competence_lead, e.competence] not in self.competence_leads:
				self.competence_leads.append([e.competence_lead, e.competence])
				
		for elems in functionsNames.values():
			self.functions.append(Function(elems[0].function, elems[0].function_lead, elems))

		self.competences = []
		
		for i, elem in enumerate(self.competence_leads):
			self.competences.append(Competence(elem[0], elem[1], generateColor(i)))

	def __repr__(self):
		return self.name

class TreeParser:
	"""
 	Tribe -> Function -> Area -> Team	
  	"""
	def __init__(self, fileName):
		self.fileName = fileName
		self.competence_leads = []
		
		with open(self.fileName, mode='r') as csv_file:
			reader = csv.DictReader(csv_file)
			self.employees = employeeFromDict(list(reader))

		self.tribesNames = {}

		for e in self.employees:
			if self.tribesNames.get(e.tribe, ''):
				self.tribesNames[e.tribe].append(e)
			else:
				self.tribesNames[e.tribe] = [e]

		self.tribes = []
				
		for elems in self.tribesNames.values():
			self.tribes.append(Tribe(elems[0].tribe, elems[0].tribe_lead, elems))