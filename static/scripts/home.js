var homePageApp = new Vue({

    // select DOM element for Vue
    el: '#homePageApp',

    // data to be keep in client memory
    data: {
        isInGallery: true,
        accessToken: '',
        picUrls: {}
    },

    // set up on creation values
    created: function() {
        let self = this;
        token = self.getUrlVars()["user_access"];
        if (token.length == 0) {
            alert("Invalid user access token, please log in again.");
            self.redirectToWelcome();
            return;
        }
        self.accessToken = token;
    },

    // methods controlling the view
    methods: {

        redirectToWelcome: function() {
            window.location.href = "http://127.0.0.1:5000/";
        },

        getUrlVars: function() {
            let results = [], hash;
            let hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                hash[1] = unescape(hash[1]);
                results.push(hash[0]);
                results[hash[0]] = hash[1];
            }
            return results;
        }

    }

})