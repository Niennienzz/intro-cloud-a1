var managerWelcomePageApp = new Vue({

    // select DOM element for Vue
    el: '#managerWelcomePageApp',

    // data to be kept in client memory
    data: {
        managerAuthAPI: '/auth',
        managerLoginAPI: '/manager_login',
    },

    // methods controlling the view
    methods: {

        checkLoginForm: function() {
            let self = this;
            let username = document.getElementById("managerLoginUsername").value;
            let password = document.getElementById("managerLoginPassword").value;
            if (username.length == 0 || password.length == 0) {
                swal(
                    "Oops...",
                    "Empty manager username or password, please try again.",
                    "error"
                );
                return;
            }
            let xhr = new XMLHttpRequest();
            xhr.open("POST", self.managerAuthAPI);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    access_token = jsonResponse.access_token;
                    self.redirectToHome(access_token);
                    return;
                }
                else if (xhr.readyState == 4 && xhr.status == 401) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    if (jsonResponse.description == "Invalid credentials") {
                        swal(
                            "Oops...",
                            "Invalid manager username or password, please try again.",
                            "error"
                        );
                        return;
                    }
                    return;
                }
            }.bind(xhr, this)
            xhr.send(JSON.stringify({username: username, password: password}));
            return;
        },

        redirectToHome: function(access_token) {
            let self = this;
            let xhr = new XMLHttpRequest();
            let formData = new FormData();
            formData.append("token", access_token);
            xhr.open("POST", self.managerLoginAPI);
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    let jsonResponse = JSON.parse(xhr.responseText);
                    swal(
                        "Success!",
                        "Redirecting to home page...",
                        "success"
                    ).then( function() {
                        window.location.href = jsonResponse.redirect;
                    });
                    return;
                }
            }
            xhr.send(formData);
            return
        }

    }

})