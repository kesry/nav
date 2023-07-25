let selectFocus = (sel) => {

  let oSelect = event.target;  //选择框
  let oOptionsPanel = dq(sel); //菜单面板
  let oSelectPosition = oSelect.currentAbsolutePosition(); //oSelect的绝对位置
  oOptionsPanel.style.width = oSelect.currentStyle().width;
  oOptionsPanel.style.left = oSelectPosition.offsetX + 'px';
  oOptionsPanel.style.top = oSelectPosition.offsetY+ parseFloat(oSelect.currentStyle().height) + 5 + 'px';
  setTimeout(() => {
    oOptionsPanel.classNameExistOnly("options-peanl-none");
  }, 200)
  oOptionsPanel.style.opacity = 0;
  setTimeout(() => oOptionsPanel.style.opacity = 1, 200);

  oSelect.classNameExistOnly("select-focus");
  let oIcon = oSelect.getElementsByClassName("icon")[0];
  oIcon.classNameExistOnly("icon-rotate");
}

let optionClick = (sel) => {
  if(dq(".select>.label>span").innerText !== event.target.innerText) {
    dq(".select>.label>span").innerText = event.target.innerText;
    // let el = el || dq("#el-select-babel");
    let el = dq(sel)?dq(sel):dq("#el-select-babel");
    el.value = event.target.attr("value");
    el.text = event.target.innerText;
  }
}
