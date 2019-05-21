function make_doughnut_plot(canvas_name, data) {
    var ctx = document.getElementById(canvas_name).getContext('2d');
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data,
                backgroundColor: [
                    "rgba(0, 255, 0, 1)",
                    "rgba(0, 1, 10, 1)",
                    "rgba(0, 100, 120, 1)",
                    "rgba(200, 255, 30, 1)",
                    "rgba(100, 255, 140, 1)"
                ],
                label: 'Dataset 1'
            }],
            labels: [
                'Red',
                'Orange',
                'Yellow',
                'Green',
                'Blue'
            ]
        },
        options: {
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Chart.js Doughnut Chart'
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

function make_bar_plot(canvas_name, incoming_data, outgoing_data, labels){
    var ctx = document.getElementById(canvas_name).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: 
          [
            { 
              data: incoming_data,
              label: "Incoming",
              backgroundColor: "rgba(0, 255, 0, 1)",
              borderColor: "#000000",
              borderWidth: 1,
              fill: true,
            },
            { 
              data: outgoing_data,
              label: "Outgoing",
              backgroundColor: "rgba(255, 0, 10, 1)",
              borderColor: "#000000",
              borderWidth: 1,
              fill: true
            }
          ]
        },
        options: {
          scales: {
            xAxes: [{
                gridLines: {
                    display:false
                }
            }],
            yAxes: [{
                gridLines: {
                    display:false
                }   
            }]
          }
      }
    });
}

function make_line_plot(canvas_name, data, labels){
    var ctx = document.getElementById(canvas_name).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: 
          [
            { 
              data: data,
              label: "Incoming",
              backgroundColor: "rgba(0, 150, 255, 0.5)",
              borderColor: "rgba(0, 150, 255, 1)",
              fill: true,
            }
          ]
        },
        options: {
          scales: {
            xAxes: [{
                gridLines: {
                    display:false
                }
            }],
            yAxes: [{
                gridLines: {
                    display:false
                }   
            }]
          }
      }
    });
}