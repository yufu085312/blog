(function () {
  const header = document.getElementById("main-header");
  if (!header) return;

  let lastScrollTop = 0;
  const delta = 5;
  const headerHeight = header.offsetHeight;

  window.addEventListener("scroll", function () {
    const st = window.pageYOffset || document.documentElement.scrollTop;

    // Make sure they scroll more than delta
    if (Math.abs(lastScrollTop - st) <= delta) return;

    // If they scrolled down and are past the header, add class .header-hidden to hide the nav
    if (st > lastScrollTop && st > headerHeight) {
      header.classList.add("header-hidden");
    } else {
      // Scroll Up
      header.classList.remove("header-hidden");
    }

    lastScrollTop = st;
  });
})();
