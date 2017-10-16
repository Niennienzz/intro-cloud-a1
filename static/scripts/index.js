var welcomePageApp = new Vue({

    // select DOM element for Vue
    el: '#welcomePageApp',

    // data to be keep in client memory
    data: {
        username: '',
        password: '',
        isOnRegisterTab: true,
        userRegisterURL: '/user',
        userLoginUserURL: '/auth'
    },

    // methods controlling the view
    methods: {

        switchToRegisterTab: function() {
            this.isOnRegisterTab = true;
            document.getElementById("switchToRegisterButton").disabled = this.isOnRegisterTab;
            document.getElementById("switchToLoginButton").disabled = !this.isOnRegisterTab;
        },

        switchToLoginTab: function() {
            this.isOnRegisterTab = false;
            document.getElementById("switchToRegisterButton").disabled = this.isOnRegisterTab;
            document.getElementById("switchToLoginButton").disabled = !this.isOnRegisterTab;
        },

        checkRegisterForm: function(type) {
            let username = document.getElementById('registerUsername').value;
            let password = document.getElementById('registerPassword').value;
            if (username.length == 0 || password.length == 0) {
                alert("Empty username or password.");
                return;
            }
            let xhr = new XMLHttpRequest();
            xhr.open("POST", this.userRegisterURL);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    alert("User created, redirecting to home page...");
                }
                else if (xhr.readyState == 4 && xhr.status == 400) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    if (jsonResponse.message == "user already exists") {
                        alert("User already exists, redirecting to home page...");
                    }
                    return;
                }
            }.bind(xhr, this)
            xhr.send(JSON.stringify({username: username, password: password}));
            return;
        },

        checkLoginForm: function() {
            let username = document.getElementById('loginUsername').value;
            let password = document.getElementById('loginPassword').value;
            if (username.length == 0 || password.length == 0) {
                alert("Empty username or password.");
                return;
            }
            let xhr = new XMLHttpRequest();
            xhr.open("POST", this.userLoginUserURL);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    alert("Redirecting to home page...");
                }
                else if (xhr.readyState == 4 && xhr.status == 401) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    if (jsonResponse.description == "Invalid credentials") {
                        alert("Invalid username or password.");
                    }
                    return;
                }
            }.bind(xhr, this)
            xhr.send(JSON.stringify({username: username, password: password}));
            return;
        }
    }

})

