const handleClickMakeReview = function () {
  console.log("review");
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
  loadComponent("mostReviewed", "/components/postercard");
};
