document.addEventListener("DOMContentLoaded", function () {

    createSidebar();
    createTopbar();

    setupUploads();
    setupTheme();
    setupNavigation();

});


/* =====================================
   SIDEBAR
===================================== */

function createSidebar() {

    const currentPage =
        window.location.pathname
            .split("/")
            .pop()
            .replace(".html", "") || "dashboard";

    const sidebar = document.createElement("aside");

    sidebar.className = "sidebar";
    sidebar.id = "sidebar";

    sidebar.innerHTML = `


        <div class="brand">
            StyleSense AI
        </div>

        <nav class="nav-menu">

            <a href="{% url 'dashboard' %}"
               class="nav-link ${currentPage === "dashboard" ? "active" : ""}">
                <i class="bi bi-grid-1x2"></i>
                Dashboard
            </a>

            <a href="{% url 'skinanalysis' %}"
               class="nav-link ${currentPage === "skin-analysis" ? "active" : ""}">
                <i class="bi bi-camera"></i>
                Skin Analysis
            </a>

            <a href="{% url 'virtualtryon' %}"
               class="nav-link ${currentPage === "virtual-try-on" ? "active" : ""}">
                <i class="bi bi-tshirt"></i>
                Virtual Try-On
            </a>

            <a href="{% url 'aistylist' %}"
               class="nav-link ${currentPage === "ai-stylist" ? "active" : ""}">
                <i class="bi bi-stars"></i>
                AI Stylist
            </a>

            <a href="{% url 'wardrobe' %}"
               class="nav-link ${currentPage === "wardrobe" ? "active" : ""}">
                <i class="bi bi-book"></i>
                Wardrobe
            </a>

            <a href="{% url 'history' %}"
               class="nav-link ${currentPage === "history" ? "active" : ""}">
                <i class="bi bi-clock-history"></i>
                History
            </a>

            <a href="{% url 'profile' %}"
               class="nav-link ${currentPage === "profile" ? "active" : ""}">
                <i class="bi bi-person"></i>
                Profile
            </a>

            <a href="{% url 'settings' %}"
               class="nav-link ${currentPage === "settings" ? "active" : ""}">
                <i class="bi bi-gear"></i>
                Settings
            </a>

        </nav>

        <div class="sidebar-bottom">
            <div class="n-avatar">
                N
            </div>
        </div>
    `;

    document.body.prepend(sidebar);
}


/* =====================================
   TOPBAR
===================================== */

function createTopbar() {

    const main = document.querySelector(".main");

    if (!main) return;

    const topbar = document.createElement("header");

    topbar.className = "topbar";

    topbar.innerHTML = `

        <button
            class="mobile-toggle"
            onclick="toggleSidebar()">

            <i class="bi bi-list"></i>

        </button>

        <div class="topbar-user">
            Hello, Jaiko Gouda 👋
        </div>

        <div class="user-avatar">
            J
        </div>

        <button
            class="logout-btn"
            onclick="logout()">

            Logout

        </button>
    `;

    main.prepend(topbar);
}


/* =====================================
   SIDEBAR MOBILE
===================================== */

function toggleSidebar() {

    const sidebar =
        document.getElementById("sidebar");

    sidebar.classList.toggle("show");
}


/* =====================================
   LOGOUT
===================================== */

function logout() {

    alert("Logout clicked.");

}


/* =====================================
   FILE UPLOAD
===================================== */

function setupUploads() {

    const inputs =
        document.querySelectorAll(
            'input[type="file"]'
        );

    inputs.forEach(input => {

        input.addEventListener(
            "change",
            function () {

                const file = this.files[0];

                if (!file) return;

                const previewId =
                    this.dataset.preview;

                if (!previewId) return;

                const preview =
                    document.getElementById(
                        previewId
                    );

                if (!preview) return;

                const reader =
                    new FileReader();

                reader.onload = function (e) {

                    preview.src =
                        e.target.result;

                    preview.classList.remove(
                        "d-none"
                    );
                };

                reader.readAsDataURL(file);
            }
        );

    });

}


/* =====================================
   THEME
===================================== */

function setupTheme() {

    const light =
        document.getElementById("themeLight");

    const dark =
        document.getElementById("themeDark");

    if (light) {

        light.addEventListener(
            "click",
            function () {

                document.body.style.background =
                    "#ffffff";

                document.body.style.color =
                    "#111111";
            }
        );
    }

    if (dark) {

        dark.addEventListener(
            "click",
            function () {

                document.body.style.background =
                    "#111111";

                document.body.style.color =
                    "#ffffff";
            }
        );
    }

}


/* =====================================
   NAVIGATION
===================================== */

function setupNavigation() {

    document
        .querySelectorAll(".nav-link")
        .forEach(link => {

            link.addEventListener(
                "click",
                function () {

                    const sidebar =
                        document.getElementById(
                            "sidebar"
                        );

                    if (sidebar) {
                        sidebar.classList.remove(
                            "show"
                        );
                    }

                }
            );

        });

}


/* =====================================
   AI STYLIST
===================================== */

function sendStylistMessage() {

    const input =
        document.getElementById(
            "stylistInput"
        );

    const chat =
        document.getElementById(
            "chatMessages"
        );

    if (!input || !chat) return;

    const message =
        input.value.trim();

    if (!message) return;

    chat.innerHTML += `

        <div class="chat-message chat-user">
            ${message}
        </div>

    `;

    input.value = "";

    setTimeout(function () {

        chat.innerHTML += `

            <div class="chat-message chat-ai">

                Based on your wardrobe, skin tone
                and style preferences, I recommend
                a smart-casual outfit with neutral
                colors.

                <br><br>

                <strong>
                    White Linen Shirt +
                    Navy Chinos +
                    White Sneakers
                </strong>

            </div>

        `;

        chat.scrollTop =
            chat.scrollHeight;

    }, 700);

}


/* =====================================
   TRY ON
===================================== */

function generateTryOn() {

    const result =
        document.getElementById(
            "tryOnResult"
        );

    if (!result) return;

    result.innerHTML = `

        <div class="text-center">

            <div class="spinner-border text-primary mb-3">
            </div>

            <h5>
                AI is generating your
                virtual try-on...
            </h5>

            <p class="text-muted">
                Detecting body pose,
                matching clothing and
                rendering final image.
            </p>

        </div>

    `;

    setTimeout(function () {

        result.innerHTML = `

            <div class="text-center">

                <div class="product-image"
                     style="height:300px">

                    AI Generated Look

                </div>

                <h4 class="mt-3">
                    Outfit Match Score: 96%
                </h4>

            </div>

        `;

    }, 2000);

}


/* =====================================
   WARDROBE SEARCH
===================================== */

function searchWardrobe() {

    const input =
        document.getElementById(
            "wardrobeSearch"
        );

    const cards =
        document.querySelectorAll(
            ".wardrobe-item"
        );

    if (!input) return;

    const value =
        input.value.toLowerCase();

    cards.forEach(card => {

        const text =
            card.innerText.toLowerCase();

        if (text.includes(value)) {

            card.style.display = "";

        } else {

            card.style.display = "none";

        }

    });

}


/* =====================================
   SETTINGS TOAST
===================================== */

function saveSettings() {

    alert(
        "Your StyleSense AI settings have been saved."
    );

}



