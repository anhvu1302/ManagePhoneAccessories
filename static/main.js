let searchForm = document.querySelector(".search-form");
let searchBox = document.getElementById("search-box");
let searchLabel = document.querySelector("label[for='search-box']");

document.querySelector("#search-btn").onclick = () => {
    searchForm.classList.toggle("active");

    if (searchForm.classList.contains("active")) {
        searchBox.focus();
    }
};

$("#user-btn").click(function(){
    var userBox = $("#user-box");
    var displayValue = userBox.css("display");
    
    if(displayValue === "none") {
        userBox.css("display", "unset");
    } else {
        userBox.css("display", "none");
    }
});