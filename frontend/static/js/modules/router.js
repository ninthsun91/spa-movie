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

const loadRev = function () {
  if (location.pathname === PATH_NAME.REV) {
    window.scrollTo(0, 0);
  } else {
    pushHistory(PATH_NAME.REV);
    loadPage(PATH_NAME.REV, handleLoadRev);
  }
};
const loadHome = function () {
  if (location.pathname === PATH_NAME.HOME) {
    window.scrollTo(0, 0);
  } else {
    pushHistory(PATH_NAME.HOME);
    loadPage(PATH_NAME.HOME, handleLoadHome);
  }
};
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
