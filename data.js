fetch('data1.json')
    .then(response => response.json())
    .then(data => {
        createPieChart(data, 'Title 1', 'canvas1');
    });

fetch('data2.json')
    .then(response => response.json())
    .then(data => {
        createPieChart(data, 'Title 2', 'canvas2');
    });

fetch('data3.json')
    .then(response => response.json())
    .then(data => {
        createPieChart(data, 'Title 3', 'canvas3');
    });

fetch('data4.json')
    .then(response => response.json())
    .then(data => {
        createPieChart(data, 'Title 4', 'canvas4');
    });

fetch('data5.json')
    .then(response => response.json())
    .then(data => {
        createBarChart(data, 'Title 5', 'canvas5');
    });

fetch('data6.json')
    .then(response => response.json())
    .then(data => {
        createBarChart(data, 'Title 6', 'canvas6');
    });


