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
            "async": true,
            "crossDomain": true,
            "url": self.managerListAPI,
            "method": "GET",
            "headers": {
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

        refreshStatistics: function() {
            let self = this;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": self.managerListAPI,
                "method": "GET",
                "headers": {
                    "authorization": "JWT " + self.accessToken
                }
            }
            $.ajax(settings).done(function (response) {
                self.workerPool = response;
            });
        }

    },

    mounted: function () {
        setInterval(function () {
            this.refreshStatistics();
        }.bind(this), 5000);
    }

})