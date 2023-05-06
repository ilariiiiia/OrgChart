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
	 		} else {
				console.log('hidden', it)
				it.style.display = 'none';
			}
		}
	});
 	checkChildrenOf(i);
}