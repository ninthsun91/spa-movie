const modalBackground = () => $("#modalBackground");
const moviesSearched = () => $("#moviesSearched");
const searchLeft = () => $("#searchLeft");
const searchRight = () => $("#searchRight");
const popupPlace = () => $("#popupPlace");
const handleClickModalBack = function (tagToEmpty) {
  $("#" + tagToEmpty).empty();
};
const handleSubmitSearchMovie = function (event) {
  event.preventDefault();
  console.log("search movie");
  keyword = $("#movieTitle").val();
  loadComponent("moviesSearched", `/components/postercard?direction=horizontal&count=4&type=search&keyword=${keyword}`);
  searchLeft().show();
  searchRight().show();
};
const handleClickSearchLeft = function () {
  console.log("left");
};
const handleClickSearchRight = function () {
  console.log("right");
};

const handleClickMovieUpsert = function () {
  console.log("upsert");
  loadComponent("modalContent", "/components/upsert?tagId=modalContent");
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
    loadComponent("reviewViewer", "/components/view-review?tagId=reviewViewer&cover=on");
    console.log("movie edit cancel");
  }
};
const handleClickPopupConfirm = function () {
  popupPlace().hide();
  clearTimeout(timeout);
};

const handleClickReviewLike = function () {
  console.log("like");
  const score = +$("#likeScore").text();
  $("#likeScore").text(score + 1);
};
const handleClickReviewDelete = function () {
  console.log("delete");
};
const handleClickMoviePoster = function (code) {
  console.log(code);
  loadComponent("modalPlace", `/components/movie-with-reviews?tagId=modalPlace&movieId=${code}`);
  console.log("poster");
};
