const nav = document.querySelector("nav");
const footer = document.querySelector("footer");
const supportPageOffset = window.pageXOffset !== undefined;
const isCSS1Compat = (document.compatMode || "") === "CSS1Compat";

let previousScrollPosition = 0;

const isScrollingDown = () => {
    let scrolldPosition = supportPageOffset
        ? window.pageYOffset
        : isCSS1Compat
        ? document.documentElement.scrollTop
        : document.body.scrollTop;
    let isScrollingDown;

    if (scrolldPosition > previousScrollPosition) {
        isScrollingDown = true;
    } else {
        isScrollingDown = false
    }

    previousScrollPosition = scrolldPosition;

    return isScrollingDown;
};

const handleNavScroll = () => {
    if (isScrollingDown() && !nav.contains(document.activeElement)) {
        nav.classList.add("scroll-down");
        nav.classList.remove("scroll-up");
        footer.classList.add("scroll-down");
        footer.classList.remove("scroll-up");
    } else {
        nav.classList.add("scroll-up");
        nav.classList.remove("scroll-down");
        nav.classList.add("scroll-up");
        nav.classList.remove("scroll-down");
    }
};

var throttleTimer;

const throttle = (callback, time) => {
    if (throttleTimer) return;

    throttleTimer = true;
    setTimeout(() => {
        callback();
        throttleTimer = false
    }, time);
};

const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

window.addEventListener("scroll", () => {
    if (mediaQuery && !mediaQuery.matches) {
        throttle(handleNavScroll, 200);
    }
});