const lanIP = `192.168.168.168:5000`;
const socket = io(`http://${lanIP}`);
let htmlWaterniveau;
let htmlCoffeemug;
let waterniveau;
let coffeemug;

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_historiek_1", function (jsonObject) {
    console.info(jsonObject);
    htmlWaterniveau = `<p>Waterniveau: ${jsonObject.historiek.Value} cm</p>`
    waterniveau.innerHTML = htmlWaterniveau;
  });
  
  socket.on("B2F_historiek_2", function (jsonObject) {
    console.info(jsonObject);
    htmlCoffeemug = `<p>Coffeemug: ${jsonObject.historiek.Value}</p>`
    coffeemug.innerHTML = htmlCoffeemug;
  });
};

const koffieKnop = function () {
  socket.emit("F2B_buttonpushed")
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  waterniveau = document.querySelector(".js-waterniveau")
  coffeemug = document.querySelector(".js-coffeemug")
  document.getElementById("js-koffieknop").addEventListener("click", koffieKnop);
  listenToSocket();
});
