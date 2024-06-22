
fetch('data1.json')
    .then(response => response.json())
    .then(data => {
        
        createPieChart(data, 'Attacks in every region', 'canvas1');
    });

fetch('data2.json')
    .then(response => response.json())
    .then(data => {
        
        createPieChart(data, 'Atacks in evry country', 'canvas2');
    });

fetch('data3.json')
    .then(response => response.json())
    .then(data => {
        
        createPieChart(data, 'Attacs in every province/state', 'canvas3');
    });

fetch('data4.json')
    .then(response => response.json())
    .then(data => {
        
        createPieChart(data, 'Attacks in every city', 'canvas4');
    });

fetch('data5.json')
    .then(response => response.json())
    .then(data => {
        
        createBarChart(data, 'Type of attacks', 'canvas5');
    });

fetch('data6.json')
    .then(response => response.json())
    .then(data => {
        
        createBarChart(data, 'Attacks on target type', 'canvas6');
    });


