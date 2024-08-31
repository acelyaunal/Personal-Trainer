document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.exercise-checkbox');
    const startButton = document.getElementById('start-button');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.closest('.exercises-link').classList.add('selected');
            } else {
                this.closest('.exercises-link').classList.remove('selected');
            }
            
            const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
            startButton.disabled = !anyChecked;
        });
    });
});

window.onpopstate = function(event) {
    window.location.href = "{{ url_for('logout') }}";
};
