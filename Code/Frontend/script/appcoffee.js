const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let water;
let mug;
let datetime;
let select;
let htmlSelect;
let htmlNextcoffee;
let nextcoffee;

const alert = function(text) {
  window.alert(text);
}

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_historiek_1", function (jsonObject) {
    water = jsonObject.historiek.Value
  });
  
  socket.on("B2F_historiek_2", function (jsonObject) {
    mug = jsonObject.historiek.Value
  });
};

const getcoffeplanned = function() {
  handleData(`http://${lanIP}/api/v1/nextcoffeeplanned`, shownextcoffee);
}

const getfuturecoffees = function() {
  handleData(`http://${lanIP}/api/v1/futurecoffees`, futurecoffees);
}

const shownextcoffee = function (data) {
  console.log(data);
  if (data.koffie == null) {
    htmlNextcoffee = `<p>Next coffee planned:<br />N/A</p>`
  }
  else{
    htmlNextcoffee = `<p>Next coffee planned:<br /> ${data.koffie.DateTime}</p>`
  }
  nextcoffee.innerHTML = htmlNextcoffee;

}

const futurecoffees = function (data) {
  console.log(data);
  if (data.koffie != null) {
    htmlSelect = "";
    for (koffie in data.koffie) {
      htmlSelect += `<option value=${data.koffie[koffie].MetingID}>${data.koffie[koffie].DateTime}</option>`
      select.innerHTML = htmlSelect
    }
  }
}

const koffieKnop = function () {
  if (mug == 0) {
    alert("Cannot make coffee, their is no coffeemug in the machine")
  }
  else {
    if (water == 0) {
      alert("Cannot make coffee, their is no water in the reservoir")
    }
    else {
      socket.emit("F2B_buttonpushed");
    }
  }
}

const insertkoffieknop = function () {
  if (Date.parse(datetime.value) > Date.parse(new Date())) {
    const jsonObject = {datetime: datetime.value}
    console.log(jsonObject)
    handleData(`http://${lanIP}/api/v1/nextcoffeeplanned`, callback, callbackerror, 'POST', JSON.stringify(jsonObject) )
    if (mug == 0) { alert("please place coffemug under coffeemachine") }
    if (water == 0) { alert("Please fill up reservoir") }
    socket.emit("F2B_buttonplanned");
  }
  else {
    alert("Datum van de geplannde koffie moet in de toekomst liggen")
  }
}

const deletekoffieknop = function () {
  handleData(`http://${lanIP}/api/v1/futurecoffees/${select.value}`, callback, callbackerror, 'DELETE');
  socket.emit("F2B_buttonplanned");
}

const callback = function(data) {
  console.log(data)
  getcoffeplanned();
  getfuturecoffees();
}

const callbackerror = function(data) {
  console.log(data)
}

function toggleNav() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function() {
          console.log("Klasse toegevoegd...");
          document.querySelector("body").classList.toggle("has-mobile-nav");
      })
  }
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  nextcoffee = document.querySelector(".js-nextcoffee")
  datetime = document.querySelector(".js-DateTime")
  select = document.querySelector(".js-select")
  document.getElementById("js-koffieknop").addEventListener("click", koffieKnop);
  document.getElementById("js-save").addEventListener("click", insertkoffieknop);
  document.getElementById("js-delete").addEventListener("click", deletekoffieknop);

  toggleNav();
  getcoffeplanned();
  getfuturecoffees();
  listenToSocket();
});