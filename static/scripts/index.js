function checkLoginForm() {

    // get element values
    let userName = document.getElementById('loginUsername').value;
    let password = document.getElementById('loginPassword').value;

    // simple validation
    if (userName.length == 0 || password.length == 0) {
        alert("Empty username or password.");
        return;
    }

    // send async request to create user
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/user");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("User created, redirecting to home page...");
        }
        else if (xhr.readyState == 4 && xhr.status == 400) {
            let jsonResponse = JSON.parse(xhr.responseText);
            if (jsonResponse.message == "user already exists") {
                alert("User already exists. Please log in.");
            }
        } else {
            alert("An error occurred.")
        }
    }
    xhr.send(JSON.stringify({username: userName, password: password}));

    return;

}