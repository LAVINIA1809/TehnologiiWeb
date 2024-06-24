function createChartContainer(id, title) {
    const container = document.createElement('div');
    container.className = 'chart2';
    
    const chartTitle = document.createElement('h3');
    chartTitle.id = `${id}Title`;
    chartTitle.innerText = title;
    container.appendChild(chartTitle);

    const canvas = document.createElement('canvas');
    canvas.id = id;
    container.appendChild(canvas);

    document.getElementById('chart-container').appendChild(container);
}

function createChartContainer2(id, title) {
    const container = document.createElement('div');
    container.className = 'chart1';
    
    const chartTitle = document.createElement('h3');
    chartTitle.id = `${id}Title`;
    chartTitle.innerText = title;
    container.appendChild(chartTitle);

    const canvas = document.createElement('canvas');
    canvas.id = id;
    container.appendChild(canvas);

    document.getElementById('chart-container').appendChild(container);
}


async function getResults() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const entityType = urlParams.get('type');
        let entityName = urlParams.get('name');

        if (entityType && entityName) {
            console.log(entityType)
            switch (entityType) {
                case 'region':
                    document.getElementById('pageTitle').innerText = `Results for region: ${entityName}`;
                    
                    try {   
                             fetch(`http://localhost:8000/reg_result?type=${entityType}&name=${entityName}`, {
                                 method: 'GET'
                             })
                             .then(response => response.json())
                             .then(data => {
                                 console.log(data.data1);
                                 entityName = entityName.replace(/\s+/g, '');
                                const mapLink = `maps/${entityName}.geojson`;
                                 makeCountrysMap(data.data1, mapLink);
                                 console.log(data.data2);
                                 createBarChart(data.data2, 'Type of attacks', 'canvas5')
                                 console.log(data.data3);
                                 createBarChart(data.data3, 'Attacks on target type', 'canvas6')
                                 console.log(data.data4);
                                 createBarChart(data.data4, 'Attacks every year', 'canvas7')
                             });
                        return;
                    } catch (error) {
                        console.error('Fetch error:', error);
                    }
                    break;

                case 'country':

                    document.getElementById('pageTitle').innerText = `Results for country: ${entityName}`;
                    
                    try {
                             fetch(`http://localhost:8000/country_result.html?type=${entityType}&name=${entityName}`, {
                                 method: 'GET'
                             })
                             .then(response => response.json())
                             .then(data => {
                                entityName = entityName.replace(/\s+/g, '');
                                const mapLink = `maps/${entityName}.geojson`;
                                 console.log("Data 1 country", data.data1);
                                 makeStatesMap(data.data1, mapLink);
                                 console.log(data.data2);
                                 createBarChart(data.data2, 'Type of attacks', 'canvas5')
                                 console.log(data.data3);
                                 createBarChart(data.data3, 'Attacks on target type', 'canvas6')
                                 console.log(data.data4);
                                 createBarChart(data.data4, 'Attacks every year', 'canvas7')
                             });

                        return;
                    } catch (error) {
                        console.error('Fetch error:', error);
                    }
                    break;

                case 'provstate':

                    document.getElementById('pageTitle').innerText = `Results for state/province: ${entityName}`;
                    
                    try {
                             fetch(`http://localhost:8000/provstate_result.html?type=${entityType}&name=${entityName}`, {
                                 method: 'GET'
                             })
                             .then(response => response.json())
                             .then(data => {
                                
                                if(data.data1.length === 1){
                                    const entityType1 = 'city';
                                    const entityName1 = data.data1[0][0]
                                    window.location.href = `city_result.html?type=${entityType1}&name=${entityName1}`;
                                    return;
                                }

                                else if(data.data1.length > 1){
                                    console.log("Data 1 country", data.data1);
                                    createChartContainer2('canvas4', 'Attacks in every city');
                                    createPieChart(data.data1, 'Attacks in every city', 'canvas4');
                                }
                                
                                else{
                                    document.getElementById('chart-container').innerText = `No events in this region`;
                                    document.getElementById('chart-container').style.textAlign = 'center';
                                    document.getElementById('chart-container').style.fontSize = '24px';
                                    document.getElementById('chart-container').style.marginTop = '50px';
                                }
                                 
                                if(data.data2.length > 0){
                                    console.log(data.data2);
                                    createChartContainer('canvas5', 'Type of attacks');
                                    createBarChart(data.data2, 'Type of attacks', 'canvas5')
                                }
                                 
                                if(data.data3.length > 0){
                                    console.log(data.data3);
                                    createChartContainer('canvas6', 'Attacks on target type');
                                    createBarChart(data.data3, 'Attacks on target type', 'canvas6')
                                } 
                                 
                                if(data.data4.length > 0){
                                    console.log(data.data4);
                                    createChartContainer('canvas7', 'Attacks every year');
                                    createBarChart(data.data4, 'Attacks every year', 'canvas7')
                                }
                                 
                             });

                        return;
                    } catch (error) {
                        console.error('Fetch error:', error);
                    }
                    break;

                case 'city':

                    document.getElementById('pageTitle').innerText = `Results for city: ${entityName}`;
                    
                    try {
                            fetch(`http://localhost:8000/city_result.html?type=${entityType}&name=${entityName}`, {
                                 method: 'GET'
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log(data.data1);
                                console.log("entityName:", entityName);
                                const eventsList = document.getElementById('events-list');

                                if(data.data1.length === 0){
                                    document.getElementById('events-list').innerText = `No events for this city`;
                                    document.getElementById('events-list').style.textAlign = 'center';
                                    document.getElementById('events-list').style.fontSize = '24px';
                                    document.getElementById('events-list').style.marginTop = '50px';
                                }

                                else{
                                    data.data1.forEach(event => {
                                        const eventElement = document.createElement('div');
                                        eventElement.innerHTML = `
                                            
                                            <h2>${event.year}</h2>
                                            <p><span>Date:</span> ${event.date}</p>
                                            <p><span>Region:</span> ${event.region_name}</p>
                                            <p><span>Country:</span> ${event.country_name}</p>
                                            <p><span>Provstate:</span> ${event.provstate_name}</p>
                                            <p><span>City:</span> ${event.city_name}</p>
                                            <p><span>Attack type:</span> ${event.attack_name}</p>
                                            <p><span>Target:</span> ${event.target_name}</p>
                                            <p><span>Subtarget:</span> ${event.subtarget_name}</p>
                                            <p><span>Corp:</span> ${event.corp}</p>
                                            <p><span>Specific target:</span> ${event.spec_target}</p>
                                            <p><span>Criminal:</span> ${event.criminal}</p>
                                            <p><span>Motive:</span> ${event.motive}</p>
                                            <p><span>Summary:</span> ${event.summary}</p>
                                        `;
                            
                                        eventsList.appendChild(eventElement);
                                    });
                                    
                                    if (data.data2.length >= 3) {
                                        console.log(data.data2);
                                        createChartContainer('canvas5', 'Type of attacks');
                                        createBarChart(data.data2, 'Type of attacks', 'canvas5');
                                    }
            
                                    if (data.data3.length >= 3) {
                                        console.log(data.data3);
                                        createChartContainer('canvas6', 'Attacks on target type');
                                        createBarChart(data.data3, 'Attacks on target type', 'canvas6');
                                    }
            
                                    if (data.data4.length >= 3) {
                                        console.log(data.data4);
                                        createChartContainer('canvas7', 'Attacks every year');
                                        createBarChart(data.data4, 'Attacks every year', 'canvas7');
                                    }
                                }
                             });

                        return;
                    } catch (error) {
                        console.error('Fetch error:', error);
                    }
                    
                    break;
                default:
                    console.error('Invalid entity type:', entityType);
                    break;
            }
            

        } else {
            console.error('Invalid or missing parameters in URL');
        }

    } catch (error) {
        console.error('Fetch error:', error);
    }

    console.log("Am terminat")
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("A");
    getResults();
    console.log("B");
});
