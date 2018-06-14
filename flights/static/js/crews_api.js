function assignCrew(event) {
    event.preventDefault();

    if (isUserLoggedIn()) {
        let HTMLForm = document.getElementById("post-form");
        let csrf_token = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/, "$1");
        let header = new Headers();
        header.append('X-CSRFToken', csrf_token);

        let request = new Request('/assign-crew/', {
            method: 'POST',
            body: new FormData(HTMLForm),
            credentials: "same-origin",
            headers: header
        });
        fetch(request).then(function (data) {
            return data.json();
        }).then(function (data) {
            if (data['result'] === 'successful') {
                location.reload();
            } else if (data['result'] === 'busy') {
                alert("Sorry, crew is already assigned to other flight in this time.");
            }
        });
    } else {
        alert("Only logged in users can change the crew!");
    }

}

function isUserLoggedIn() {
    return localStorage.getItem('loggedin') !== null && localStorage.getItem('loggedin') === 'true';
}

function findDate() {
    let input = document.getElementById("date").value;

    if (input === "") {
        location.reload();
    } else {
        let table = document.getElementById("crews");
        let tr = table.getElementsByTagName("tr");
        let td;
        for (let i = 1; i < tr.length; ++i) {
            td = tr[i].getElementsByTagName("td")[3];
            if (td) {
                if (td.innerHTML !== input.toString()) {
                    tr[i].style.display = "none";
                } else {
                    tr[i].style.display = "";
                }
            }
        }
    }
}

function createFilter(data) {
    let input = document.getElementById("flight");
    for (let i = 1; i < sth.rows.length; ++i) {
        input.insertAdjacentHTML('beforeend', "<option value='" + sth.rows[i].getElementsByTagName("td")[0].innerHTML + "'>" +
            sth.rows[i].getElementsByTagName("td")[0].innerHTML + "</option>");
    }

    let input2 = document.getElementById("crew");
    for (let elem in data) {
        input2.insertAdjacentHTML('beforeend', "<option value='" + data[elem]['id'] + "'>" +
            data[elem]['captain_name'] + " " + data[elem]['captain_surname'] + "</option>");
    }
}



function createTable() {
    fetch(request).then(function (data) {
        return data.json();
    }).then(function (data) {
        let i = 0;
        let line = sth.insertRow(0);
        for (let elem in data[0]) {
            let cell = line.insertCell(i++);
            cell.innerHTML = elem;
        }
        let j = 1;
        for (let elem in data) {
            let line = sth.insertRow(j++);
            let i = 0;
            for (let val in data[elem]) {
                let cell = line.insertCell(i++);
                cell.innerHTML = data[elem][val];
            }
        }
    }).then(function () {
        fetch(request_crews).then(function (data) {
            return data.json();
        }).then(function (data) {
            createFilter(data);
            let button = document.getElementById("assign");
            button.addEventListener("click", assignCrew);
        })
    });
}

let sth = document.getElementById("crews");
let request = new Request("/flights");
let request_crews = new Request("/crews");
let rowsDisplayed = 20;
let ordering = [];

createTable();

function sort(page, th, pageCount, rowCount) {
    let s = (rowsDisplayed * page) - rowsDisplayed;
    let rows = th;
    for (let i = s; i < (s + rowsDisplayed) && i < rowCount; ++i) {
        rows += ordering[i];
    }
    sth.innerHTML = rows;
    document.getElementById("buttons").innerHTML = pageButtons(pageCount, th, pageCount, rowCount);
}


function pageButtons(pCount, th, pageCount, rowCount) {
    let arguments = ", " + th + ", " + pageCount + ", " + rowCount;
    let buttons = "";

    for (let i = 1; i <= pCount; ++i) {
        buttons += "<input type='button' value='" + i + "' onclick='sort(" + i + arguments + ")'>";
    }
    return buttons;
}



