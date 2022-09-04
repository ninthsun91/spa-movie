history.replaceState({ pathname: location.pathname }, "");
window.onpopstate = function ({ state }) {
  switch (state.pathname) {
    case "/movie":
      return $("#App").load("/movie #AppContainer", console.log("test success"));
    case "/":
      return $("#App").load("/ #AppContainer", console.log("test success"));
  }
};
