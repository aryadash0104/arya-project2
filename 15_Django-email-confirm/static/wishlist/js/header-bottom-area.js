customElements.define('header-bottom-area', class HeaderBottom extends HTMLElement {
  connectedCallback() {
    this.innerHTML = ' <div class="header-bottom-area header-sticky header-sticky">\
            <div class="container">\
                <div class="row">\
                   \
                    <div class="col-lg-3 col-md-5 col-6">\
                        \
                        <!-- logo-area -->\
                        <div style="margin-top: 10px;margin-bottom: 10px;">\
			    <img src="assets/images/logo/acorn_logo_graduated.png" alt="">\
                        </div><!--// logo-area -->\
                        \
                    </div>\
                    \
                    <div class="col-lg-9 col-md-7 col-6">\
                        \
                        <div class="header-bottom-right">\
                            <!-- main-menu -->\
                            <div class="main-menu">\
                                <nav class="main-navigation">\
                                    <ul>\
                                        <li class="active"><a href="index.html"> HOME</a>\
                                            <ul class="sub-menu">\
						<li><a href="policy/OFSTED Report - The Acorn School May 2023.pdf">Ofsted 2023 Report</a></li>\
                                            </ul>\
                                        </li>\
                                        <li><a href="about.html">SCHOOL LIFE</a>\
                                            <ul class="sub-menu">\
                                                <li><a href="about.html">Welcome</a></li>\
						<li><a href="about.html#opendays">Open Days</a></li>\
						<li><a href="about.html#events">Events</a></li>\
						<li><a href="schoolLife.html#termtimes">Term Times</a></li>\
						<li><a href="fees.html">Fees & Bursary</a></li>\
						<li><a href="outdoors.html">Outdoors</a></li>\
                                                <li><a href="policies.html">Policies & Press Releases</a></li>\
                                            </ul>\
                                        </li>\
                                        <li><a href="gallery.html">GALLERY</a>\
                                        </li>\
                                        <li><a href="vacancies.html">VACANCIES</a>\
                                        </li>\
                                        <li><a href="contact.html">CONTACT</a></li>\
                                    </ul>\
                                </nav>\
                            </div><!--// main-menu -->\
\
                            <div style="float:right;margin-top: 5px;margin-right: 5px;"><img style="height:60px" src="assets/images/logo/Ofsted.png"</div>\
                        </div>\
                    </div>\
                    \
		    \
                     <div class="col">\
                        <!-- mobile-menu start -->\
                        <div class="mobile-menu d-block d-lg-none"></div>\
                        <!-- mobile-menu end -->\
                    </div>\
                    \
                </div>\
            </div>\
        </div>';
  }
});