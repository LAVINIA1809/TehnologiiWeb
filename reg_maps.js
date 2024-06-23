var map = L.map('map1').setView([0, 0], 2);
var colors = ['#FFEDA0', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'];
var thresholds = [0, 500, 1000, 5000, 10000, 20000, 50000];
var clickedRegion = null;

function createLegend() {
    var legend = L.control({ position: 'bottomleft' });

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'legend');
        var labels = [];

        div.innerHTML += '<h4>Number of Attacks</h4>';

        for (var i = 0; i < thresholds.length; i++) {
            div.innerHTML +=
                '<i style="background:' + colors[i] + '"></i> ' +
                thresholds[i] + (thresholds[i + 1] ? '&ndash;' + thresholds[i + 1] + '<br>' : '+');
        }

        return div;
    };

    legend.addTo(map);
}


function preprocessData(data) {
    var result = {};
    data.forEach(function(entry) {
        result[entry[0]] = entry[1];
    });
    return result;
}


function getColor(d) {
    //console.log(d);
    return d > 50000 ? '#7F0000' :
           d > 20000 ? '#FF0000' :
           d > 10000 ? '#FF4500' :
           d > 5000  ? '#FF7F50' :
           d > 1000  ? '#FFA07A' :
           d > 500   ? '#FFD700' :
                       '#FFEDA0';
}


function style(feature) {
    const regionName = feature.properties.name;
    //console.log("regionName: ", regionName);
    const attackCount = attackData[regionName];
    //console.log("AttackCount: ", attackCount);
    //console.log("data: ", attackData);
    return {
        fillColor: getColor(attackCount),
        weight: 0.5,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.3
    };
}

function onEachFeature(feature, layer) {
    layer.on({
        click: function(e) {
            const entityType = "region";
            const entityName = feature.properties.name;
            
            window.location.href = `result.html?type=${entityType}&name=${entityName}`;
        }
    });
    layer.bindPopup(feature.properties.region + ": " + (attackData[feature.properties.region] || 0) + " atacuri");
}

function makeRegMap(data, mapLink) {
    
    attackData = preprocessData(data);

    var geojsonLayer = new L.GeoJSON.AJAX(mapLink, {
        style: style,
        onEachFeature: onEachFeature
    });

    geojsonLayer.on('data:loaded', function() {
        geojsonLayer.addTo(map); 
    });

    createLegend();

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}
