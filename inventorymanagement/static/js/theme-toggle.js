document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const darkClass = 'dark-mode';

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add(darkClass);
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    toggleButton.addEventListener('click', function (e) {
        e.preventDefault();
        document.body.classList.toggle(darkClass);

        if (document.body.classList.contains(darkClass)) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
});
