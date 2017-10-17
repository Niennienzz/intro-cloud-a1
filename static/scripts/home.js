var homePageApp = new Vue({

    // select DOM element for Vue
    el: '#homePageApp',

    // both Flask and Vue use {{..}} by default
    delimiters: ['${', '}'],

    // data to be kept in client memory
    data: {
        isInGallery: true,
        imageURLListAPI: '/api/pics',
        imageContentAPI: '/api/image/',
        accessToken: '',
        picUrls: {},
        thumbnailURLList: []
    },

    // set up on creation values
    created: function() {

        // set access token
        let self = this;
        token = self.getURLParams()["user_access"];
        if (token.length == 0) {
            alert("Invalid user access token, please log in again.");
            self.redirectToWelcome();
            return;
        }
        self.accessToken = token;

        // request image urls associated with current user
        let xhr = new XMLHttpRequest();
        xhr.open("GET", self.imageURLListAPI)
        xhr.setRequestHeader("Authorization", "JWT " + self.accessToken);
        xhr.onreadystatechange = function(vm) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let jsonResponse = JSON.parse(xhr.responseText);
                self.picUrls = jsonResponse;
                return;
            }
            else if (xhr.readyState == 4 && xhr.status == 401) {
                alert("Invalid user access token, please log in again.");
                self.redirectToWelcome();
                return;
            }
        }.bind(xhr, this)
        xhr.send();
        return;
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
            window.location.href = "http://127.0.0.1:5000/";
        }

    },

    // watched properties
    watch: {

        picUrls: function(val) {
            let self = this;
            let results = [];
            let len =  val.pic_urls.length;
            for (let i = 0; i < len; i++) {
                results.push(val.pic_urls[i].thumb_url);
            }
            self.thumbnailURLList = results;
        }

    }

})