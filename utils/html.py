from utils.treeParser import Employee, Team, Area, Function, Tribe, Competence
from typing import List

def safeName(name: str):
	return name.replace(' ', '_')

def employeeHTML(e: Employee, l:List[Competence]):
	c = Competence('Competence not found', 'An error occurred', '#FF0000')

	for com in l:
		if com.name == e.competence_lead and com.competence == e.competence:
			c = com
			
	return f""" <div class='employee'>
 					<svg viewBox="0 0 500 500" width=30 height=30 style="fill:{c.color}">
						<path d="M256,224c53,0,96-43,96-96s-43-96-96-96s-96,43-96,96S203,224,256,224z M256,256c-70.7,0-128-57.3-128-128S185.3,0,256,0
							s128,57.3,128,128S326.7,256,256,256z"/>
						<path d="M96,512H64v-79.4c0-79.5,64.5-144,144-144c0.2,0,32.5,0.2,96.7,0.5c79.3,0.4,143.3,64.7,143.3,144V512h-32v-78.9
							c0-61.6-49.8-111.7-111.5-112l-96-0.5c-62.4,0-112.5,50.1-112.5,112V512z"/>
					</svg>
	   				<p>
						{e.name}
	  				</p>
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
	 				<div>
		 				{tribeCompetences(t)}
	   				</div>
	 			</div>"""
	
def renderTribes(l:List[Tribe]):
	return "".join(tribeHTML(t) for t in l)

def choiceHTML(l:List[Tribe]):
	onChangeFun = """
<script type='text/javascript'>
function onChangeFun(selector, selectorAll, disp){
	let selected = document.querySelector('#'+selector).value;
 	selected = selected.replaceAll(' ', '_')
 	console.log(selected);
 	document.querySelectorAll(selectorAll).forEach((it) => {
  		if(selected == 'Any'){
			it.style.display = disp;
	  	} else {
  			it.id === selected ? it.style.display = disp : it.style.display = 'none';
		}
	});
}
</script>
"""
	return onChangeFun + tribeSelectHTML(l) + funcSelectHTML(l) + areaSelectHTML(l) + teamSelectHTML(l)
	
def tribeSelectHTML(l:List[Tribe]):
	return  """<label>Select tribe</label><select id='tribeSelect' onchange="onChangeFun('tribeSelect', '.allWrapper', 'flex')">""" + '<option>Any</option>' + ''.join(f'<option id={t.name}>{t.name}</option>\n' for t in l) + '</select>'

def funcSelectHTML(l:List[Tribe]):
	return  """<label>Select function</label><select id='functionsSelect' onchange="onChangeFun('functionsSelect', '.function', 'block')">""" + '<option>Any</option>' + ''.join(''.join(f'<option id={f.name}>{f.name}</option>\n' for f in t.functions) for t in l) + '</select>'

def areaSelectHTML(l:List[Tribe]):
	return  """<label>Select area</label><select id='areasSelect' onchange="onChangeFun('areasSelect', '.area', 'block')">""" + '<option>Any</option>' + ''.join(''.join(''.join(f'<option id={a.name}>{a.name}</option>\n' for a in f.areas) for f in t.functions) for t in l) + '</select>'

def teamSelectHTML(l:List[Tribe]):
	return  """<label>Select team</label><select id='teamsSelect' onchange="onChangeFun('teamsSelect', '.team', 'block')">""" + '<option>Any</option>' + ''.join(''.join(''.join(''.join(f'<option id={t.name}>{t.name}</option>\n' for t in a.teams) for a in f.areas) for f in t.functions) for t in l) + '</select>'