/* Smart Attendance App - JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // Mobile menu toggle (if needed in future)
    const navToggle = document.querySelector('.nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            document.querySelector('.nav-menu').classList.toggle('active');
        });
    }

    // Attendance select all present
    const selectAllPresent = document.getElementById('selectAllPresent');
    if (selectAllPresent) {
        selectAllPresent.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.toggle-btn.present input').forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // Attendance select all absent
    const selectAllAbsent = document.getElementById('selectAllAbsent');
    if (selectAllAbsent) {
        selectAllAbsent.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.toggle-btn.absent input').forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // Add quick action buttons for attendance
    const attendanceList = document.querySelector('.attendance-list');
    if (attendanceList) {
        const quickActions = document.createElement('div');
        quickActions.className = 'quick-actions';
        quickActions.innerHTML = `
            <button id="markAllPresent" class="btn btn-success btn-sm">
                <i class="fas fa-check-double"></i> Mark All Present
            </button>
            <button id="markAllAbsent" class="btn btn-danger btn-sm">
                <i class="fas fa-times-circle"></i> Mark All Absent
            </button>
        `;

        const cardHeader = document.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.appendChild(quickActions);
        }

        document.getElementById('markAllPresent').addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.toggle-btn.present input[type="radio"]').forEach(radio => {
                radio.checked = true;
            });
        });

        document.getElementById('markAllAbsent').addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.toggle-btn.absent input[type="radio"]').forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // Confirm before leaving attendance page with unsaved changes
    let formChanged = false;
    const attendanceForm = document.querySelector('.attendance-list + form, form:has(.attendance-list)');
    if (attendanceForm) {
        attendanceForm.querySelectorAll('input[type="radio"]').forEach(input => {
            input.addEventListener('change', () => { formChanged = true; });
        });

        window.addEventListener('beforeunload', function(e) {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = '';
            }
        });

        attendanceForm.addEventListener('submit', () => {
            formChanged = false;
        });
    }

    // Set today's date as default for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });

    // Search/filter for tables
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        const wrapper = table.closest('.card');
        if (wrapper) {
            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.placeholder = 'Search...';
            searchInput.className = 'table-search';
            searchInput.style.cssText = 'padding: 8px 12px; border: 2px solid #e0e0e0; border-radius: 8px; margin-bottom: 10px; width: 100%; max-width: 300px;';

            const header = wrapper.querySelector('.card-header');
            if (header) {
                header.appendChild(searchInput);
            }

            searchInput.addEventListener('input', function() {
                const term = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(term) ? '' : 'none';
                });
            });
        }
    });

    console.log('Smart Attendance App loaded!');
});
