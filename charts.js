function createPieChart(data, title, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.regions,
            datasets: [{
                data: data.attack_counts,
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
                    const clickedElementIndex = elements[0].index;
                    const label = this.data.labels[clickedElementIndex];
                    window.location.href = `details.html?region=${label}`;
                }
            }
        }
    });
}

function createBarChart(data, title, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.regions,
            datasets: [{
                data: data.attack_counts,
                backgroundColor: '#36A2EB',
                hoverBackgroundColor: '#FF6384'
            }]
        },
        options: {
            title: {
                display: true,
                text: title
            },
            scales: {
                y: [{
                    display: true,
                scaleLabel: {
                    display: true,
                    labelString: "Value"
                }
                }]
            },            
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    const clickedElementIndex = elements[0]._index;
                    const label = this.data.labels[clickedElementIndex];
                    window.location.href = `details.html?region=${label}`;
                }
            }
        }
    });
}