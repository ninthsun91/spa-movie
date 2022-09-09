const modalBackground = () => $("#modalBackground");
const moviesSearched = () => $("#moviesSearched");
const searchLeft = () => $("#searchLeft");
const searchRight = () => $("#searchRight");
const popupPlace = () => $("#popupPlace");
const handleClickModalBack = function (tagToEmpty) {
  $("#" + tagToEmpty).empty();
  // modalBackground().hide();
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
    loadComponent("moviesSearched", "/components/postercard?direction=horizontal&count=4");
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
let timeout;
const handleSubmitMovieUpsirt = function (event) {
  event.preventDefault();
  console.log("movie upsirt");
  modalBackground().hide();
  loadComponent("popupPlace", "/components/popup-upsertied");
  popupPlace().show();
  timeout = setTimeout(function () {
    popupPlace().hide();
  }, 3000);
};
const handleClickMovieUpsirtCancel = function (makeEdit) {
  if (makeEdit === "make") {
    loadComponent("modalContent", "/components/moviesearch?tagId=modalContent&cover=off");
    console.log("movie make cancel");
  } else {
    loadComponent("reviewViewer", "/components/view-review?tagId=reviewViewer");
    console.log("movie edit cancel");
  }
};
const handleClickPopupConfirm = function () {
  popupPlace().hide();
  clearTimeout(timeout);
};
