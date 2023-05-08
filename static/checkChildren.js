function checkChildrenOf(i) {
	const selectors = [".employee", ".team", ".area", ".function", ".tribe"];
	if(!(i > 1 && i < selectors.length)) {
		return;
	}
	let parents = Array.from(document.querySelectorAll(selectors[i]));
	parents.forEach((parent) => {
		let children = Array.from(parent.querySelectorAll(selectors[i-1]));
		let allHidden = true;
		children.forEach((child) => {
			if(getComputedStyle(child).display != 'none') {
				allHidden = false;
			}
		})
		if(allHidden){
			parent.style.display = 'none';
			if(parent.className == 'tribe') {
				parent.parentElement.style.display = 'none';
			}
		} else {
			parent.style.display = 'block';
			if(parent.className == 'tribe') {
				parent.parentElement.style.display = 'flex';
			}
		}
	});
	checkChildrenOf(i+1);
}

Array.from(document.querySelectorAll("input")).forEach((it) => {
	it.onclick = function () {
		it.value = '';
	}
})