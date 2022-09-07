$(function () {
  if (location.pathname === PATH_NAME.HOME) {
    handleLoadHome();
  } else if (location.pathname === PATH_NAME.HOME) {
    handleLoadRev;
  }
});
let last_known_scroll_position = 0;
let ticking = false;

function doSomething(scroll_pos) {
  if (scroll_pos === 0) {
    $("nav").css("height", "150px");
    $("#logo").css("height", "100%");
    $("#logo>*").css("opacity", "1");
  } else {
    $("nav").css("height", "60px");
    $("#logo").css("height", "0");
    $("#logo>*").css("opacity", "0");
  }
  console.log("scroll");
}

window.addEventListener("scroll", function (e) {
  last_known_scroll_position = window.scrollY;

  if (!ticking) {
    window.requestAnimationFrame(function () {
      doSomething(last_known_scroll_position);
      ticking = false;
    });

    ticking = true;
  }
});
