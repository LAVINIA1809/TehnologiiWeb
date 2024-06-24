async function getResults() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const entityType = urlParams.get('type');
        let entityName = urlParams.get('name');

        if (entityType && entityName) {
            url = `http://localhost:8000/result?type=${entityType}&name=${entityName}`;
            switch (entityType) {
                case 'region':
                    document.getElementById('pageTitle').innerText = `Results for region: ${entityName}`;
                    
                    try {
                        
                            
                             fetch(url, {
                                 method: 'GET'
                             })
                             .then(response => response.json())
                             .then(data => {
                                 console.log('Get successful', data);

                             });

                             console.log("salut3")
                
                        

                        entityName = entityName.replace(/\s+/g, '');
                        const mapLink = `maps/${entityName}.geojson`;

                        console.log("salut")

                        await Promise.all([
                            console.log("sunt aici"),
                            fetch('data2.json')
                            .then(response => response.json())
                            .then(data => {
                                makeCountrysMap(data, mapLink);
                            }),
                            fetch('data5.json')
                                .then(response => response.json())
                                .then(data => createBarChart(data, 'Type of attacks', 'canvas5')),
                            fetch('data6.json')
                                .then(response => response.json())
                                .then(data => createBarChart(data, 'Attacks on target type', 'canvas6')),
                            fetch('data7.json')
                                .then(response => response.json())
                                .then(data => createBarChart(data, 'Attacks every year', 'canvas7'))
                        ]);
                        console.log("am iesit de aici");
                        return;
                    } catch (error) {
                        console.error('Fetch error:', error);
                    }
                    break;
                // case 'country':
                //     document.getElementById('pageTitle').innerText = `Results for country: ${entityName}`;
                    
                //     try {
                //         const response = await fetch(`http://localhost:8000/result?type=${entityType}&name=${entityName}`, {
                //             method: 'GET'
                //         });
            
                //         if (!response.ok) {
                //             console.error('Response not ok:', response.status);
                //             return;
                //         }
            
                //         const data1 = await response.json();
                //         console.log('Get successful', data1);

                //         entityName = entityName.replace(/\s+/g, '');
                //         const mapLink = `maps/${entityName}.geojson`;
            
                //         // Așteaptă ca toate datele să fie procesate înainte de a continua
                //         await Promise.all([
                //             fetch('data2.json')
                //             .then(response => response.json())
                //             .then(data => {
                                
                //                 makeStatesMap(data, mapLink);
                //             }),
                //             fetch('data5.json')
                //                 .then(response => response.json())
                //                 .then(data => createBarChart(data, 'Type of attacks', 'canvas5')),
                //             fetch('data6.json')
                //                 .then(response => response.json())
                //                 .then(data => createBarChart(data, 'Attacks on target type', 'canvas6')),
                //             fetch('data7.json')
                //                 .then(response => response.json())
                //                 .then(data => createBarChart(data, 'Attacks every year', 'canvas7'))
                //         ]);
            
                //     } catch (error) {
                //         console.error('Fetch error:', error);
                //     }
                    
                //     break;
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
