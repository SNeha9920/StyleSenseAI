{% load static %}

/* =====================================================
   STYLESENSE AI - FRONTEND JAVASCRIPT
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* =================================================
       SMOOTH SCROLL
    ================================================= */

    const links = document.querySelectorAll(
        'a[href^="#"]'
    );

    links.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId =
                this.getAttribute("href");

            if (targetId === "#") {
                return;
            }

            const target =
                document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    /* =================================================
       REGISTER
    ================================================= */

    const registerForm =
        document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const name =
                    document.getElementById(
                        "fullName"
                    ).value.trim();


                const email =
                    document.getElementById(
                        "registerEmail"
                    ).value.trim();


                const password =
                    document.getElementById(
                        "registerPassword"
                    ).value;


                const message =
                    document.getElementById(
                        "registerMessage"
                    );


                /* Validate name */

                if (name === "") {

                    showMessage(
                        message,
                        "Please enter your full name.",
                        "danger"
                    );

                    return;
                }


                /* Validate email */

                if (!validateEmail(email)) {

                    showMessage(
                        message,
                        "Please enter a valid email address.",
                        "danger"
                    );

                    return;
                }


                /* Validate password */

                if (password.length < 6) {

                    showMessage(
                        message,
                        "Password must contain at least 6 characters.",
                        "danger"
                    );

                    return;
                }


                /*
                   FRONTEND DEMO ONLY

                   Later this will become:

                   fetch("/api/register/", {
                       method: "POST",
                       ...
                   })
                */

                localStorage.setItem(
                    "stylesenseUser",
                    JSON.stringify({
                        name: name,
                        email: email
                    })
                );


                showMessage(
                    message,
                    "Account created successfully!",
                    "success"
                );


                setTimeout(function () {

                    window.location.href =
                        "login.html";

                }, 1000);

            }
        );

    }


    /* =================================================
       LOGIN
    ================================================= */

    const loginForm =
        document.getElementById("loginForm");


    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const email =
                    document.getElementById(
                        "loginEmail"
                    ).value.trim();


                const password =
                    document.getElementById(
                        "loginPassword"
                    ).value;


                const message =
                    document.getElementById(
                        "loginMessage"
                    );


                if (!validateEmail(email)) {

                    showMessage(
                        message,
                        "Please enter a valid email address.",
                        "danger"
                    );

                    return;
                }


                if (password === "") {

                    showMessage(
                        message,
                        "Please enter your password.",
                        "danger"
                    );

                    return;
                }


                /*
                   FRONTEND DEMO LOGIN

                   Later connect this to Django:

                   fetch("/api/login/", {
                       method: "POST",
                       ...
                   })
                */

                localStorage.setItem(
                    "stylesenseLoggedIn",
                    "true"
                );


                showMessage(
                    message,
                    "Login successful!",
                    "success"
                );


                setTimeout(function () {

                    window.location.href =
                        "{% url 'dashboard' %}";

                }, 800);

            }
        );

    }


    /* =================================================
       CHECK LOGIN STATE
    ================================================= */

    const protectedLinks =
        document.querySelectorAll(
            ".protected-link"
        );


    protectedLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const loggedIn =
                    localStorage.getItem(
                        "stylesenseLoggedIn"
                    );


                if (loggedIn !== "true") {

                    event.preventDefault();

                    window.location.href =
                        "login.html";

                }

            }
        );

    });

});


/* =====================================================
   EMAIL VALIDATION
===================================================== */

function validateEmail(email) {

    const pattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);

}


/* =====================================================
   SHOW MESSAGE
===================================================== */

function showMessage(
    element,
    text,
    type
) {

    if (!element) {
        return;
    }


    element.innerHTML = `
        <div class="alert alert-${type} py-2 small">
            ${text}
        </div>
    `;

}