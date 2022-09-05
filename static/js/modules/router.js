const PATH_NAME = {
  HOME: "/",
  MOV: "/mov",
};

const loadPage = (pathname) => {
  $("#App").load(`${pathname} #AppContainer`);
};
const pushHistory = (pathname) => history.pushState({ pathname }, "", location.origin + pathname);

history.replaceState({ pathname: location.pathname }, "");
window.onpopstate = function ({ state }) {
  switch (state.pathname) {
    case PATH_NAME.MOV:
      return loadPage(PATH_NAME.MOV);
    case PATH_NAME.HOME:
      return loadPage(PATH_NAME.HOME);
  }
};
const loadMovie = function () {
  pushHistory(PATH_NAME.MOV);
  loadPage(PATH_NAME.MOV);
};
const loadHome = function () {
  pushHistory(PATH_NAME.HOME);
  loadPage(PATH_NAME.HOME);
};

const loadComponent = function (tagId, pathname, complete = undefined) {
  $("#" + tagId).load(`${pathname}`, complete);
};
