
fetch('data1.json')
    .then(response => response.json())
    .then(data => {
        makeRegMap(data, "maps/map.geojson");
    });

fetch('data2.json')
    .then(response => response.json())
    .then(data => {
        
        makeCountrysMap(data, "maps/world-outline-low-precision_759.geojson");
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

fetch('data7.json')
    .then(response => response.json())
    .then(data => {
        
        createBarChart(data, 'Attacks every year', 'canvas7');
    });


