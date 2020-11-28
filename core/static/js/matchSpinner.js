function showPage() {
    var spinner = document.getElementById("spinner");
    var content = document.getElementsByClassName("container")[0];
    spinner.style.display = "none";
    content.style.display = "block";
}

window.onload = (event) => {
    console.log("hello!");
    setTimeout(showPage, 3000);
}