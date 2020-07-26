$(function () {

    var endpoint = 'api/chart/data'
    $.ajax({
      method: "GET",
      url: endpoint,
      success: function(data){
        labelsM = data.labelsM
        datachartM = data.MCurNMLas
        labelsY = data.labelsY
        datachartY = data.YCurrent
        labels = data.labels
        YCData = data.YCur
        YLData = data.YLas
        labelsMbar = data.labelsMbar
        datachartMbar = data.Mbar
        chartYPerformanceLine()
        chartMPerformancePie()
        chartYPerformancePie()
        chartMPerformanceBar()
      },
      error: function(error_data){
        console.log("error")
        console.log(error_data)
      }
    })

    var violet = '#DF99CA',
        red = '#F0404C',
        green = '#7CF29C',
        blue = '#4680ff';

    // ------------------------------------------------------- //
    // Charts Gradients
    // ------------------------------------------------------ //
    var ctx1 = $("canvas").get(0).getContext("2d");
    var gradient1 = ctx1.createLinearGradient(150, 0, 150, 300);
    gradient1.addColorStop(0, 'rgba(210, 114, 181, 0.91)');
    gradient1.addColorStop(1, 'rgba(177, 62, 162, 0)');

    var gradient2 = ctx1.createLinearGradient(10, 0, 150, 300);
    gradient2.addColorStop(0, 'rgba(252, 117, 176, 0.84)');
    gradient2.addColorStop(1, 'rgba(250, 199, 106, 0.92)');

    // ------------------------------------------------------- //
    // Bar Chart
    // ------------------------------------------------------ //
    function chartMPerformanceBar() {
      var BARCHARTEXMPLE    = document.getElementById('barChartExample1');
      var barChartExample = new Chart(BARCHARTEXMPLE, {
          type: 'bar',
          options: {
              scales: {
                  xAxes: [{
                      display: true,
                      gridLines: {
                          color: '#fff'
                      }
                  }],
                  yAxes: [{
                      display: true,
                      ticks: {
                          max: 500,
                          min: 0
                      },
                      gridLines: {
                          color: '#fff'
                      }
                  }]
              },
              legend: false
          },
          data: {
              labels: labelsMbar,
              datasets: [
                  {
                      label: "sold units",
                      backgroundColor: [
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2
                      ],
                      hoverBackgroundColor: [
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2
                      ],
                      borderColor: [
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2,
                          gradient2
                      ],
                      borderWidth: 1,
                      data: datachartMbar,
                  }
              ]
          }
      });
    }



    // ------------------------------------------------------- //
    // Line Chart lineChartExample
    // ------------------------------------------------------ //

    function chartYPerformanceLine() {
      var LINECHARTPERFORMANCE = document.getElementById('lineChartPerformance');
      var lineChartPerformance = new Chart(LINECHARTPERFORMANCE, {
          type: 'line',
          options: {
              legend: {labels:{fontColor:"#777", fontSize: 12}},
              scales: {
                  xAxes: [{
                      display: true,
                      gridLines: {
                          color: '#fff'
                      }
                  }],
                  yAxes: [{
                      display: true,
                      ticks: {
                          max: 500000,
                          min: 50000
                      },
                      gridLines: {
                          color: '#fff'
                      }
                  }]
              },
          },
          data: {
              labels: labels,
              datasets: [
                  {
                      label: "Current Year",
                      fill: true,
                      lineTension: 0.3,
                      backgroundColor: gradient1,
                      borderColor: 'rgba(210, 114, 181, 0.91)',
                      borderCapStyle: 'butt',
                      borderDash: [],
                      borderDashOffset: 0.0,
                      borderJoinStyle: 'miter',
                      borderWidth: 2,
                      pointBorderColor: gradient1,
                      pointBackgroundColor: "#fff",
                      pointBorderWidth: 2,
                      pointHoverRadius: 5,
                      pointHoverBackgroundColor: gradient1,
                      pointHoverBorderColor: "rgba(220,220,220,1)",
                      pointHoverBorderWidth: 2,
                      pointRadius: 1,
                      pointHitRadius: 10,
                      data: YCData,
                      spanGaps: false,
                  },
                  {
                      label: "last Year",
                      fill: true,
                      lineTension: 0.3,
                      backgroundColor: gradient2,
                      borderColor: 'rgba(210, 114, 181, 0.91)',
                      borderCapStyle: 'butt',
                      borderDash: [],
                      borderDashOffset: 0.0,
                      borderJoinStyle: 'miter',
                      borderWidth: 2,
                      pointBorderColor: gradient2,
                      pointBackgroundColor: "#fff",
                      pointBorderWidth: 2,
                      pointHoverRadius: 5,
                      pointHoverBackgroundColor: gradient2,
                      pointHoverBorderColor: "rgba(220,220,220,1)",
                      pointHoverBorderWidth: 2,
                      pointRadius: 1,
                      pointHitRadius: 10,
                      data: YLData,
                      spanGaps: false
                  }
              ]
          }
      });
    }


    // ------------------------------------------------------- //
    // Line Chart
    // ------------------------------------------------------ //

    var LINECHART = $('#lineChart1');
    var myLineChart = new Chart(LINECHART, {
        type: 'line',
        options: {
            scales: {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    ticks: {
                        max: 50,
                        min: 0
                    },
                    display: false
                }]
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
            datasets: [{
                label: "Page Visitors",
                fill: true,
                lineTension: 0.4,
                backgroundColor: "transparent",
                borderColor: green,
                pointBorderColor: green,
                pointHoverBackgroundColor: green,
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 3,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 50,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 1,
                pointRadius: 0,
                pointHitRadius: 1,
                data: [10, 30, 21, 15, 22, 8, 18, 13, 21, 13, 17, 13, 20, 15],
                spanGaps: false
            }]
        }
    });


    // ------------------------------------------------------- //
    // Line Chart
    // ------------------------------------------------------ //

    var LINECHART = $('#lineChart2');
    var myLineChart = new Chart(LINECHART, {
        type: 'line',
        options: {
            scales: {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    ticks: {
                        max: 50,
                        min: 0
                    },
                    display: false
                }]
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
            datasets: [{
                label: "Page Visitors",
                fill: true,
                lineTension: 0.4,
                backgroundColor: "transparent",
                borderColor: blue,
                pointBorderColor: blue,
                pointHoverBackgroundColor: blue,
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 3,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 5,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 1,
                pointRadius: 0,
                pointHitRadius: 1,
                data: [20, 14, 21, 15, 22, 8, 18, 13, 21, 13, 17, 13, 20, 15],
                spanGaps: false
            }]
        }
    });


    // ------------------------------------------------------- //
    // Line Chart 3
    // ------------------------------------------------------ //

    var LINECHART = $('#lineChart3');
    var myLineChart = new Chart(LINECHART, {
        type: 'line',
        options: {
            scales: {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    ticks: {
                        max: 50,
                        min: 0
                    },
                    display: false
                }]
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
            datasets: [{
                label: "Page Visitors",
                fill: true,
                lineTension: 0.4,
                backgroundColor: "transparent",
                borderColor: red,
                pointBorderColor: red,
                pointHoverBackgroundColor: red,
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 3,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 5,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 1,
                pointRadius: 0,
                pointHitRadius: 1,
                data: [20, 14, 21, 15, 22, 8, 18, 13, 21, 13, 17, 13, 20, 15],
                spanGaps: false
            }]
        }
    });


    // ------------------------------------------------------- //
    // Pie Chart
    // ------------------------------------------------------ //

    function chartMPerformancePie() {
      var PIECHART = document.getElementById('pieChartHome1');
      var pieChartHome1 = new Chart(PIECHART, {
          type: 'doughnut',
          options: {
              cutoutPercentage: 85,
              legend: {
                  display: false
              }
          },
          data: {
              labels: labelsM,
              datasets: [{
                  data: datachartM,
                  borderWidth: [0, 0],
                  backgroundColor: [
                      green,
                      "#eee",
                  ],
                  hoverBackgroundColor: [
                      green,
                      "#eee",
                  ]
              }]
          }
      });
    }



    // ------------------------------------------------------- //
    // Pie Chart
    // ------------------------------------------------------ //
    function chartYPerformancePie() {
      var PIECHART = $('#pieChartHome2');
      var myPieChart = new Chart(PIECHART, {
          type: 'doughnut',
          options: {
              cutoutPercentage: 85,
              legend: {
                  display: false
              }
          },
          data: {
              labels: labelsY,
              datasets: [{
                  data: datachartY,
                  borderWidth: [0, 0],
                  backgroundColor: [
                      blue,
                      "#eee"
                  ],
                  hoverBackgroundColor: [
                      blue,
                      "#eee"
                  ]
              }]
          }
      });
    }


    // ------------------------------------------------------- //
    // Pie Chart
    // ------------------------------------------------------ //
    var PIECHART = $('#pieChartHome3');
    var myPieChart = new Chart(PIECHART, {
        type: 'doughnut',
        options: {
            cutoutPercentage: 90,
            legend: {
                display: false
            }
        },
        data: {
            labels: [
                "First",
                "Second"
            ],
            datasets: [{
                data: [300, 50],
                borderWidth: [0, 0],
                backgroundColor: [
                    violet,
                    "#eee"
                ],
                hoverBackgroundColor: [
                    violet,
                    "#eee"
                ]
            }]
        }
    });


    // ------------------------------------------------------- //
    // Pie Chart
    // ------------------------------------------------------ //
    var PIECHART = $('#pieChartHome4');
    var myPieChart = new Chart(PIECHART, {
        type: 'doughnut',
        options: {
            cutoutPercentage: 90,
            legend: {
                display: false
            }
        },
        data: {
            labels: [
                "First",
                "Second"
            ],
            datasets: [{
                data: [200, 80],
                borderWidth: [0, 0],
                backgroundColor: [
                    green,
                    "#eee"
                ],
                hoverBackgroundColor: [
                    green,
                    "#eee"
                ]
            }]
        }
    });


});
