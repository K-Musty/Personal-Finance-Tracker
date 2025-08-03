document.addEventListener('DOMContentLoaded', function() {
    let spendingChart;

    function renderChart(labels, data) {
        const ctx = document.getElementById('spendingChart').getContext('2d');

        if (spendingChart) {
            spendingChart.destroy();
        }

        spendingChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Spending by Category',
                    data: data,
                    backgroundColor: [
                        '#4CAF50', '#2196F3', '#FFC107', '#FF5722',
                        '#9C27B0', '#607D8B', '#00BCD4', '#8BC34A'
                    ],
                    borderWidth: 1
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
    }

    function fetchChartData() {
        fetch("/get_spending_data")
            .then(response => response.json())
            .then(data => {
                renderChart(data.labels, data.data);
            })
            .catch(err => console.error("Error fetching chart data:", err));
    }

    // Attach Add Transaction Form Handler
    const form = document.getElementById('add-transaction-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch('/add_transaction', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    fetchChartData();  // Update Chart after adding
                    this.reset();  // Clear form after submission
                }
            })
            .catch(err => console.error("Error adding transaction:", err));
        });
    }

    /function fetchChartData() {
        fetch("/get_spending_data")
            .then(response => response.json())
            .then(data => {
                console.log('Chart Data:', data);
                renderChart(data.labels, data.data);
            })
            .catch(err => console.error("Chart Fetch Error", err));
    }

    fetchChartData();
});
