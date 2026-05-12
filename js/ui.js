(() => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const enhanceNavigation = () => {
        document.querySelectorAll(".site-header").forEach((header) => {
            const nav = header.querySelector(".site-nav");
            if (!nav || header.querySelector(".menu-toggle")) {
                return;
            }

            const button = document.createElement("button");
            button.className = "menu-toggle";
            button.type = "button";
            button.setAttribute("aria-label", "メニューを開閉");
            button.setAttribute("aria-expanded", "false");
            button.innerHTML = "<span></span><span></span>";

            header.classList.add("has-menu-toggle");
            header.insertBefore(button, nav);

            button.addEventListener("click", () => {
                const isOpen = header.classList.toggle("is-open");
                button.setAttribute("aria-expanded", String(isOpen));
            });

            nav.querySelectorAll("a").forEach((link) => {
                link.addEventListener("click", () => {
                    header.classList.remove("is-open");
                    button.setAttribute("aria-expanded", "false");
                });
            });
        });
    };

    const enhanceReveal = () => {
        const targets = document.querySelectorAll([
            ".hero-copy",
            ".hero-visual",
            ".portfolio-section",
            ".portfolio-list li",
            ".course-hero",
            ".work-group",
            ".article-frame > *",
            ".article-frame img",
            ".article-frame iframe",
            ".article-frame .card"
        ].join(","));

        targets.forEach((target, index) => {
            target.classList.add("reveal-item");
            target.style.setProperty("--reveal-delay", `${Math.min(index * 45, 360)}ms`);
        });

        if (reduceMotion || !("IntersectionObserver" in window)) {
            targets.forEach((target) => target.classList.add("is-visible"));
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: "0px 0px -12% 0px",
            threshold: 0.12
        });

        targets.forEach((target) => observer.observe(target));
    };

    const enhancePressFeedback = () => {
        const controls = document.querySelectorAll([
            ".primary-link",
            ".portfolio-list a",
            ".work-list a",
            ".article-file-link",
            ".site-nav a",
            ".article-frame a"
        ].join(","));

        controls.forEach((control) => {
            control.addEventListener("pointerdown", () => {
                control.classList.add("is-pressing");
            });
            ["pointerup", "pointercancel", "pointerleave", "blur"].forEach((eventName) => {
                control.addEventListener(eventName, () => {
                    control.classList.remove("is-pressing");
                });
            });
        });
    };

    document.documentElement.classList.add("js-enabled");
    enhanceNavigation();
    enhanceReveal();
    enhancePressFeedback();
})();
