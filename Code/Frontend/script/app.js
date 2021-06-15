const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let htmlWaterniveau;
let waterniveau;
let htmlCoffeemug;
let coffeemug;
let htmlNextcoffee;
let nextcoffee;

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_historiek_1", function (jsonObject) {
    console.info(jsonObject);
    htmlWaterniveau = `<p>Waterlevel:<br />${jsonObject.historiek.Value} ml</p>`
    waterniveau.innerHTML = htmlWaterniveau;
  });

  socket.on("B2F_historiek_2", function (jsonObject) {
    console.info(jsonObject);
    if (jsonObject.historiek.Value == 1) {htmlCoffeemug = `<p>Coffeemug:<br />present</p>`}
    else {htmlCoffeemug = `<p>Coffeemug:<br />not present</p>`}
    coffeemug.innerHTML = htmlCoffeemug;
  });
};

const getcoffeplanned = function() {
  handleData(`http://${lanIP}/api/v1/nextcoffeeplanned`, shownextcoffee);
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
  waterniveau = document.querySelector(".js-waterniveau")
  coffeemug = document.querySelector(".js-coffeemug")
  nextcoffee = document.querySelector(".js-nextcoffee")

  toggleNav();
  getcoffeplanned();
  listenToSocket();
});