/**
 * Dashboard Filters Implementation
 * This file handles the filtering functionality for the Animal Management Dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the filter form event listener
    const filterForm = document.getElementById('dashboardFilters');
    if (filterForm) {
        filterForm.addEventListener('submit', handleFilterSubmit);
        
        // Also handle reset button
        const resetButton = filterForm.querySelector('button[type="reset"]');
        if (resetButton) {
            resetButton.addEventListener('click', function(e) {
                // Small delay to ensure form values are reset before handling
                setTimeout(() => {
                    handleFilterSubmit(new Event('submit'));
                }, 100);
            });
        }
    }
    
    // Initialize the export buttons
    document.getElementById('exportPDF')?.addEventListener('click', handleExportPDF);
    document.getElementById('exportCSV')?.addEventListener('click', handleExportCSV);
    document.getElementById('printReport')?.addEventListener('click', handlePrintReport);
});

/**
 * Handle filter form submission
 * @param {Event} e - The form submit event
 */
function handleFilterSubmit(e) {
    e.preventDefault();
    
    // Show loading indicator
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.add('active');
    
    // Get filter values
    const formData = new FormData(document.getElementById('dashboardFilters'));
    const filters = {
        location: formData.get('location'),
        animalType: formData.get('animal_type'),
        status: formData.get('status'),
        dateRange: formData.get('date_range')
    };
    
    // Log filters for debugging
    console.log('Applied filters:', filters);
    
    // Simulate API request with delay
    setTimeout(() => {
        // Apply filters to dashboard data
        applyFilters(filters);
        
        // Update filter badge summary
        updateFilterSummary(filters);
        
        // Hide loading indicator
        loadingOverlay.classList.remove('active');
        
        // Show success message
        showToast('Filters applied successfully!', 'success');
    }, 1000);
}

/**
 * Apply filters to dashboard data
 * @param {Object} filters - The filter values
 */
function applyFilters(filters) {
    // Apply location filter
    filterByLocation(filters.location);
    
    // Apply animal type filter
    filterByAnimalType(filters.animalType);
    
    // Apply status filter
    filterByStatus(filters.status);
    
    // Apply date range filter
    filterByDateRange(filters.dateRange);
    
    // Update charts
    updateChartsWithFilters(filters);
    
    // Update activity log
    updateActivityLog(filters);
    
    // Update transfers list
    updateTransfersList(filters);
    
    // Update stats cards
    updateStatsCardsWithFilters(filters);
}

/**
 * Filter data by location
 * @param {string} location - The selected location
 */
function filterByLocation(location) {
    try {
        // In a real implementation, this would filter actual data
        console.log(`Filtering by location: ${location}`);
        
        // In a real app, you would likely fetch filtered data here.
    
    // For demo purposes, just add a badge to the header
    updateFilterBadge('location', location);
    
    // If not filtering all, adjust the location chart to highlight selected location
    if (location !== 'all' && window.locationChart) {
        const chartData = window.locationChart.data;
        const locationIndex = chartData.labels.findIndex(label => 
            label.toLowerCase().includes(location.replace('_', ' ')));
        
        if (locationIndex !== -1) {
            // Create a backgroundColorOriginal property if it doesn't exist
            if (!chartData.datasets[0].backgroundColorOriginal) {
                chartData.datasets.forEach(dataset => {
                    dataset.backgroundColorOriginal = [...dataset.backgroundColor];
                });
            }
            
            // Highlight the selected location
            chartData.datasets.forEach(dataset => {
                const newColors = dataset.backgroundColorOriginal.map((color, index) => {
                    return index === locationIndex ? color : 'rgba(200, 200, 200, 0.2)';
                });
                dataset.backgroundColor = newColors;
            });
            
            window.locationChart.update();
        }
    } else if (window.locationChart && window.locationChart.data.datasets[0].backgroundColorOriginal) {
        // Reset to original colors
        window.locationChart.data.datasets.forEach(dataset => {
            dataset.backgroundColor = dataset.backgroundColorOriginal;
        });
        window.locationChart.update();
    }
} catch (error) {
        console.error("Error filtering by location:", error);
        showToast('Error applying location filter.', 'danger');
    }
}

/**
 * Filter data by animal type
 * @param {string} animalType - The selected animal type
 */
function filterByAnimalType(animalType) {
    try {
        // In a real implementation, this would filter actual data
        console.log(`Filtering by animal type: ${animalType}`);
        
        // In a real app, you would likely fetch filtered data here.
    
    // For demo purposes, just add a badge to the header
    updateFilterBadge('animalType', animalType);
    
    // If filtering by a specific type, hide the other type's data in charts
    if (animalType !== 'all') {
        const charts = [
            window.locationChart,
            window.trainingChart,
            window.medicalTrendChart
        ];
        
        charts.forEach(chart => {
            if (!chart) return;
            
            chart.data.datasets.forEach(dataset => {
                // Check if we need to save original data
                if (!dataset.hiddenByFilter) {
                    dataset.hiddenByFilter = false;
                    dataset.originalHidden = dataset.hidden || false;
                }
                
                if (animalType === 'dog' && dataset.label.toLowerCase().includes('horse')) {
                    dataset.hidden = true;
                    dataset.hiddenByFilter = true;
                } else if (animalType === 'horse' && dataset.label.toLowerCase().includes('dog')) {
                    dataset.hidden = true;
                    dataset.hiddenByFilter = true;
                } else if (dataset.hiddenByFilter) {
                    dataset.hidden = dataset.originalHidden;
                    dataset.hiddenByFilter = false;
                }
            });
            
            chart.update();
        });
    } else {
        // Reset all charts to show all datasets
        const charts = [
            window.locationChart,
            window.trainingChart,
            window.medicalTrendChart
        ];
        
        charts.forEach(chart => {
            if (!chart) return;
            
            chart.data.datasets.forEach(dataset => {
                if (dataset.hiddenByFilter) {
                    dataset.hidden = dataset.originalHidden;
                    dataset.hiddenByFilter = false;
                }
            });
            
            chart.update();
        });
    }
} catch (error) {
        console.error("Error filtering by animal type:", error);
        showToast('Error applying animal type filter.', 'danger');
    }
}

/**
 * Filter data by status
 * @param {string} status - The selected status
 */
function filterByStatus(status) {
    try {
        // In a real implementation, this would filter actual data
        console.log(`Filtering by status: ${status}`);
        
        // In a real app, you would likely fetch filtered data here.
    
    // For demo purposes, just add a badge to the header
    updateFilterBadge('status', status);
    
    // If we have activity log items, filter them by status
    const activityItems = document.querySelectorAll('#activityLog .activity-item');
    if (status !== 'all' && activityItems.length > 0) {
        activityItems.forEach(item => {
            const itemText = item.textContent.toLowerCase();
            const matchesStatus = itemText.includes(status.toLowerCase());
            
            // Save original display if not saved yet
            if (!item.dataset.originalDisplay) {
                item.dataset.originalDisplay = item.style.display || '';
            }
            
            // Show or hide based on filter match
            item.style.display = matchesStatus ? item.dataset.originalDisplay : 'none';
        });
    } else if (activityItems.length > 0) {
        // Reset all items to their original display value
        activityItems.forEach(item => {
            if (item.dataset.originalDisplay) {
                item.style.display = item.dataset.originalDisplay;
            }
        });
    }
} catch (error) {
        console.error("Error filtering by status:", error);
        showToast('Error applying status filter.', 'danger');
    }
}

/**
 * Filter data by date range
 * @param {string} dateRange - The selected date range
 */
function filterByDateRange(dateRange) {
    try {
        // In a real implementation, this would filter actual data
        console.log(`Filtering by date range: ${dateRange}`);
        
        // In a real app, you would likely fetch filtered data here.
    
    // For demo purposes, just add a badge to the header
    updateFilterBadge('dateRange', dateRange);
    
    // If date range is set, update the charts to show specific time range
    if (dateRange !== 'all' && window.trainingChart && window.medicalTrendChart) {
        let dataPointsToShow;
        
        switch(dateRange) {
            case 'today':
                dataPointsToShow = 1;
                break;
            case 'week':
                dataPointsToShow = 1;
                break;
            case 'month':
                dataPointsToShow = 1;
                break;
            case 'quarter':
                dataPointsToShow = 3;
                break;
            case 'year':
                dataPointsToShow = 12;
                break;
            default:
                dataPointsToShow = 12;
        }
        
        // Save original data if not saved yet
        const charts = [window.trainingChart, window.medicalTrendChart];
        charts.forEach(chart => {
            if (!chart.originalData) {
                chart.originalData = {
                    labels: [...chart.data.labels],
                    datasets: chart.data.datasets.map(dataset => ({
                        data: [...dataset.data]
                    }))
                };
            }
            
            // Update chart to show only the selected range
            const endIndex = chart.originalData.labels.length;
            const startIndex = Math.max(0, endIndex - dataPointsToShow);
            
            chart.data.labels = chart.originalData.labels.slice(startIndex, endIndex);
            chart.data.datasets.forEach((dataset, i) => {
                dataset.data = chart.originalData.datasets[i].data.slice(startIndex, endIndex);
            });
            
            chart.update();
        });
    } else if (window.trainingChart?.originalData && window.medicalTrendChart?.originalData) {
        // Reset charts to original data
        const charts = [window.trainingChart, window.medicalTrendChart];
        charts.forEach(chart => {
            chart.data.labels = [...chart.originalData.labels];
            chart.data.datasets.forEach((dataset, i) => {
                dataset.data = [...chart.originalData.datasets[i].data];
            });
            chart.update();
        });
    }
} catch (error) {
        console.error("Error filtering by date range:", error);
        showToast('Error applying date range filter.', 'danger');
    }
}

/**
 * Update charts based on applied filters
 * @param {Object} filters - The applied filters
 */
function updateChartsWithFilters(filters) {
    try {
        // This would do more complex chart updates based on filters
        // For now, simple updates are done in the individual filter methods
        
        // In a real app, you might update chart data based on multiple filters combined.
    
    // Update chart titles to reflect active filters
    let titleSuffix = '';
    if (filters.location !== 'all') {
        titleSuffix += ` (${formatFilterValue(filters.location, 'location')})`;
    }
    if (filters.animalType !== 'all') {
        titleSuffix += ` (${formatFilterValue(filters.animalType, 'animalType')})`;
    }
    
    // Apply title changes to charts
    const chartHeaders = document.querySelectorAll('.card-header');
    chartHeaders.forEach(header => {
        // Save original text if not saved yet
        if (!header.dataset.originalText) {
            header.dataset.originalText = header.textContent;
        }
        
        // Update header text with filter information if necessary
        if (titleSuffix && (filters.location !== 'all' || filters.animalType !== 'all')) {
            const baseText = header.dataset.originalText.split('(')[0].trim();
            header.textContent = `${baseText} ${titleSuffix}`;
        } else {
            header.textContent = header.dataset.originalText;
        }
    });
} catch (error) {
        console.error("Error updating charts with filters:", error);
        showToast('Error updating charts.', 'danger');
    }
}

/**
 * Update activity log based on filters
 * @param {Object} filters - The applied filters
 */
function updateActivityLog(filters) {
    try {
        // For a real implementation, this would fetch filtered activity data from the server
        // For demo purposes, we'll simulate filtering the existing items
        
        const activityItems = document.querySelectorAll('#activityLog .activity-item');
        if (activityItems.length === 0) return;
        
        // Count how many items remain visible after filtering
        let visibleCount = 0;
        
        activityItems.forEach(item => {
            const itemText = item.textContent.toLowerCase();
            let shouldShow = true;
            
            // Apply each filter
            if (filters.location !== 'all') {
                const formattedLocation = formatFilterValue(filters.location, 'location').toLowerCase();
                shouldShow = shouldShow && itemText.includes(formattedLocation);
            }
            
            if (filters.animalType !== 'all') {
                const formattedType = formatFilterValue(filters.animalType, 'animalType').toLowerCase();
                shouldShow = shouldShow && itemText.includes(formattedType);
            }
            
            if (filters.status !== 'all') {
                const formattedStatus = formatFilterValue(filters.status, 'status').toLowerCase();
                shouldShow = shouldShow && itemText.includes(formattedStatus);
            }
            
            // In a real app, you might extract the date from the activity item
            // and compare it with the selected date range.
            // For this demo, we'll just check if a date is present and if so,
            // roughly filter based on the date range string in the item.
            if (filters.dateRange !== 'all') {
                //  Note: This assumes your activity items have a date or time string.
                //  You'll need to adapt this to your actual data structure.
                const dateRanges = {
                    today: ['today'],
                    week: ['day', 'days', 'week', 'weeks'],
                    month: ['week', 'weeks', 'month', 'months'],
                    quarter: ['month', 'months'],
                    year: ['month', 'months']
                };
                
                const rangeKeywords = dateRanges[filters.dateRange] || [];
                
                // Should show is true only if the filter matched AND the date range is applicable.
                // If there's no date-like string, we still treat it as "shouldShow".
                shouldShow = shouldShow && (rangeKeywords.length === 0 || rangeKeywords.some(keyword => itemText.includes(keyword)));
            }
            
            // Show or hide based on filter match
            if (!item.dataset.originalDisplay) {
                item.dataset.originalDisplay = item.style.display || '';
            }
            
            item.style.display = shouldShow ? item.dataset.originalDisplay : 'none';
            
            if (shouldShow) visibleCount++;
        });
        
        // Update the card header with filter summary
        const activityHeader = document.querySelector('#activityLog').closest('.card').querySelector('.card-header');
        if (activityHeader) {
            const badge = activityHeader.querySelector('.badge');
            if (badge) {
                badge.textContent = `Showing ${visibleCount} of ${activityItems.length} activities`;
            }
        }
    } catch (error) {
        console.error("Error updating activity log:", error);
        showToast('Error updating activity log.', 'danger');
    }
}

/**
 * Update transfers list based on filters
 * @param {Object} filters - The applied filters
 */
    function updateTransfersList(filters) {
        try {
            // For a real implementation, this would fetch filtered transfer data from the server
            // For demo purposes, we'll simulate filtering the existing items
            
            const transferItems = document.querySelectorAll('#transfersList .list-group-item');
            if (transferItems.length === 0) return;
            
            // Count how many items remain visible after filtering
            let visibleCount = 0;
            
            transferItems.forEach(item => {
                const itemText = item.textContent.toLowerCase();
                let shouldShow = true;
                
                // Apply each filter
                if (filters.location !== 'all') {
                    const formattedLocation = formatFilterValue(filters.location, 'location').toLowerCase();
                    shouldShow = shouldShow && itemText.includes(formattedLocation);
                }
                
                if (filters.animalType !== 'all') {
                    const formattedType = formatFilterValue(filters.animalType, 'animalType').toLowerCase();
                    shouldShow = shouldShow && itemText.includes(formattedType);
                }
                
                //  Example for status - adapt to your actual data structure.
                //   In this example, we look for "approved" or "pending" badges in the item.
                // if (filters.status !== 'all') {
                //    const formattedStatus = formatFilterValue(filters.status, 'status').toLowerCase();
                //    shouldShow = shouldShow && itemText.includes(formattedStatus);
                // }
                
                // Apply date filtering (adjust this according to your actual data structure).
                if (filters.dateRange !== 'all') {
                    //  Here, we apply date range filtering assuming the transfer items have a date.
                    //  You'll need to adapt the date extraction and comparison to your data.
                    //  This is a simplified example.
                    // const transferDate = item.querySelector('.transfer-date').textContent;
                    //  ... code to parse date and compare with dateRange ...
                    const dateRanges = {
                        today: ['today'],
                        week: ['day', 'days', 'week', 'weeks'],
                        month: ['week', 'weeks', 'month', 'months'],
                        quarter: ['month', 'months'],
                        year: ['month', 'months']
                    };
                    
                    const rangeKeywords = dateRanges[filters.dateRange] || [];
                    
                    shouldShow = shouldShow && (rangeKeywords.length === 0 || rangeKeywords.some(keyword => itemText.includes(keyword)));
                }
                
                // Show or hide based on filter match
                if (!item.dataset.originalDisplay) {
                    item.dataset.originalDisplay = item.style.display || '';
                }
                
                item.style.display = shouldShow ? item.dataset.originalDisplay : 'none';
                
                if (shouldShow) visibleCount++;
            });
            
            // Update the card header with filter summary
            const transfersHeader = document.querySelector('#transfersList').closest('.card').querySelector('.card-header');
            if (transfersHeader) {
                const badge = transfersHeader.querySelector('.badge');
                if (badge) {
                    badge.textContent = `Showing ${visibleCount} of ${transferItems.length} transfers`;
                }
            }
        } catch (error) {
            console.error("Error updating transfers list:", error);
            showToast('Error updating transfers list.', 'danger');
        }
    }
    
    
}

/**
 * Update stats cards based on filters
 * @param {Object} filters - The applied filters
 */
function updateStatsCardsWithFilters(filters) {
    try {
        // For a real implementation, this would involve fetching updated stat values from the server
        // based on the applied filters.
        
        // For this demo, we'll simply keep the existing values
        // In a real scenario, you'd make an API call here.
        console.log('Updating stats cards with filters (simulated)', filters);
        
        // Since we're not changing the actual data, we'll just update the
        // filter badge summary in the stat cards to reflect what's being shown.
        
        const statCards = document.querySelectorAll('.stats-card');
        statCards.forEach(card => {
            let title = card.querySelector('.card-title').textContent;
            let summary = '';
            
            if (filters.location !== 'all') {
                summary += `Location: ${formatFilterValue(filters.location, 'location')}, `;
            }
            if (filters.animalType !== 'all') {
                summary += `Type: ${formatFilterValue(filters.animalType, 'animalType')}, `;
            }
            // You could add status or date range summaries if relevant for the stats
            if (filters.status !== 'all') {
                summary += `Status: ${formatFilterValue(filters.status, 'status')}, `;
            }
            if (filters.dateRange !== 'all') {
                summary += `Date: ${formatFilterValue(filters.dateRange, 'dateRange')}`;
            }
            
            // Remove trailing comma and space, if any
            summary = summary.replace(/, $/, '');
            
            // Update or clear the filter summary badge in the card
            let badge = card.querySelector('.filter-badge');
            if (summary) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'badge bg-secondary ms-2 filter-badge';
                    card.querySelector('.card-title').parentNode.appendChild(badge);
                }
                badge.textContent = `Filters: ${summary}`;
            } else if (badge) {
                badge.remove();
            }
        });
    } catch (error) {
        console.error("Error updating stats cards:", error);
        showToast('Error updating stats cards.', 'danger');
    }
}

/**
 * Update filter summary badge
 * @param {Object} filters - The active filters
 */
function updateFilterSummary(filters) {
    try {
        // Update the main filter summary display, if you have one
        const filterSummaryDiv = document.getElementById('filterSummary');
        if (!filterSummaryDiv) return;
        
        let summaryText = 'Active Filters: ';
        let hasFilters = false;
        
        if (filters.location !== 'all') {
            summaryText += `Location: ${formatFilterValue(filters.location, 'location')}, `;
            hasFilters = true;
        }
        if (filters.animalType !== 'all') {
            summaryText += `Type: ${formatFilterValue(filters.animalType, 'animalType')}, `;
            hasFilters = true;
        }
        if (filters.status !== 'all') {
            summaryText += `Status: ${formatFilterValue(filters.status, 'status')}, `;
            hasFilters = true;
        }
        if (filters.dateRange !== 'all') {
            summaryText += `Date: ${formatFilterValue(filters.dateRange, 'dateRange')}, `;
            hasFilters = true;
        }
        
        // Remove trailing comma and space, if any
        summaryText = summaryText.replace(/, $/, '');
        
        filterSummaryDiv.textContent = hasFilters ? summaryText : 'No filters applied';
    } catch (error) {
        console.error("Error updating filter summary:", error);
        // Optionally, display an error message to the user.
    }
}

/**
 * Update or create a filter badge in the header
 * @param {string} filterType - The type of filter (e.g., 'location')
 * @param {string} value - The filter value
 */
function updateFilterBadge(filterType, value) {
    // You can customize this function to fit how badges are displayed in your header
    // In this example, we'll just log the filter for demonstration purposes
    console.log(`Filter updated: ${filterType} - ${value}`);
}

/**
 * Format filter values for display
 * @param {string} value - The filter value
 * @param {string} type - The filter type ('location', 'animalType', etc.)
 * @returns {string} - The formatted value
 */
function formatFilterValue(value, type) {
    if (!value) return '';
    
    switch(type) {
        case 'location':
            return value.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
        case 'animalType':
            return value.charAt(0).toUpperCase() + value.slice(1);
        case 'status':
            return value.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
        case 'dateRange':
            switch(value) {
                case 'today': return 'Today';
                case 'week': return 'Last 7 Days';
                case 'month': return 'Last 30 Days';
                case 'quarter': return 'Last 90 Days';
                case 'year': return 'Last 12 Months';
                default: return value;
            }
        default:
            return value;
    }
}

/**
 * Handle PDF export
 */
function handleExportPDF() {
    // For a real implementation, you'd trigger a PDF generation and download here
    console.log('Exporting to PDF...');
    
    // Show a success message or initiate a download
    showToast('Initiating PDF export...', 'info');
}

/**
 * Handle CSV export
 */
function handleExportCSV() {
    // For a real implementation, you'd trigger a CSV generation and download here
    console.log('Exporting to CSV...');
    
    // Show a success message or initiate a download
    showToast('Initiating CSV export...', 'info');
}

/**
 * Handle report printing
 */
function handlePrintReport() {
    // For a real implementation, you'd prepare and trigger the printing of a report
    console.log('Printing report...');
    
    // Show a message or open a print dialog
    showToast('Preparing report for printing...', 'info');
}