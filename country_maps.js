(function () {
    var map = L.map('map2').setView([0, 0], 2);
    var colors = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026', '#4C0000', '#1A0000'];
    var thresholds = [0, 50, 100, 500, 1000, 5000, 10000, 20000, 30000];

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
        return d > 30000 ? colors[8] :
               d > 20000 ? colors[7] :
               d > 10000 ? colors[6] :
               d > 5000  ? colors[5] :
               d > 1000  ? colors[4] :
               d > 500   ? colors[3] :
               d > 100   ? colors[2] :
               d > 50    ? colors[1] :
                           colors[0];
    }

    function style(feature) {
        const regionName = feature.properties.name;
        //console.log("region name: ", regionName);
        const attackCount = attackData2[regionName];
        //console.log("attackCount: ", attackCount);
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
                window.location.href = `result.html?region=${feature.properties.region}`;
            }
        });
        layer.bindPopup(feature.properties.region + ": " + (attackData2[feature.properties.region] || 0) + " atacuri");
    }

    window.makeCountrysMap = function(data, mapLink) {
        attackData2 = preprocessData(data);
        //console.log("data: ", attackData2);

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
    };
})();
