// $("#movie").on("click", function () {
//   history.pushState({ title: "test" }, "", location.origin + "/movie");
//   $("#App").load("/movie #AppContainer", console.log("test success"));
// });
const loadMovie = function () {
  history.pushState({ name: "movie" }, "", location.origin + "/movie");
  $("#App").load("/movie #AppContainer", console.log("test success"));
};
