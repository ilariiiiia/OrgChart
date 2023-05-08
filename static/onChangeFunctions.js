function areAttributesEq(stats, inputs) {
	let equal = false;
	let allAny = true;
	Object.entries(inputs).forEach(([key, value]) => {
		if(value == 'Any'){
			return; // continues the loop
		}
		allAny = false;
		value = value.replaceAll(' ', '_');
		if(value != stats[key]){
			equal = true;
		}
	});
	if(allAny){
		return false;
	}
	return equal;
}

function onChange() {
	let selectors = ["tribe", "functions", "areas", "teams", "competence"];
	let modifiers = ["Select", "Lead"];
	let inputs = {};
	modifiers.forEach((mod) => {
		selectors.forEach((sel) => {
			let sum = sel + mod;
			inputs[sum] = document.querySelector("#" + sum).value;
		});
	});
	selectors = ["tribe", "functions", "areas", "teams", "competence"];
	modifiers = ["Select", "Lead"];
	document.querySelectorAll(".employee").forEach((employee) => {
		let employeeStats = {};
		let hidden = false;
		selectors.forEach((sel) => {
			modifiers.forEach((mod) => {
				let sum = sel + mod;
				employeeStats[sum] = employee.getAttribute(sum);
			});
		});
		if(areAttributesEq(employeeStats, inputs)){
			employee.style.display = 'none';
		} else {
			employee.style.display = 'block';
		}
	});
	checkChildrenOf(1);
}

function reset() {
	document.querySelectorAll(".selectors").forEach((it) => {
		it.value="Any";
		it.onchange()
	});
}