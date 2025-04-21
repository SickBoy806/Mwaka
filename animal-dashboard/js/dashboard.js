/**
 * Dashboard Charts Implementation
 * This file handles all chart rendering and data management for the Animal Management Dashboard
 */

// Initialize all charts when DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set Chart.js defaults
    Chart.defaults.font.family = "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
    Chart.defaults.color = "#666";
    
    // Initialize all charts
    initLocationChart();
    initTypeStatusChart();
    initTrainingChart();
    initMedicalTrendChart();
    
    // Add listener for the refresh button
    document.getElementById('refreshDashboard').addEventListener('click', refreshAllCharts);
});

/**
 * Initialize the Animals by Location chart
 */
function initLocationChart() {
    const ctx = document.getElementById('locationChart').getContext('2d');
    
    // Sample data - would be replaced with API data
    const data = {
        labels: ['Headquarters', 'TPS Moshi', 'Dodoma', 'Iringa'],
        datasets: [
            {
                label: 'Dogs',
                data: [45, 32, 18, 12],
                backgroundColor: 'rgba(0, 123, 255, 0.6)',
                borderColor: 'rgb(0, 123, 255)',
                borderWidth: 1
            },
            {
                label: 'Horses',
                data: [12, 8, 20, 15],
                backgroundColor: 'rgba(40, 167, 69, 0.6)',
                borderColor: 'rgb(40, 167, 69)',
                borderWidth: 1
            }
        ]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false,
                    text: 'Animals by Location'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw} animals`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Animals'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Location'
                    }
                }
            }
        }
    };
    
    window.locationChart = new Chart(ctx, config);
}

/**
 * Initialize the Animals by Type and Status chart
 */
function initTypeStatusChart() {
    const ctx = document.getElementById('typeStatusChart').getContext('2d');
    
    // Sample data - would be replaced with API data
    const data = {
        labels: ['Active', 'Inactive', 'In Training', 'Medical Leave'],
        datasets: [
            {
                label: 'Dogs',
                data: [65, 12, 25, 5],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.6)',
                    'rgba(108, 117, 125, 0.6)',
                    'rgba(255, 193, 7, 0.6)',
                    'rgba(220, 53, 69, 0.6)'
                ],
                borderColor: [
                    'rgb(40, 167, 69)',
                    'rgb(108, 117, 125)',
                    'rgb(255, 193, 7)',
                    'rgb(220, 53, 69)'
                ],
                borderWidth: 1
            },
            {
                label: 'Horses',
                data: [35, 8, 10, 2],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.3)',
                    'rgba(108, 117, 125, 0.3)',
                    'rgba(255, 193, 7, 0.3)',
                    'rgba(220, 53, 69, 0.3)'
                ],
                borderColor: [
                    'rgb(40, 167, 69)',
                    'rgb(108, 117, 125)',
                    'rgb(255, 193, 7)',
                    'rgb(220, 53, 69)'
                ],
                borderWidth: 1
            }
        ]
    };
    
    const config = {
        type: 'polarArea',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        generateLabels: function(chart) {
                            // Get the default legendItems
                            const original = Chart.overrides.polarArea.plugins.legend.labels.generateLabels;
                            const legendItems = original.call(this, chart);
                            
                            // Add type label to each item
                            let currentType = '';
                            return legendItems.map((item, i) => {
                                const type = i < 4 ? 'Dogs' : 'Horses';
                                if (type !== currentType) {
                                    currentType = type;
                                    item.text = `${type} - ${item.text}`;
                                }
                                return item;
                            });
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const datasetLabel = context.dataset.label || '';
                            return `${datasetLabel} - ${context.label}: ${context.raw}`;
                        }
                    }
                }
            }
        }
    };
    
    window.typeStatusChart = new Chart(ctx, config);
}

/**
 * Initialize the Training Progress chart
 */
function initTrainingChart() {
    const ctx = document.getElementById('trainingChart').getContext('2d');
    
    // Generate data for the last 12 months
    const labels = [];
    const currentDate = new Date();
    for (let i = 11; i >= 0; i--) {
        const date = new Date(currentDate);
        date.setMonth(currentDate.getMonth() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }));
    }
    
    // Sample data - would be replaced with API data
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Dogs Completing Training',
                data: [8, 12, 15, 10, 14, 16, 18, 20, 12, 15, 17, 19],
                borderColor: 'rgb(23, 162, 184)',
                backgroundColor: 'rgba(23, 162, 184, 0.1)',
                fill: true,
                tension: 0.4
            },
            {
                label: 'Horses Completing Training',
                data: [5, 7, 6, 8, 9, 7, 8, 10, 9, 11, 10, 12],
                borderColor: 'rgb(255, 193, 7)',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                fill: true,
                tension: 0.4
            }
        ]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Animals'
                    },
                    suggestedMax: 25
                },
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                }
            }
        }
    };
    
    window.trainingChart = new Chart(ctx, config);
}

/**
 * Initialize the Medical Cases Trend chart
 */
function initMedicalTrendChart() {
    const ctx = document.getElementById('medicalTrendChart').getContext('2d');
    
    // Generate data for the last 12 months
    const labels = [];
    const currentDate = new Date();
    for (let i = 11; i >= 0; i--) {
        const date = new Date(currentDate);
        date.setMonth(currentDate.getMonth() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }));
    }
    
    // Sample data - would be replaced with API data
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Dog Medical Cases',
                data: [15, 12, 10, 14, 9, 7, 8, 10, 13, 11, 6, 8],
                borderColor: 'rgb(220, 53, 69)',
                backgroundColor: 'rgba(220, 53, 69, 0.2)',
                borderWidth: 2,
                fill: true
            },
            {
                label: 'Horse Medical Cases',
                data: [8, 7, 5, 6, 4, 5, 7, 6, 8, 5, 3, 4],
                borderColor: 'rgb(111, 66, 193)',
                backgroundColor: 'rgba(111, 66, 193, 0.2)',
                borderWidth: 2,
                fill: true
            }
        ]
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Cases'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                }
            }
        }
    };
    
    window.medicalTrendChart = new Chart(ctx, config);
}

/**
 * Refresh all charts with animation
 */
function refreshAllCharts() {
    // Show loading indicator
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.add('active');
    
    // Simulate API data fetch
    const filters = {}; // In a real app, get current filters
    setTimeout(() => {
        updateChartsWithFilters(filters);
        
        // Update stats cards
        updateStatsCards();
        
        // Hide loading indicator
        loadingOverlay.classList.remove('active');
        
        // Show success message
        showToast('Dashboard data refreshed successfully!', 'success');
    }, 1500);
}

/**
 * Update chart with random data (for demo purposes)
 */
function updateChartWithRandomData(chart) {
    if (!chart) return;
    
    chart.data.datasets.forEach(dataset => {
        dataset.data = dataset.data.map(() => Math.floor(Math.random() * 30) + 5);
    });
    
    chart.update();
}

/**
 * Update stats cards with random data (for demo purposes)
 */
function updateStatsCards() {
    // Generate random values for stats
    const totalDogs = Math.floor(Math.random() * 50) + 80;
    const totalHorses = Math.floor(Math.random() * 30) + 40;
    const medicalCases = Math.floor(Math.random() * 15) + 5;
    const totalTransfers = Math.floor(Math.random() * 10) + 10;
    
    // Calculate random change percentages
    const dogsChange = (Math.random() * 10 - 5).toFixed(1);
    const horsesChange = (Math.random() * 10 - 5).toFixed(1);
    const medicalChange = (Math.random() * 10 - 5).toFixed(1);
    const transfersChange = (Math.random() * 20 - 5).toFixed(1);
    
    // Update DOM
    document.getElementById('totalDogs').textContent = totalDogs;
    document.getElementById('totalHorses').textContent = totalHorses;
    document.getElementById('medicalCases').textContent = medicalCases;
    document.getElementById('totalTransfers').textContent = totalTransfers;
    
    // Update change percentages with + or - sign
    document.getElementById('dogsChange').textContent = `${dogsChange > 0 ? '+' : ''}${dogsChange}% from last month`;
    document.getElementById('horsesChange').textContent = `${horsesChange > 0 ? '+' : ''}${horsesChange}% from last month`;
    document.getElementById('medicalChange').textContent = `${medicalChange > 0 ? '+' : ''}${medicalChange}% from last month`;
    document.getElementById('transfersChange').textContent = `${transfersChange > 0 ? '+' : ''}${transfersChange}% from last month`;
    
    // Update progress bars
    document.querySelector('#totalDogs').closest('.card-body').querySelector('.progress-bar').style.width = `${Math.abs(dogsChange) * 10}%`;
    document.querySelector('#totalHorses').closest('.card-body').querySelector('.progress-bar').style.width = `${Math.abs(horsesChange) * 10}%`;
    document.querySelector('#medicalCases').closest('.card-body').querySelector('.progress-bar').style.width = `${Math.abs(medicalChange) * 10}%`;
    document.querySelector('#totalTransfers').closest('.card-body').querySelector('.progress-bar').style.width = `${Math.abs(transfersChange) * 10}%`;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Check if toast container exists, if not create it
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show the toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Remove toast from DOM after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}