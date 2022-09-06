const PATH_NAME = {
  HOME: "/",
  REV: "/rev",
};

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
  pushHistory(PATH_NAME.REV);
  loadPage(PATH_NAME.REV);
};
const loadHome = function () {
  pushHistory(PATH_NAME.HOME);
  loadPage(PATH_NAME.HOME, afterLoadHome);
};
const afterLoadHome = function () {
  console.log("after load home");
  loadComponent("movieListNow", "/components/postercard-v");
  loadComponent("movieListTrending", "/components/postercard-v");
};

const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, complete);
};
