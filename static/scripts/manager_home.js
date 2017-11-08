var managerHomeApp = new Vue({

    // select DOM element for Vue
    el: '#managerHomePageApp',

    // data to be kept in client memory
    data: {
        isInGallery: true,
        managerLogoutAPI: '/manager_logout',
        accessToken: '',
    },

    // methods controlling the view
    methods: {

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

    }

})