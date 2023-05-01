from utils.treeParser import Employee, Team, Area, Function, Tribe, Competence
from typing import List
from flask import url_for

def employeeHTML(e: Employee, l:List[Competence]):
	yellowFilter = 'filter: invert(81%) sepia(53%) saturate(661%) hue-rotate(344deg) brightness(97%) contrast(94%)'
	orangeFilter = 'filter: invert(74%) sepia(42%) saturate(3131%) hue-rotate(337deg) brightness(98%) contrast(84%);'

	colorDict = {
		"#f1c232": yellowFilter,
		"#e69138": orangeFilter
	}

	c = Competence('Competence not found', 'An error occurred', '#F00')

	for com in l:
		if com.name == e.competence_lead and com.competence == e.competence:
			c = com
	
	color = colorDict.get(c.color, '')
	return f""" <div class='employee'>
 					<img width=30 height=30 src="{url_for('static',filename = 'user.svg')}" style='{color}'>
	  				</img>
	   				<p>
						{e.name}
	  				</p>
	  			</div>"""

def teamEmployees(t: Team, tr: Tribe):
	return "".join(employeeHTML(e, tr.competences) for e in t.employees)

def teamHTML(t: Team, tr: Tribe):
	return f""" <div class='team'>
 					<h5>
	  					{t.name}
					</h5>
	 				<p>
	  					{t.lead}
					</p>
	 				<div class='employeesWrapper'>
	  					{teamEmployees(t, tr)}
	  				</div>
	 			</div>"""

def areaTeams(a: Area, tr: Tribe):
	return "".join(teamHTML(t, tr) for t in a.teams)

def areaHTML(a: Area, tr: Tribe):
	return f""" <div class='area'>
 					<h5>
	  					{a.name}
					</h5>
	 				<p>
	  					{a.lead}
					</p>
	 				<div class='teamsWrapper'>
	  					{areaTeams(a, tr)}
	  				</div>
	 			</div>"""

def functionAreas(f: Function, tr: Tribe):
	return "".join(areaHTML(a, tr) for a in f.areas)

def functionHTML(f: Function, tr: Tribe):
	return f""" <div class='function'>
 					<h5>
	  					{f.name}
					</h5>
	 				<p>
	  					{f.lead}
					</p>
	 				<div class='areasWrapper'>
	  					{functionAreas(f, tr)}
	  				</div>
	 			</div>"""

def tribeFunctions(t: Tribe):
	return "".join(functionHTML(f, t) for f in t.functions)

def competenceHTML(c: Competence):
	return f"<div style='color:{c.color}'><h5>{c.name}</h5><p>{c.competence}</p></div>"

def tribeCompetences(t: Tribe):
	return "".join(competenceHTML(c) for c in t.competences)

def tribeHTML(t: Tribe):
	return f""" <div class='allWrapper' id={t.name}>
	 				<div class='tribe' style='max-width: {450*len(t.functions)}px'>
						<h5>
							{t.name}
						</h5>
						<p>
							{t.lead}
						</p>
						<div class='functionsWrapper'>
							{tribeFunctions(t)}
						</div>
					</div>
	 				<div>
		 				{tribeCompetences(t)}
	   				</div>
	 			</div>"""
	
def renderTribes(l:List[Tribe]):
	return "".join(tribeHTML(t) for t in l)

def choiceHTML(l:List[Tribe]):
	onchange =  "\"let selected = document.querySelector('select').value;document.querySelectorAll('.allWrapper').forEach((it) => {it.id === selected ? it.style.display = 'flex' : it.style.display = 'none';});\""

	return  f'<select onchange={onchange}>' + ''.join(f'<option id={t.name}>{t.name}</option>' for t in l) + '</select>'