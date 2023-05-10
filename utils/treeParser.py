# this is likely not very optimized but it does the job
import random
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

def is_readable_color(hex_color1, hex_color2):
	"""
	Checks if two hex colors are readable on top of each other.
	"""
	# Convert the hex colors to RGB format
	r1, g1, b1 = tuple(int(hex_color1[i:i+2], 16) for i in (1, 3, 5))
	r2, g2, b2 = tuple(int(hex_color2[i:i+2], 16) for i in (1, 3, 5))
	
	# Calculate the relative luminance of each color
	def relative_luminance(r, g, b):
		r_srgb = r / 255.0
		g_srgb = g / 255.0
		b_srgb = b / 255.0
		
		def srgb_to_linear(c):
			if c <= 0.03928:
				return c / 12.92
			else:
				return ((c + 0.055) / 1.055) ** 2.4
		
		r_linear = srgb_to_linear(r_srgb)
		g_linear = srgb_to_linear(g_srgb)
		b_linear = srgb_to_linear(b_srgb)
		
		return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
	
	lum1 = relative_luminance(r1, g1, b1)
	lum2 = relative_luminance(r2, g2, b2)
	
	# Calculate the contrast ratio between the two colors
	ratio = (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)
	
	# Calculate the threshold value based on the contrast ratio
	threshold = 4.5 if ratio >= 7 else 3 if ratio >= 4.5 else 2
	
	# Calculate the difference between each color component
	delta_r = abs(r1 - r2)
	delta_g = abs(g1 - g2)
	delta_b = abs(b1 - b2)
	
	# Calculate the average color difference
	avg_delta = (delta_r + delta_g + delta_b) / 3
	
	# Check if the colors are readable on top of each other
	return avg_delta <= threshold


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
	def __init__(self, name, competence, color=None):
		self.name = name
		self.competence = competence
		self.color = "#" + ''.join([random.choice('346789ABCDEF') for j in range(6)]) # Remove 012 to avoid dark colors

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
			self.competences.append(Competence(elem[0], elem[1]))

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