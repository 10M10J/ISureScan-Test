// app.module.js
angular.module('myApp', []);

function toggleChat() {
    var chatPopup = document.getElementById("chatPopup");
    chatPopup.style.display = chatPopup.style.display === "none" || chatPopup.style.display === "" ? "block" : "none";
}
