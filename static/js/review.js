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
