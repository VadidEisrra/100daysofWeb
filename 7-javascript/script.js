window.onload = function() {
  let billTotal = document.getElementById("billAmount");
  let tipPer = document.getElementById("totalTip");
  let totalPer = document.getElementById("totalPerson");
  
  document.getElementById("selectTip").addEventListener("click", function(e) {
    if(e.target.type == 'radio') {
      let tipPercent = +document.querySelector('input[name="percent"]:checked').value;
      let peeps = +document.getElementById("numPeople").value;
      if (peeps == 0){
        peeps = 1; 
      };
      let bill = +billTotal.value;
      let tip = (tipPercent / 100) * bill;
      let perPersonTip = tip / peeps;
      let perPersonTotal = (bill + tip) / peeps;

      tipPer.textContent =  "$" + Math.round(perPersonTip * 100) / 100;
      totalPer.textContent = "$" + Math.round(perPersonTotal * 100) / 100;
      document.getElementById("resetButton").style.opacity = "100";
    };
  });

  document.getElementById("customTip").addEventListener("click", function(e) {
    if(e.target) {
      radioBtns = document.querySelectorAll('input[name="percent"]');
      for (i = 0; i < radioBtns.length; i++){
        radioBtns[i].checked = false;
      }
      tipPercent = parseInt(e.target.value);
      if (isNaN(tipPercent)){
        tipPercent = 0;
      };
      let peeps = +document.getElementById("numPeople").value;
      if (peeps == 0){
        peeps = 1; 
      };
      let bill = +billTotal.value;
      let tip = (tipPercent / 100) * bill;
      let perPersonTip = tip / peeps;
      let perPersonTotal = (bill + tip) / peeps;

      tipPer.textContent =  "$" + Math.round(perPersonTip * 100) / 100;
      totalPer.textContent = "$" + Math.round(perPersonTotal * 100) / 100;
      document.getElementById("resetButton").style.opacity = "100";
    };
  });

  document.getElementById("customTip").addEventListener("input", function(e) {
    if(e.target.value) {
      tipPercent = parseInt(e.target.value);
      let peeps = +document.getElementById("numPeople").value;
      if (peeps == 0){
        peeps = 1; 
      };
      let bill = +billTotal.value;
      let tip = (tipPercent / 100) * bill;
      let perPersonTip = tip / peeps;
      let perPersonTotal = (bill + tip) / peeps;

      tipPer.textContent =  "$" + Math.round(perPersonTip * 100) / 100;
      totalPer.textContent = "$" + Math.round(perPersonTotal * 100) / 100;
      document.getElementById("resetButton").style.opacity = "100";
    };
  });
  document.getElementById("numPeople").addEventListener("click", function(e) {
    if(e.target) {
      let tipPercent = +document.querySelector('input[name="percent"]:checked').value;
      let peeps = +document.getElementById("numPeople").value;
      if (peeps == 0){
        peeps = 1; 
      };
      let bill = +billTotal.value;
      let tip = (tipPercent / 100) * bill;
      let perPersonTip = tip / peeps;
      let perPersonTotal = (bill + tip) / peeps;

      tipPer.textContent =  "$" + Math.round(perPersonTip * 100) / 100;
      totalPer.textContent = "$" + Math.round(perPersonTotal * 100) / 100;
      document.getElementById("resetButton").style.opacity = "100";
    };
  });

  document.getElementById("numPeople").addEventListener("input", function(e) {
    if(e.target.value) {
      let tipPercent = +document.querySelector('input[name="percent"]:checked').value;
      let peeps = +document.getElementById("numPeople").value;
      if (peeps == 0){
        peeps = 1; 
      };
      let bill = +billTotal.value;
      let tip = (tipPercent / 100) * bill;
      let perPersonTip = tip / peeps;
      let perPersonTotal = (bill + tip) / peeps;

      tipPer.textContent =  "$" + Math.round(perPersonTip * 100) / 100;
      totalPer.textContent = "$" + Math.round(perPersonTotal * 100) / 100;
      document.getElementById("resetButton").style.opacity = "100";
    };
  });

};
