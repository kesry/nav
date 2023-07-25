/* add new class name for dom */
HTMLElement.prototype.addClassName = HTMLElement.prototype.addClassName || function(newClassName) {
	let current_class = this.getAttribute("class");
	current_class = current_class + " " + newClassName;
	this.setAttribute("class", current_class);
}

/*
remove classname from current dom
*/

HTMLElement.prototype.removeClassName = HTMLElement.prototype.removeClassName || function(className) {
	let current_class = this.getAttribute("class") || "";
	let classArr = current_class.split(" ");
	classArr = classArr.filter(e => {
		return e !== className;
	})
	this.setAttribute("class", classArr.join(" "));
}

/*
	oldClassName will be replaced by newClassName
*/
HTMLElement.prototype.classReplace = HTMLElement.prototype.classReplace || function(oldClassName, newClassName) {
	let current_class = this.getAttribute("class") || "";
	let classArr = current_class.split(" ");
	classArr.forEach((e, i) => {
		if(e === oldClassName) classArr[i] = newClassName;
	})
	this.setAttribute("class", classArr.join(" "));
}

/* 判断dom中是否存在该类名 */
HTMLElement.prototype.classNameIsExist = HTMLElement.prototype.classNameIsExist || function(className) {
	let current_class = this.getAttribute("class") || "";
	let index = current_class.indexOf(className);
	return index >= 0;
}

/* className1 和 className2只能存在一个 */
HTMLElement.prototype.classNameExistOnly = HTMLElement.prototype.classNameExistOnly || function(className1, className2) {
	if(!className1) throw new Error("The function must send param");
	//className1 和 className2都存在
	if(className2) {
		let current_class = this.getAttribute("class") || "";
		let classArr = current_class.split(" ");
		classArr.forEach((e, i) => {
			if(e === className1) classArr[i] = className2;
			else if(e === className2) classArr[i] = className1;
		})
		this.setAttribute("class", classArr.join(" "))
	}
	// className2不存在
	else {
		//className1已存在
		if(this.classNameIsExist(className1)) this.removeClassName(className1);
		//className1不存在
		else this.addClassName(className1);
	}
}

/* 获取当前元素的样式 */
HTMLElement.prototype.currentStyle = HTMLElement.prototype.currentStyle || function() {
	if(document.defaultView.getComputedStyle)
		//不是IE
		return document.defaultView.getComputedStyle(this);
	else
		return this.currentStyle;
}

/* 获取当前元素的浏览器的绝对位置 */
HTMLElement.prototype.currentAbsolutePosition = HTMLElement.prototype.currentAbsolutePosition || function() {
	let temp = this;
	let x = 0, y = 0;
	while(temp) {
		x += temp.offsetLeft;
		y += temp.offsetTop;
		temp = temp.offsetParent;
	}
	return { offsetX: x, offsetY: y};
}

/* 获取当前元素的属性 */
HTMLElement.prototype.attr = HTMLElement.prototype.attr || function(name, value) {
	if(value) this.setAttribute(name, value);
	else return this.getAttribute(name);
}

let dq = sel => document.querySelector(sel)
