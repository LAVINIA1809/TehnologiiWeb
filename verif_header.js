document.addEventListener('DOMContentLoaded', () => {
    const firstName = localStorage.getItem('userFirstName');
    const lastName = localStorage.getItem('userLastName');
    const header = document.getElementById('header');

    if (firstName && lastName) {
        // Utilizatorul este logat
        header.innerHTML = `
        <div class="menu">
            <a class="option current-page" href="homeLogged.html"> HOME </a>
            <a class="option" href="addEvent.html"> ADD EVENT </a>
            <a class="option" href="register.html"> REGISTER </a>
            <a class="option" id="accountInfo" href="admin.html"></a>
        </div>
        `;
        const accountInfoDiv = document.getElementById('accountInfo');
        accountInfoDiv.style.whiteSpace = 'pre-line';
        accountInfoDiv.textContent = `ACCOUNT:\n${firstName} ${lastName}`;
    } else {
        // Utilizatorul nu este logat
        header.innerHTML = `
        <div class="menu">
            <a class="option" href="index.html"> HOME </a>
            <a class="option" href="about.html"> ABOUT </a>
            <a class="option" href="help.html"> HELP </a>
            <a class="option" href="login.html"> LOGIN </a>
        </div>
        `;
    }
});