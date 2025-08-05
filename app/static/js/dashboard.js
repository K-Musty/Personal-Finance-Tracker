document.addEventListener('DOMContentLoaded', function() {
    const monthSelector = document.getElementById('monthSelector');
    const ctx = document.getElementById('spendingChart').getContext('2d');
    let spendingChart;

    // Fetch and populate months dropdown
    fetch('/get_available_months')
        .then(response => response.json())
        .then(months => {
            months.forEach(month => {
                const option = document.createElement('option');
                option.value = month;
                option.textContent = new Date(month + "-01").toLocaleString('default', { month: 'long', year: 'numeric' });
                monthSelector.appendChild(option);
            });
        });

    function fetchAndRenderChart(month = '') {
        let url = '/get_spending_data';
        if (month) {
            url += `?month=${month}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (spendingChart) {
                    spendingChart.destroy();  // Destroy previous chart
                }
                spendingChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    }

    // Initial Load
    fetchAndRenderChart();

    // On Month Selection Change
    monthSelector.addEventListener('change', function() {
        const selectedMonth = this.value;
        fetchAndRenderChart(selectedMonth);
    });
});
