const modalBackground = () => $("#modalBackground");
const moviesSearched = () => $("#moviesSearched");

const handleClickModalBack = function () {
  modalBackground().hide();
};
const handleSubmitSearchMovie = function (event) {
  event.preventDefault();
  console.log("search movie");
  // $.ajax({
  //   url: "/search",
  //   method: "POST",
  //   data: { keyword: "tenet" },
  //   success: function (response) {
  //     console.log(response);
  //   },
  // });
  setTimeout(function () {
    loadComponent("moviesSearched", "/components/postercard");
  }, 1000);
};
