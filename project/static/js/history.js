document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    if (!dateInput.value) {
        dateInput.value = today; // Bugünün tarihini ayarlar
    }
    dateInput.addEventListener('input', function () {
        const selectedDate = new Date(this.value);
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        this.value = selectedDate.toLocaleDateString('en-GB', options).split('/').reverse().join('-');
    });

    const dateLocale = document.getElementById('date');
    dateLocale.addEventListener('focus', function (e) {
        e.target.type = 'date';
    });

    dateLocale.addEventListener('blur', function (e) {
        e.target.type = 'text';
    });
});
