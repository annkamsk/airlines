createLogin();

function createLogin() {
    if (localStorage.getItem('loggedin') !== 'true') {
        createLoginForm();
    } else {
        createLogoutForm();
    }
}

function createLoginForm() {
    let form = document.getElementById("login");
    let username = document.createElement("input");
    username.setAttribute("type", "text");
    username.setAttribute("id", "user");
    username.setAttribute("name", "user");
    let password = document.createElement("input");
    password.setAttribute("type", "password");
    password.setAttribute("id", "password");
    password.setAttribute("name", "password");
    let button = document.createElement("button");
    button.setAttribute("id", "log");
    button.setAttribute("type", "submit");
    button.innerHTML = "Login";
    button.addEventListener("click", login);
    form.appendChild(username);
    form.appendChild(password);
    form.appendChild(button);
}

function createLogoutForm() {
    let form = document.getElementById("login");
    let button = document.createElement("button");
    button.setAttribute("id", "log");
    button.setAttribute("type", "submit");
    button.innerHTML = "Logout";
    button.addEventListener("click", logout);
    form.appendChild(button);
}



function logout(event) {
    event.preventDefault();
    localStorage.setItem('loggedin', 'false');
    removeLogoutForm();
    createLoginForm();
}

function login(event) {
    event.preventDefault();
    let HTMLForm = document.getElementById("login");

    let request = new Request('/user-authenticate/', {
        method: 'POST',
        body: new FormData(HTMLForm),
        credentials: "omit"
    });

    fetch(request).then(function (data) {
        return data.json();
    }).then(function (data) {

        if (data['loggedin'] === 'true') {
            localStorage.setItem('loggedin', 'true');
            removeLoginForm();
            createLogoutForm();
        } else {
            alert("Your username or password was incorrect.");
        }
    });
}

function removeLoginForm() {
    document.getElementById("user").remove();
    document.getElementById("password").remove();
    document.getElementById("log").remove();
}

function removeLogoutForm() {
    document.getElementById("log").remove();
}
