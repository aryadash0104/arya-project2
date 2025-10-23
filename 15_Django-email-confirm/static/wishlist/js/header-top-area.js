customElements.define('header-top-area', class AppDrawer extends HTMLElement {
  connectedCallback() {
    this.innerHTML = '<div class="header-top-area">\
            <div class="container">\
                <div class="row">\
                    <div class="col-lg-6 col-md-6 col-12">\
                       \
                        <!-- top-contact-info -->\
                        <div class="top-contact-info">\
                            <ul>\
                                <li><a href="#"><i class="zmdi zmdi-phone"></i> +44 (0)1453 836508‬ </a></li>\
                                <li><a href="contact.html"><i class="zmdi zmdi-email"></i> contact@theacornschool.com</a></li>\
                            </ul>\
                        </div><!--// top-contact-info -->\
                        \
                    </div>\
                    <div class="col-lg-6 col-md-6 col-12">\
                        <div class="top-info-right">\
                           \
                            <!-- top-social -->\
                            <div class="top-social">\
                                <ul>\
                                    <li><a href="https://www.facebook.com/TheAcornSchoolUK/"><i class="zmdi zmdi-facebook"></i></a></li>\
                                    <li><a href="https://twitter.com/theacornschool"><i class="zmdi zmdi-twitter"></i></a></li>\
                                    <li><a href="https://www.instagram.com/explore/locations/1018289358/the-acorn-school"><i class="zmdi zmdi-instagram"></i></a></li>\
                                </ul>\
                            </div><!--// top-social -->\
                            \
                            <!-- login-and-register -->\
                            <div class="login-and-register">\
                                <ul>\
                                    <li><a href="contact.html">Contact</a></li>\
                                </ul>\
                            </div><!--// login-and-register -->\
                            \
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>';
  }
});