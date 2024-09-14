// Get the modal
var aboutPopup = document.getElementById("aboutPopup");
var helpPopup = document.getElementById("helpPopup");
var loginPopup = document.getElementById("loginPopup");

// Get the button that opens the modal
var aboutBtn = document.getElementById("aboutBtn");
var helpBtn = document.getElementById("helpBtn");
var loginBtn = document.getElementById("loginBtn");

// Get the <span> element that closes the modal
var closeAbout = document.getElementById("closeAbout");
var closeHelp = document.getElementById("closeHelp");
var closeLogin = document.getElementById("closeLogin");

// When the user clicks the button, open the modal 
aboutBtn.onclick = function() {
    aboutPopup.style.display = "block";
}

helpBtn.onclick = function() {
    helpPopup.style.display = "block";
}

loginBtn.onclick = function() {
    loginPopup.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closeAbout.onclick = function() {
    aboutPopup.style.display = "none";
}

closeHelp.onclick = function() {
    helpPopup.style.display = "none";
}

closeLogin.onclick = function() {
    loginPopup.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == aboutPopup) {
        aboutPopup.style.display = "none";
    }
    if (event.target == helpPopup) {
        helpPopup.style.display = "none";
    }
    if (event.target == loginPopup) {
        loginPopup.style.display = "none";
    }
}

function openGoogleForm() {
    // Replace the URL below with the actual URL of your Google Form
    window.open("https://forms.gle/niZzHa2wuRqDzLne8", "_blank");
}