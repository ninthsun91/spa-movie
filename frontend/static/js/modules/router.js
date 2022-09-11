const loadPage = (pathname, complete = undefined) => {
  $("#App").load(`${pathname} #AppContainer`, complete);
};


const pushHistory = (pathname) => history.pushState({ pathname }, "", location.origin + pathname);
history.replaceState({ pathname: location.pathname }, "");
window.onpopstate = function ({ state }) {
  // console.log("onpopstate POPSTATE", state)
  switch (state.pathname) {
    case PATH_NAME.REV:
      return loadPage(PATH_NAME.REV, handleLoadRev);
    case PATH_NAME.HOME:
      return loadPage(PATH_NAME.HOME, handleLoadHome);
    case PATH_NAME.MY_PAGE:
      return loadPage(PATH_NAME.MY_PAGE, handleLoadMyPage);
  }
};


const reloadPage = (pathName, handler) => {
  const isAtTop = window.scrollY < 90;
  const isPathSame = location.pathname === pathName;
  if (isAtTop && isPathSame) {
  }
  if (!isAtTop && isPathSame) {
    window.scrollTo(0, 0);
  }
  if (isAtTop && !isPathSame) {
    pushHistory(pathName);
    loadPage(pathName, handler);
  }
  if (!isAtTop && !isPathSame) {
    window.scrollTo(0, 0);
    setTimeout(function () {
      pushHistory(pathName);
      loadPage(pathName, handler);
    }, 1000);
  }
};

//my page
const loadMyPage = () => {
  window.scrollTo(0, 0);
  if (location.pathname !== PATH_NAME.PROFILE) {
    setTimeout(function () {
      pushHistory(PATH_NAME.PROFILE);
      loadPage(PATH_NAME.PROFILE, handleLoadMyPage);
    }, 1000);
  }
};


const handleLoadMyPage = (responseText, textStatus, req) => {
  if (textStatus === "success") {
    // console.log("after load my page");
    setTitle(TITLE.MY_PAGE);
    $("#modalPlace").empty();
    $("#popupPlace").empty();
  } else if (textStatus === "error") {
    pushHistory(PATH_NAME.HOME);
    handler403Error("먼저 로그인을 해주세요")
  }
};


const handleLoadHome = () => {
  // console.log("after load home");

  setTitle(TITLE.HOME);
  loadComponent("movieListNow", "/components/postercard?direction=vertical&count=5&type=now");
  loadComponent("movieListTrending", "/components/postercard?direction=vertical&count=5&type=trend");
  $("#modalPlace").empty();
  $("#popupPlace").empty();
  numberIndicating = 0;
};


const handleLoadRev = function () {
  // console.log("after load rev");
  setTitle(TITLE.REV);
  loadComponent("recentReview", "/components/reviewcard?type=recent");
  loadComponent("popularReview", "/components/reviewcard?type=popular");
  $("#modalPlace").empty();
  $("#popupPlace").empty();
  setTimeout(function () {
    reviewMenuSlideUp();
    reviewContainerWidthGrow();
  }, 300);
};


const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, complete, () => console.log(`${tagId} loaded`));
};


const setTitle = function (title) {
  document.title = title + " | Movie Toy";
};
