var list = document.querySelectorAll(".cardtit")
var searchBar = document.getElementById("search");
searchBar.addEventListener('keyup', function (e) {
    var letter = e.target.value.toLowerCase();
    // console.log(letter);
    console.log(list);


});

//Wallet and User alert
function popup(postUserId, login) {
    if (login === postUserId) {
        alert("This is your post! ");
    }
    else {
        alert("Wallet Problem");
    }

}


function show() {
    var noti = document.getElementsByClassName("notification")[0].style.display = "block";;
    var side = document.getElementsByClassName("side")[0].style.display = "none";
    console.log("HI");
    noti.style.display = "block";
    side.style.display = "none";

}
function hide() {
    var noti = document.getElementsByClassName("notification")[0];
    var side = document.getElementsByClassName("side")[0];
    noti.style.display = "none";
    side.style.display = "block";

}


function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
function clk() {
    if(document.getElementById("pro").style.display === "none"){
        document.getElementById("pro").style.display = "block";
    }
    else{
        document.getElementById("pro").style.display = "none";
    }
}




