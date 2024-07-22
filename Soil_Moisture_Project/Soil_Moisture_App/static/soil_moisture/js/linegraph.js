function initializeCharts(data) {
    // Prepare data for Soil Moisture Chart
    const dates = data.map(item => `${item.date} ${item.time}`);
    const soilMoistures = data.map(item => item.soil_moisture);

    const temperature = data.map(item => item.temperature);
    const humidity = data.map(item => item.humidity);

    // Create Soil Moisture Chart
    const ctx1 = document.getElementById('soilMoistureChart').getContext('2d');
    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Soil Moisture',
                data: soilMoistures,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Create Temperature and Humidity Chart
    const ctx2 = document.getElementById('temperatureHumidityChart').getContext('2d');
    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Temperature',
                    data: temperature,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: false
                },
                {
                    label: 'Humidity',
                    data: humidity,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}