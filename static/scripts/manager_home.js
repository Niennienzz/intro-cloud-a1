var managerHomeApp = new Vue({

    // select DOM element for Vue
    el: '#managerHomePageApp',

    // both Flask and Vue use {{..}} by default
    delimiters: ['${', '}'],

    // data to be kept in client memory
    data: {
        isInGallery: true,
        managerLogoutAPI: '/manager_logout',
        managerListAPI: '/api/manager_list',
        managerManualAPI: '/api/manager_manual',
        managerDataAPI: '/api/manager_data',
        accessToken: '',
        workerPool: [],
    },

    // set up on creation values
    created: function() {

        // set access token
        let self = this;
        token = self.getURLParams()["token"];
        if (token.length == 0) {
            swal(
                "Oops...",
                "Invalid user access token, please log in again.",
                "error"
            ).then( function() {
                window.location.href = "/";
            });
            return;
        }
        self.accessToken = token;

        // request worker pool
        let settings = {
            async: true,
            crossDomain: true,
            url: self.managerListAPI,
            method: "GET",
            headers: {
                "authorization": "JWT " + self.accessToken
            }
        }
        $.ajax(settings).done(function (response) {
            self.workerPool = response;
        });
    },

    // methods controlling the view
    methods: {

        // general get url parameter method, referenced from:
        // https://gist.github.com/kaioe/8401201
        getURLParams: function() {
            let results = [], hash;
            let hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                hash[1] = unescape(hash[1]);
                results.push(hash[0]);
                results[hash[0]] = hash[1];
            }
            return results;
        },

        refreshStatistics: function() {
            let self = this;
            let settings = {
                async: true,
                crossDomain: true,
                url: self.managerListAPI,
                method: "GET",
                headers: {
                    "authorization": "JWT " + self.accessToken
                }
            }
            $.ajax(settings).done(function (response) {
                self.workerPool = response;
            });
        },

        activateWorker: function() {
            let self = this;
            swal({
                title: 'Are you sure?',
                text: "You are about to activate a worker.",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, Activate!'
            }).then(function () {
                let settings = {
                    async: true,
                    crossDomain: true,
                    url: self.managerManualAPI,
                    method: "POST",
                    headers: {
                        "content-type": "application/json",
                        "authorization": "JWT " + self.accessToken
                    },
                    processData: false,
                    data: '{"action": "grow"}'
                };
                $.ajax(settings)
                    .done(function (response) {
                        swal(
                            "Success!",
                            "Worker activated.",
                            "success"
                        )
                        console.log(response);
                    })
                    .fail(function () {
                        swal(
                            "Oops...",
                            "Worker failed to activate.",
                            "error"
                        )
                        console.log(response);
                    });
            })
        },

        deactivateWorker: function(instance) {
            let self = this;
            swal({
                title: 'Are you sure?',
                text: "You are about to deactivate a worker.",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, Deactivate!'
            }).then(function () {
                let settings = {
                    async: true,
                    crossDomain: true,
                    url: self.managerManualAPI,
                    method: "POST",
                    headers: {
                        "content-type": "application/json",
                        "authorization": "JWT " + self.accessToken
                    },
                    processData: false,
                    data: '{"action": "shrink", "instance": "' + instance + '"}'
                };
                $.ajax(settings)
                    .done(function (response) {
                        swal(
                            "Success!",
                            "Worker deactivated.",
                            "success"
                        )
                        console.log(response);
                    })
                    .fail(function () {
                        swal(
                            "Oops...",
                            "Worker failed to deactivate.",
                            "error"
                        )
                        console.log(response);
                    });
            })
        },

        purgeUserData: function() {
            let self = this;
            swal({
                title: 'Are you sure?',
                text: "You are about to purge all user data.",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, Purge!'
            }).then(function () {
                let settings = {
                    async: true,
                    crossDomain: true,
                    url: self.managerDataAPI,
                    method: "DELETE",
                    headers: {
                        "authorization": "JWT " + self.accessToken
                    },
                    processData: false
                };
                $.ajax(settings)
                    .done(function (response) {
                        swal(
                            "Success!",
                            "User data purged.",
                            "success"
                        )
                        console.log(response);
                    })
                    .fail(function () {
                        swal(
                            "Oops...",
                            "Failed to purge user data.",
                            "error"
                        )
                        console.log(response);
                    });
            })

        },

        redirectToWelcome: function() {
            let self = this;
            let xhr = new XMLHttpRequest();
            xhr.open("GET", self.managerLogoutAPI);
            xhr.onreadystatechange = function(vm) {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    swal(
                        "Goodbye!",
                        "You are now logged out.",
                        "success"
                    ).then( function() {
                        window.location.href = "/";
                    });
                    return;
                }
            }
            xhr.send();
            return
        },

    },

    // refresh statistics every 5 seconds
    mounted: function () {
        setInterval(function () {
            this.refreshStatistics();
        }.bind(this), 5000);
    }

})