// $("#Home").on("click", function () {
//   history.pushState({ title: "test" }, "", location.origin + "/");
//   $("#App").load("/ #AppContainer", console.log("test success"));
// });
const loadHome = function () {
  history.pushState({ pathname: "/" }, "", location.origin + "/");
  $("#App").load("/ #AppContainer", console.log("test success"));
};
