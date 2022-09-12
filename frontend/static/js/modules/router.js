const loadPage = (pathname, complete = undefined) => {
  if (pathname === "/") {
    document.cookie = "now=1";
    document.cookie = "trend=1";
  }
  if (pathname === "/rev") {
    document.cookie = "popular=1";
    document.cookie = "trendrev=1";
    document.cookie = "recentrev=1";
  }
  $("#App").load(`${pathname} #AppContainer`, complete);
};

const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, (complete = complete));
  console.log(complete);
  console.log(complete === undefined);
  if (complete === undefined) {
    console.log(`${tagId} loaded`);
  }
};

const setTitle = function (title) {
  document.title = title + " | Movie Toy";
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
    case PATH_NAME.PROFILE:
      return loadPage(PATH_NAME.PROFILE, handleLoadMyPage);
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
    handler403Error("먼저 로그인을 해주세요");
  }
};

const handleLoadHome = () => {
  // console.log("after load home");
  setTitle(TITLE.HOME);
  loadComponent(
    "movieListNow", 
    "/components/postercard?" +
    "direction=vertical" +
    "&query=now" +
    "&chevron=on" +
    "&is_home=yes"
    );
  loadComponent(
    "movieListTrending",
    "/components/postercard" + 
    "?direction=vertical" + 
    "&query=trend" + 
    "&chevron=on" + 
    "&is_home=yes"
  );
  $("#modalPlace").empty();
  $("#popupPlace").empty();

  numberIndicating = 0;
};

const handleLoadRev = function () {
  // console.log("after load rev");
  setTitle(TITLE.REV);
  $("#modalPlace").empty();
  $("#popupPlace").empty();
  setTimeout(function () {
    reviewMenuSlideUp();
    reviewContainerWidthGrow();
  }, 300);
};
