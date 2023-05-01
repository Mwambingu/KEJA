// Get the container element
// var btnContainer = document.getElementById("dashboard-links");
// var linkContainer = document.getElementById("dashboard-links");

// Get all buttons with class="btn" inside the container
// var btns = btnContainer.getElementsByClassName("btn");
// var links = linkContainer.getElementsByClassName("list-group-item");

// Loop through the buttons and add the active class to the current/clicked button
// for (var i = 0; i < links.length; i++) {
//     links[i].addEventListener("click", function () {
//         var current = document.getElementsByClassName("active");
//         current[0].className = current[0].className.replace(" active", "");
//         this.className += " active";
//     });
// }
console.log("Hello Loaded this shit!!!");

// apartment-dashboard
function deleteAllAptms() {
    fetch("/delete-all-apt", {
        method: "POST",
    }).then((_res) => {
        window.location.href = "/houses/apartments";
    });
}

function deleteApt(apt_id) {
    fetch("/delete-apt", {
        method: "POST",
        body: JSON.stringify({ apt_id: apt_id }),
    }).then((_res) => {
        window.location.href = "/houses/apartments";
    });
}

function removeTenant(apt_id) {
    fetch("/remove-tenant", {
        method: "POST",
        body: JSON.stringify({ apt_id: apt_id }),
    }).then((_res) => {
        window.location.href = "/houses/apartments";
    });
}

// base-html
var element = document.getElementById("wrapper");
var toggleButton = document.getElementById("menu-toggle");

toggleButton.onclick = function () {
    element.classList.toggle("toggled");
};

var path = window.location.pathname;
var page = path.split("/").pop();

console.log(page);

if (page === "apartments") {
    page = "houses";
}

// Get all buttons with class="btn" inside the container
// var btns = btnContainer.getElementsByClassName("btn");

var current = document.getElementsByClassName("active");
console.log(current);
current[0].className = current[0].className.replace(" active", "");
var navLink = document.getElementById(page);
navLink.className += " active";

// House-Dashboard
function getHouseId(houseId) {
    fetch("/get_id", {
        method: "POST",
        body: JSON.stringify({ houseId: houseId }),
    }).then((_res) => {
        window.location.href = "/houses/apartments";
    });
}

function deleteAllHouses() {
    fetch("/delete-all-hse", {
        method: "POST",
    }).then((_res) => {
        window.location.href = "/houses";
    });
}

function deleteHouse(house_id) {
    fetch("/delete-hse", {
        method: "POST",
        body: JSON.stringify({ house_id: house_id }),
    }).then((_res) => {
        window.location.href = "/houses";
    });
}

// Tenant Dashboard
function deleteTenant(tenant_id) {
    fetch("/delete-tenant", {
        method: "POST",
        body: JSON.stringify({ tenant_id: tenant_id }),
    }).then((_res) => {
        window.location.href = "/tenants";
    });
}

function deleteAllTenant() {
    fetch("/delete-all-tenant", {
        method: "POST",
    }).then((_res) => {
        window.location.href = "/tenants";
    });
}

function removeTenant(tenant_id) {
    fetch("/remove-tenant", {
        method: "POST",
        body: JSON.stringify({ tenant_id: tenant_id }),
    }).then((_res) => {
        window.location.href = "/tenants";
    });
}

function checkChange(selectId) {
    let count = 0;
    const selectElDiv = document.getElementById("house-select");

    const selectEl = selectElDiv.getElementsByTagName("select");
    const labelEl = selectElDiv.getElementsByTagName("label");

    for (select of selectEl) {
        console.log(select.id);
        console.log(labelEl[count].htmlFor);
        if (select.id === selectId) {
            console.log("They are equal!!");
        }
        if (select.id !== selectId) {
            select.style.display = "none";
        }

        if (select.id === selectId) {
            select.name = "selected";
        }

        if (labelEl[count].htmlFor !== selectId) {
            labelEl[count].style.display = "none";
        }
        count += 1;
    }
}
