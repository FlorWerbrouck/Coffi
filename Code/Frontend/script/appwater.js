const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let htmlTotalwater;
let totalwater;
let htmlTotalwateravg;
let totalwateravg;

const getapi = function () {
  gettotalwater();
  gettotalwateravg();
  gettotalwaterall()
}

const gettotalwater = function() {
  handleData(`http://${lanIP}/api/v1/totalwater`, showtotalwater);
}

const gettotalwateravg = function() {
  handleData(`http://${lanIP}/api/v1/totalwateravg`, showtotalwateravg);
}

const gettotalwaterall = function() {
  handleData(`http://${lanIP}/api/v1/totalwaterall`, showtotalwaterall);
}

const showtotalwater = function(data) {
  htmlTotalwater = `<p>Total water usage:<br />${data.water["sum(Value)"]} ml</p>`
  totalwater.innerHTML = htmlTotalwater
}

const showtotalwateravg = function(data) {
  htmlTotalwateravg = `<p>Average water usage:<br />${data.water["avg"]} ml</p>`
  totalwateravg.innerHTML = htmlTotalwateravg
}

const showtotalwaterall = function(data) {
  let converted_labels = [];
  let converted_data = [];
  for (const water of data.water) {
    converted_labels.push(water.DateTime);
    converted_data.push(water.Value);
  }
  drawchart(converted_labels, converted_data, "Water Usage", 6, 10, 0, 1500);
}

//#region *** charts***

const drawchart = function (labels, data, name, tickAmountx, tickAmounty, min, max) {
  var options = {
      chart: {
          type: 'scatter',
      },
      stroke: {
          curve: 'stepline',
      },
      dataLabels: {
          enabled: false,
      },
      series: [
          {
              name: name,
              data: data,
          },
      ],
      colors:['#0000FF'],
      labels: labels,
      noData: {
          text: "Loading...",
      },
      xaxis: {
          type: "datetime",
          tickAmount: tickAmountx,
      },
      yaxis: {
          tickAmount: tickAmounty,
          min: min,
          max: max,
      },
  };
  var chart = new ApexCharts(document.querySelector(".js-chart"), options);
  chart.render();
  console.log("render chart");
};

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
  totalwater = document.querySelector(".js-totalwater")
  totalwateravg = document.querySelector(".js-totalwateravg")
  
  getapi();
  toggleNav();
});