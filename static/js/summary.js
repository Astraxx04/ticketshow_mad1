var chartData = data;
const chartContainer = document.getElementById("chartContainer");


for (let i = 0; i < 6; i++) {
	const cancard = document.createElement("canvas");
	cancard.classList.add("cancard");
    cancard.setAttribute('id', 'myChart'+(i+1));
    console.log(cancard);
	chartContainer.appendChild(cancard);
    createChart(i);
}

function createChart(i){
    const ctx = document.getElementById('myChart'+(i+1));
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mov1', 'Mov2', 'Mov1', 'Mov2', 'Mov1', 'Mov2'],
            datasets: [{
            label: '',
            data: [1, 2, 3, 3, 2, 3],
            borderWidth: 2,
            barThickness: 50
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Venue 1',
                    font: {
                        size: 24
                    }
                }
            },
            responsive: false,
            scales: {
            x: {
                title: {
                    color: 'black',
                    display: true,
                    text: 'Shows',
                    font: {
                        size: 18
                    }
                }
            }
            }
        }
    });
}