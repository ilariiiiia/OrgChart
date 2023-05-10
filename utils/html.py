from utils.treeParser import Employee, Team, Area, Function, Tribe, Competence
from typing import List

def safeName(name: str):
	return name.replace(' ', '_')

def employeeHTML(e: Employee, l:List[Competence]):
	c = Competence('Competence not found', 'An error occurred', '#FF0000')

	for com in l:
		if com.name == e.competence_lead and com.competence == e.competence:
			c = com
			
	return f""" <div class="employee tooltip"
					attname={safeName(e.name)}
					teamsSelect={safeName(e.team)}
					competenceSelect={safeName(e.competence)}
					areasSelect={safeName(e.area)}
					functionsSelect={safeName(e.function)}
					tribeSelect={safeName(e.tribe)}
					competenceLead={safeName(e.competence_lead)}
					teamsLead={safeName(e.team_lead)}
					areasLead={safeName(e.area_lead)}
					functionsLead={safeName(e.function_lead)}
					tribeLead={safeName(e.tribe_lead)}>
 					<svg viewBox="0 0 500 500" width=30 height=30 style="fill:{c.color}">
						<path d="M256,224c53,0,96-43,96-96s-43-96-96-96s-96,43-96,96S203,224,256,224z M256,256c-70.7,0-128-57.3-128-128S185.3,0,256,0
							s128,57.3,128,128S326.7,256,256,256z"/>
						<path d="M96,512H64v-79.4c0-79.5,64.5-144,144-144c0.2,0,32.5,0.2,96.7,0.5c79.3,0.4,143.3,64.7,143.3,144V512h-32v-78.9
							c0-61.6-49.8-111.7-111.5-112l-96-0.5c-62.4,0-112.5,50.1-112.5,112V512z"/>
					</svg>
	   				<p>
						{e.name}
	  				</p>
	   				<span class="tooltiptext"><span class='employeeCompetence'>{e.competence}</span><br/>Lead: <span class='employeeCompetenceLead'>{e.competence_lead}</span></span>
	  			</div>"""

def teamEmployees(t: Team, tr: Tribe):
	return "".join(employeeHTML(e, tr.competences) for e in t.employees)

def teamHTML(t: Team, tr: Tribe):
	return f""" <div class='team' id={safeName(t.name)}>
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
	return f""" <div class='area' id={safeName(a.name)}>
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
	return f""" <div id={safeName(f.name)} class='function'>
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
	return f""" <div class='allWrapper' id={safeName(t.name)}>
	 				<div class='tribe'>
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
	 			</div>"""
	
def renderTribes(l:List[Tribe]):
	return "".join(tribeHTML(t) for t in l)

def choiceHTML(l:List[Tribe]):
	onChangeFun = f"""
<script type='text/javascript'>
{open('./static/onChangeFunctions.js').read()}
</script>
"""
	return onChangeFun + '<div class="selectorsWrapper">' + broaderSelect(l) + leadsHTML(l) + memberHTML(l) +  resetHTML() + '</div>'

def broaderSelect(l:list[Tribe]):
	return tribeSelectHTML(l) + funcSelectHTML(l) + areaSelectHTML(l) + teamSelectHTML(l) + compSelectHTML(l)

def tribeSelectHTML(l:List[Tribe]):
	return  """<label>Select tribe</label><input type="text" class='selectors' id="tribeSelect" list="tribeList" value="Any" onchange="onChange()"><datalist id='tribeList'>""" + '<option>Any</option>' + ''.join(f'<option id={t.name}>{t.name}</option>\n' for t in l) + '</datalist>'

def funcSelectHTML(l:List[Tribe]):
	return  """<label>Select function</label><input type="text" class='selectors' id="functionsSelect" list="functionsList" value="Any" onchange="onChange()"><datalist id='functionsList'>""" + '<option>Any</option>' + ''.join(''.join(f'<option id={f.name}>{f.name}</option>\n' for f in t.functions) for t in l) + '</datalist>'

def areaSelectHTML(l:List[Tribe]):
	return  """<label>Select area</label><input type="text" class='selectors' id="areasSelect" list="areasList" value="Any" onchange="onChange()"><datalist id='areasList'>""" + '<option>Any</option>' + ''.join(''.join(''.join(f'<option id={a.name}>{a.name}</option>\n' for a in f.areas) for f in t.functions) for t in l) + '</datalist>'

def teamSelectHTML(l:List[Tribe]):
	return  """<label>Select team</label><input type="text" class='selectors' id="teamsSelect" list="teamsList" value="Any" onchange="onChange()"><datalist id='teamsList'">""" + '<option>Any</option>' + ''.join(''.join(''.join(''.join(f'<option id={t.name}>{t.name}</option>\n' for t in a.teams) for a in f.areas) for f in t.functions) for t in l) + '</datalist>'

def compSelectHTML(l:List[Tribe]):
	return """<label>Select competence</label><input type="text" class='selectors' id="competenceSelect" list="competenceList" value="Any" onchange="onChange()"><datalist id='competenceList' onchange="onChange('functionsSelect', '.function', 'block', 4)">""" + '<option>Any</option>' + ''.join(''.join(f'<option id={c.competence}>{c.competence}</option>\n' for c in t.competences) for t in l) + '</datalist>'

def leadsHTML(l:List[Tribe]):
	return tribeLeadHTML(l) + funcLeadHTML(l) + areaLeadHTML(l) + teamLeadHTML(l) + compLeadHTML(l)

def tribeLeadHTML(l:List[Tribe]):
	return  """<label>Select tribe lead</label><input type="text" class='selectors' id="tribeLead" list="tribeLeadList" value="Any" onchange="onChange()"><datalist id='tribeLeadList'">""" + '<option>Any</option>' + ''.join(f'<option id={t.lead}>{t.lead}</option>\n' for t in l) + '</datalist>'

def funcLeadHTML(l:List[Tribe]):
	return  """<label>Select function lead</label><input type="text" class='selectors' id="functionsLead" list="functionsLeadList" value="Any" onchange="onChange()"><datalist id='functionsLeadList'">""" + '<option>Any</option>' + ''.join(''.join(f'<option id={f.lead}>{f.lead}</option>\n' for f in t.functions) for t in l) + '</datalist>'

def areaLeadHTML(l:List[Tribe]):
	return  """<label>Select area lead</label><input type="text" class='selectors' id="areasLead" list="areasLeadList" value="Any" onchange="onChange()"><datalist id='areasLeadList'">""" + '<option>Any</option>' + ''.join(''.join(''.join(f'<option id={a.lead}>{a.lead}</option>\n' for a in f.areas) for f in t.functions) for t in l) + '</datalist>'

def teamLeadHTML(l:List[Tribe]):
	return  """<label>Select team lead</label><input type="text" class='selectors' id="teamsLead" list="teamsLeadList" value="Any" onchange="onChange()"><datalist id='teamsLeadList'">""" + '<option>Any</option>' + ''.join(''.join(''.join(''.join(f'<option id={t.lead}>{t.lead}</option>\n' for t in a.teams) for a in f.areas) for f in t.functions) for t in l) + '</datalist>'

def compLeadHTML(l:List[Tribe]):
	return """<label>Select competence lead</label><input type="text" class='selectors' id="competenceLead" list="compLeadList" value="Any" onchange="onChange()"><datalist id='compLeadList' onchange="onChange('tribeLead', '.allWrapper', 'flex', 5)">""" + '<option>Any</option>' + ''.join(''.join(f'<option id={c.name}>{c.name}</option>\n' for c in t.competences) for t in l) + '</datalist>'

def resetHTML():
	return """<button onclick='reset()'>Reset</button>"""

def memberHTML(l:List[Tribe]):
	return  """<label>Select team member</label><input type="text" class='selectors' id="membersSelect" list="membersList" value="Any" onchange="onChange()"><datalist id='membersList'">""" + '<option>Any</option>' + ''.join(''.join(''.join(''.join(''.join(f'<option id={safeName(e.name)}>{e.name}</option>\n' for e in t.employees) for t in a.teams) for a in f.areas) for f in t.functions) for t in l) + '</datalist>'
