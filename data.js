async function getData() {
    fetch(`http://localhost:8000/index.html`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.data1);
        makeRegMap(data.data1, "maps/map.geojson");
        console.log(data.data2);
        makeCountrysMap(data.data2, "maps/world-outline-low-precision_759.geojson");
        console.log(data.data3);
        createBarChart(data.data3, 'Type of attacks', 'canvas5');
        console.log(data.data4);
        createBarChart(data.data4, 'Attacks on target type', 'canvas6');
        console.log(data.data5);
        createBarChart(data.data5, 'Attacks every year', 'canvas7');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("A");
    getData();
    console.log("B");
});