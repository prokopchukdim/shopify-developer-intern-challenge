window.onload = function() {
    let editbutts = document.getElementsByClassName("edit");
    for (let but of editbutts){
        but.onclick = function(){
            let overlay = but.nextElementSibling;
            overlay.style.display = "block";
        }
    }
}