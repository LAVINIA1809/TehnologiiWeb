function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function formatDate(dateString) {
    const months = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"];
    const parts = dateString.split("-");
    const day = parseInt(parts[2], 10);
    const month = parseInt(parts[1], 10);
    const year = parseInt(parts[0], 10);
    return day + " " + months[month - 1] + " " + year;
}

const fetchChartData = async (regName, canvasId, chartType, chartTitle) => {
    try {
        const response = await fetch(`get_reults.php?reg_name=${regName}`);
        const data = await response.json();

        if (chartType === 'pie') {
            createPieChart(data, chartTitle, canvasId);
        } else if (chartType === 'bar') {
            createBarChart(data, chartTitle, canvasId);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

var region = getParameterByName('region');

document.getElementById('regionTitle').innerText = region;

fetchChartData(region, 'canvas1', 'pie', 'Attacks in every region');

