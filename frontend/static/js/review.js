const handleClickMakeReview = function () {
  console.log("review");
  loadComponent("createReview", "/components/moviesearch?tagId=createReview&cover=on");
};
const handleClickRecentLabel = function () {
  console.log("recent");
  loadComponent("recentReview", "/components/reviewcard");
  toggleLi("recentLi");
  setTimeout(function () {
    scrollToTag("recentReview");
  }, 500);
};
const handleClickPopularLabel = function () {
  console.log("popular");
  loadComponent("popularReview", "/components/reviewcard");
  toggleLi("popularLi");
  setTimeout(function () {
    scrollToTag("popularReview");
  }, 500);
};
const handleClickMostLabel = function () {
  console.log("postercard");
  loadComponent("mostReviewed", "/components/postercard?direction=vertical&count=6");
  toggleLi("mostLi");
  setTimeout(function () {
    scrollToTag("mostReviewed");
  }, 500);
};
const handleClickViewReview = function () {
  console.log("view review");
  loadComponent("reviewViewer", "/components/view-review?tagId=reviewViewer");
};
const handleClickReviewEdit = function () {
  console.log("edit review");
  loadComponent("modalContent", "/components/edit");
};
const handleClickReviewH1 = function () {
  console.log("review H1 click");
  window.scrollTo(0, 0);
};

const reviewMenuSlideUp = function () {
  console.log("menu slide up");
  $("#reviewMenu").css("bottom", "-20vh");
};
const reviewContainerWidthGrow = function () {
  console.log("review container width grow");
  $(".review-container").css("width", "100%");
};
const toggleLi = function (tagId) {
  $("#" + tagId).toggleClass("review-li");
};
const scrollToTag = function (tagId) {
  const { top } = $("#" + tagId).offset();
  window.scrollTo(0, top - 120);
};
