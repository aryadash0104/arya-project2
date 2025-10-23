customElements.define('footer-area', class Footer extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<!-- Footer Area -->\
    <footer class="footer-area">\
       \
        <!-- Footer Top Area -->\
        <div class="footer-top section-pb section-pt-60">\
            <div class="container">\
                <div class="row">\
\
                    <div class="col-lg-5 col-md-6 mt--60">\
                        <div class="footer-single-block">\
                            <p  class="footer-dec">The Acorn School Educational Trust Ltd<br>\
			    Church St, Nailsworth, Stroud GL6 0BP, UK<br>\
			    Registered Charity: 1204957</p>\
                            <ul class="footer-social-link">\
                                <li><a href="https://www.facebook.com/TheAcornSchoolUK/" target="_blank" rel="noopener noreferrer"><i class="zmdi zmdi-facebook"></i></a></li>\
                                <li><a href="https://twitter.com/theacornschool" target="_blank" rel="noopener noreferrer"><i class="zmdi zmdi-twitter"></i></a></li>\
                                <li><a href="https://www.instagram.com/explore/locations/1018289358/the-acorn-school" target="_blank" rel="noopener noreferrer"><i class="zmdi zmdi-instagram"></i></a></li>\
                            </ul>\
                        </div>\
                    </div>\
\
                    <div class="col-lg-3 col-md-6 mt--60">\
                        <div class="footer-block">\
                            <h5>Links</h5>\
                            <ul class="footer-courses">\
                                <li>    \
                                    <div class="courses-image">\
                                        <a href="http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/115808" target="_blank" rel="noopener noreferrer"><img src="assets/images/other/ofsted.png" alt=""></a>\
                                    </div>\
                                    <div class="courses-nifo">\
                                        <h5><a href="http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/115808" target="_blank" rel="noopener noreferrer">Ofsted</a></h5>\
                                        <p>Reports</p>\
                                    </div>\
                                </li>\
                                <li>   \
                                    <div class="courses-image">\
                                        <a href="http://www.acornoverseas.org" target="_blank" rel="noopener noreferrer"><img src="assets/images/other/acornover.png" alt=""></a>\
                                    </div>\
                                    <div class="courses-nifo">\
                                        <h5><a href="http://www.acornoverseas.org" target="_blank" rel="noopener noreferrer">Acorn Overseas</a></h5>\
                                        <p>registered charity</p>\
                                    </div>\
                                </li>\
                            </ul>\
                        </div>\
                    </div>\
\
                    <div class="col-lg-4 col-md-6 mt--60">\
                        <div class="footer-block">\
                            <h5>Prospectus</h5>\
                            <div class="newsletter-wrap">\
                                <p>Please contact us for more information and a prospectus.</p>\
				<div class="slider-text-info"style="padding-left: 10px;">\
                                    <a href="contact.html" class="btn slider-btn uppercase"><span>Contact Us</span></a>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
\
                </div>\
            </div>\
        </div><!--// Footer Top Area -->\
        \
        <!-- Footer-bottom Area -->\
        <div class="footer-bottom">\
            <div class="container">\
                <div class="row">\
                    <div class="col-lg-12">\
                        <div class="copy-right pt--10 pb--10 text-center text-white">\
                            <p>Copyright&#169; 2024 <span>The Acorn School</span></p>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div><!--// Footer-botton Area -->\
\
    </footer>\
    <!--// Footer Area -->`;
  }
});