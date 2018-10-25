const regLink = "http://edi.iem.pw.edu.pl/chaberb/register/check/";

init();

function init(){
    var login = document.getElementsByName("login")[0];
    var pesel = document.getElementsByName("pesel")[0];
    var password = document.getElementsByName("password")[0];
    var repeat_password = document.getElementsByName("repeat-password")[0];
    var myForm = document.getElementsByName("my-form")[0];

    login.addEventListener("change", checkLogin, false);
    pesel.addEventListener("change", setGenderByPesel, false);
    password.addEventListener("input", checkPass, false);
    repeat_password.addEventListener("change", checkPass, false);
    myForm.addEventListener("submit", checkSubmit, false);
}

function checkLogin(){
    var loginInput = document.getElementsByName("login")[0].value;
    var regUrl = regLink + loginInput;

    fetch(regUrl)
    .then(response => {response.json()
    .then(data => loginResponseHandle(data,loginInput) )});
}

function setGenderByPesel(){
    var pesel = document.getElementsByName("pesel")[0].value.toString();

    if( ["0", "2", "4", "6", "8"].includes(pesel[9]) ){
        var female = document.getElementsByName("female")[0];
        female.click();
    } else {
        var male = document.getElementsByName("male")[0];
        male.click();
    }
}

function checkPass(){
    var pass = document.getElementsByName("password")[0].value;
    var pass2 = document.getElementsByName("repeat-password")[0].value;

    var status = getStatusDiv("repeat-password-li","repeat-password-status");
    var match = pass === pass2;

    setStatus(status, match );
    return match;
}

function loginResponseHandle(data,login){
    var json = data;

    var div = getStatusDiv("login-li","login-status");
    var free = !json[login];
    setStatus(div, free);

    return free;
}

function getStatusDiv(liId, id) {
    var div = document.getElementById(id);

    if (div == null) {
        const loginLi = document.getElementById(liId);
        div = document.createElement('div');
        div.id = id;
        div.classList.add("input-status");
        loginLi.appendChild(div);
    }

    return div;
}

function setStatus(div, value){
    var cls = div.classList;

    if( value ){
        div.innerText = "OK!"
    } else {
        cls.add("invalid-input");
        div.innerText = "NIE OK!";
    }
}