history.replaceState({ pathname: location.pathname }, "");
window.onpopstate = function ({ state }) {
  switch (state.pathname) {
    case "/mov":
      return $("#App").load("/mov #AppContainer", console.log("test success"));
    case "/":
      return $("#App").load("/ #AppContainer", console.log("test success"));
  }
};
const loadMovie = function () {
  history.pushState({ pathname: "/mov" }, "", location.origin + "/mov");
  $("#App").load("/mov #AppContainer", console.log("test success"));
};
const loadHome = function () {
  history.pushState({ pathname: "/" }, "", location.origin + "/");
  $("#App").load("/ #AppContainer", console.log("test success"));
};
