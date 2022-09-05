const PATH_NAME = {
  HOME: "/",
  REV: "/rev",
};

const loadPage = (pathname) => {
  $("#App").load(`${pathname} #AppContainer`);
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
  loadPage(PATH_NAME.HOME);
};

const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, complete);
};
