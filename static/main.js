let searchForm = document.querySelector(".search-form");
let searchBox = document.getElementById("search-box");
let searchLabel = document.querySelector("label[for='search-box']");

document.querySelector("#search-btn").onclick = () => {
    searchForm.classList.toggle("active");

    if (searchForm.classList.contains("active")) {
        searchBox.focus();
    }
};