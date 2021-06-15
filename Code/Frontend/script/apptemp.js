const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let htmlTotaltempavg;
let totaltempavg;

const getapi = function () {
  gettotaltempavg();
  gettotaltempall()
}


const gettotaltempavg = function() {
  handleData(`http://${lanIP}/api/v1/totaltempavg`, showtotaltempavg);
}

const gettotaltempall = function() {
  handleData(`http://${lanIP}/api/v1/totaltempall`, showtotaltempall);
}

const showtotaltempavg = function(data) {
  htmlTotaltempavg = `<p>Average temperature:<br />${data.temp["avg"]} °C</p>`
  totaltempavg.innerHTML = htmlTotaltempavg
}

const showtotaltempall = function(data) {
  let converted_labels = [];
  let converted_data = [];
  for (const temp of data.temp) {
    converted_labels.push(temp.DateTime);
    converted_data.push(temp.Value);
  }
  drawchart(converted_labels, converted_data, "Temperature", 6, 10, 0, 100);
}

//#region *** charts***

const drawchart = function (labels, data, name, tickAmountx, tickAmounty, min, max) {
  var options = {
      chart: {
          type: 'area',
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
      colors:['#FF0000'],
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 90, 100]
        }
      },
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
  totaltempavg = document.querySelector(".js-totaltempavg")
  
  getapi();
  toggleNav();
});