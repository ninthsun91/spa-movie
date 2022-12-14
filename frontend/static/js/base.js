$(function () {
  if (location.pathname === PATH_NAME.HOME) {
    document.cookie = "now=1"
    document.cookie = "trend=1"
    handleLoadHome();
  } else if (location.pathname === PATH_NAME.REV) {
    document.cookie = "popular=1"
    document.cookie = "trendrev=1"
    document.cookie = "recentrev=1"
    handleLoadRev();
  }
});
let last_known_scroll_position = 0;
let ticking = false;

function doSomething(scroll_pos) {
  if (scroll_pos < 90) {
    $("nav").css("height", "150px");
    $("#mainLogo").css("height", "100%");
    $("#mainLogo>*").css("opacity", "1");
    $("#subAppname").css("opacity", "0");
    $("#subAppname").css("z-index", "-1");
  } else {
    $("nav").css("height", "60px");
    $("#mainLogo").css("height", "0px");
    $("#mainLogo>*").css("opacity", "0");
    $("#subAppname").css("opacity", "1");
    $("#subAppname").css("z-index", "1");
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
