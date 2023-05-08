function onChangeFun(selector, selectorAll, disp, i){
	let selected = document.querySelector('#'+selector).value;
 	selected = selected.replaceAll(' ', '_');
 	document.querySelectorAll(selectorAll).forEach((it) => {
  		if(selected == 'Any'){
			it.style.display = disp;
	  	} else {
  			if(it.id === selected){
	 			it.style.display = disp;
	 		} else {
				it.style.display = 'none';
			}
		}
	});
 	checkChildrenOf(i);
}

function onChangeLead(selector, selectorAll, disp, i){
	let done = false;
	let selected = document.querySelector('#'+selector).value;
 	document.querySelectorAll(selectorAll).forEach((it) => {
  		if(selected == 'Any'){
			it.style.display = disp;
	  	} else {
			let children = Array.from(it.children);
  			if(children[1].innerHTML.trim() == selected){
				console.log('displayed', it);
	 			it.style.display = disp;
				done = true;
	 		} else {
				console.log('hidden', it)
				it.style.display = 'none';
			}
		}
	});
 	checkChildrenOf(i);
}

function onChangeCompetence(lead) {
	let selected = document.querySelector("#competenceSelect").value;
	document.querySelectorAll(".employee").forEach((it) => {
		let check = it.querySelector(".employeeCompetence")
		if(lead){
			check = it.querySelector(".employeeCompetenceLead")
		}
		if(check.innerHTML == selected){
			it.style.display = 'none';
		} else  {
			it.style.display = 'block';
		}
		if(selected == 'Any'){
			it.style.display = 'block';
		}
	});
	checkChildrenOf(1);
}

function onChangeTribe(lead) {
	let selected = document.querySelector("#tribeSelect").value;
	if(lead){
		selected = document.querySelector("#tribeLead").value;
	}
	document.querySelectorAll(".tribe").forEach((tribe) => {
		if(selected == 'Any') {
			tribe.style.display = 'block';
			return;
		}
		let check = tribe.children[0].innerHTML;
		if(lead) {
			check = tribe.children[1].innerHTML;
		}
		check = check.trim();
		if(check == selected) {
			tribe.style.display = 'block';
		} else {
			tribe.style.display = 'none';
		}
	})
}

function reset() {
	document.querySelectorAll(".selectors").forEach((it) => {
		it.value="Any";
		it.onchange()
	});
}