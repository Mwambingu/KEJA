// Get the container element
// var btnContainer = document.getElementById("dashboard-links");
var linkContainer = document.getElementById("dashboard-links");

// Get all buttons with class="btn" inside the container
// var btns = btnContainer.getElementsByClassName("btn");
var links = linkContainer.getElementsByClassName("list-group-item");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < links.length; i++) {
    links[i].addEventListener("click", function () {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}
