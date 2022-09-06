const handleClickMakeReview = function () {
  console.log("review");
};
const handleClickRecentReview = function () {
  console.log("recent");
  loadComponent("recentReview", "/revcard");
};
const handleClickPopularReview = function () {
  console.log("popular");
  loadComponent("popularReview", "/revcard");
};
const handleClickMostReviewed = function () {
  console.log("postercard");
  loadComponent("mostReviewed", "/postercard");
};
