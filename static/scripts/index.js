var welcomePageApp = new Vue({

    // select DOM element for Vue
    el: '#welcomePageApp',

    // data to be keep in client memory
    data: {
        username: '',
        password: '',
        isOnRegisterTab: true,
        userRegisterAPI: '/user',
        userLoginUserAPI: '/auth'
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
            let self = this;
            let username = document.getElementById('registerUsername').value;
            let password = document.getElementById('registerPassword').value;
            if (username.length == 0 || password.length == 0) {
                alert("Empty username or password.");
                return;
            }
            let xhr = new XMLHttpRequest();
            xhr.open("POST", self.userRegisterAPI);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    alert("User created, please log in.");
                    return;
                }
                else if (xhr.readyState == 4 && xhr.status == 400) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    if (jsonResponse.message == "user already exists") {
                        alert("User already exists, please log in.");
                        return;
                    }
                    return;
                }
            }.bind(xhr, this)
            xhr.send(JSON.stringify({username: username, password: password}));
            return;
        },

        checkLoginForm: function() {
            let self = this;
            let username = document.getElementById('loginUsername').value;
            let password = document.getElementById('loginPassword').value;
            if (username.length == 0 || password.length == 0) {
                alert("Empty username or password.");
                return;
            }
            let xhr = new XMLHttpRequest();
            xhr.open("POST", self.userLoginUserAPI);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    alert("Redirecting to home page...");
                    let jsonResponse = JSON.parse(xhr.responseText);
                    access_token = jsonResponse.access_token;
                    self.redirectToHome(access_token);
                    return;
                }
                else if (xhr.readyState == 4 && xhr.status == 401) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    if (jsonResponse.description == "Invalid credentials") {
                        alert("Invalid username or password, please try again.");
                        return;
                    }
                    return;
                }
            }.bind(xhr, this)
            xhr.send(JSON.stringify({username: username, password: password}));
            return;
        },

        redirectToHome: function(access_token) {
            window.location.href = "http://127.0.0.1:5000/home?user_access=" + access_token;
        }
    }

})
