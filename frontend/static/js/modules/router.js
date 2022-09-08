const loadPage = (pathname, complete = undefined) => {
  $("#App").load(`${pathname} #AppContainer`, complete);
};

const pushHistory = (pathname) => history.pushState({ pathname }, "", location.origin + pathname);
history.replaceState({ pathname: location.pathname }, "");
window.onpopstate = function ({ state }) {
  switch (state.pathname) {
    case PATH_NAME.REV:
      return loadPage(PATH_NAME.REV);
    case PATH_NAME.HOME:
      return loadPage(PATH_NAME.HOME);
  }
};

const reloadPage = function (pathName, handler) {
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
const loadMyPage = function () {
   window.scrollTo(0, 0);
     if (location.pathname === PATH_NAME.PROFILE) {
  } else {
    setTimeout(function () {
      pushHistory(PATH_NAME.PROFILE);
      loadPage(PATH_NAME.PROFILE, handleLoadHome);
    }, 1000);
  }
}

const handleLoadHome = function () {
  console.log("after load home");

  setTitle(TITLE.HOME);
  loadComponent("movieListNow", "/components/postercard-v");
  loadComponent("movieListTrending", "/components/postercard-v");
  numberIndicating = 0;
};
const handleLoadRev = function () {
  console.log("after load rev");
  setTitle(TITLE.REV);
  setTimeout(function () {
    reviewMenuSlideUp();
    reviewContainerWidthGrow();
  }, 300);
};

const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, complete);
};

const setTitle = function (title) {
  document.title = title + " | Movie Toy";
};
