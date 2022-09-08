const handleClickMakeReview = function () {
  console.log("review");
  loadComponent("createReview", "/components/moviesearch");
};
const handleClickRecentReview = function () {
  console.log("recent");
  loadComponent("recentReview", "/components/reviewcard");
};
const handleClickPopularReview = function () {
  console.log("popular");
  loadComponent("popularReview", "/components/reviewcard");
};
const handleClickMostReviewed = function () {
  console.log("postercard");
  loadComponent("mostReviewed", "/components/postercard-v");
};
const handleClickViewReview = function () {
  console.log("view review");
  loadComponent("reviewViewer", "/components/view-review");
};
const handleClickReviewEdit = function () {
  console.log("edit review");
  loadComponent("modalContent", "/components/edit");
};
const reviewMenuSlideUp = function () {
  console.log("menu slide up");
  $("#reviewMenu").css("bottom", "-20vh");
};
const reviewContainerWidthGrow = function () {
  console.log("review container width grow");
  $(".review-container").css("width", "100%");
};
