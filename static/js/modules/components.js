const modalBackground = () => $("#modalBackground");
const moviesSearched = () => $("#moviesSearched");
const searchLeft = () => $("#searchLeft");
const searchRight = () => $("#searchRight");

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
    loadComponent("moviesSearched", "/components/postercard-h");
    searchLeft().show();
    searchRight().show();
  }, 1000);
};
const handleClickSearchLeft = function () {
  console.log("left");
};
const handleClickSearchRight = function () {
  console.log("right");
};

const handleClickMovieUpsert = function () {
  console.log("upsert");
  loadComponent("modalContent", "/components/upsert");
  searchLeft().hide();
  searchRight().hide();
};
const handleSubmitMovieUpsirt = function (event) {
  event.preventDefault();
  console.log("movie upsirt");
  modalBackground().hide();
};
const handleClickMovieUpsirtCancel = function () {
  loadComponent("modalContent", "/components/plus/create-uncov");
  console.log("movie upsirt cancel");
};
