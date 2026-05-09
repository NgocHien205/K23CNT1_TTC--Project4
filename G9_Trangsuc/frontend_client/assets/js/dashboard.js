const ctx =
document.getElementById('myChart');

new Chart(ctx, {

    type: 'bar',

    data: {

        labels: ['Jan', 'Feb', 'Mar'],

        datasets: [{

            label: 'Doanh thu',

            data: [120, 190, 300]

        }]
    }
});