function createPieChart(data, title, canvasId) {
    const regions = [];
    const attackCounts = [];
    data.forEach(entry => {
        regions.push(entry[0]);
        attackCounts.push(entry[1]);
    });

    const ctx = document.getElementById(canvasId).getContext('2d');
    const pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: regions,
            datasets: [{
                data: attackCounts,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            title: {
                display: true,
                text: title
            },
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    const entityType = "city";
                    const clickedElementIndex = elements[0].index;
                    const label = this.data.labels[clickedElementIndex];
                    window.location.href = `city_result.html?type=${entityType}&name=${label}`;
                }
            }
        }
    });
}

function createBarChart(data, title, canvasId) {
    const regions = [];
    const attackCounts = [];
    data.forEach(entry => {
        regions.push(entry[0]);
        attackCounts.push(entry[1]);
    });

    const ctx = document.getElementById(canvasId).getContext('2d');
    const barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: regions, 
            datasets: [{
                data: attackCounts,
                backgroundColor: '#36A2EB',
                hoverBackgroundColor: '#FF6384'
            }]
        },
        options: {
            title: {
                display: true,
                text: title
            },
            legend: {
                display:false,
                text:"Number of attacks",
                position: 'bottom',
                labels: {
                    fontColor: 'black',
                    fontSize: 14,
                    fontStyle: 'normal',
                    text: 'Attacks Number' 
                },
                title:{
                    text: "Number of attacks"
                }
            },         
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    const clickedElementIndex = elements[0]._index;
                    const label = this.data.labels[clickedElementIndex];
                    window.location.href = `result.html?region=${label}`;
                }
            }
        }
    });
}
