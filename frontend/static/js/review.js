const handleClickMakeReview = function () {
  console.log("review");
  loadComponent("modalPlace", "/components/moviesearch?tagId=modalPlace&cover=on");
};
const handleClickRecentLabel = function () {
  console.log("recent");
  loadComponent("recentReview", "/components/reviewcard?type=recentrev");
  toggleLi("recentLi");
  setTimeout(function () {
    scrollToTag("recentReview");
  }, 300);
};
const handleClickPopularLabel = function () {
  console.log("popular");
  loadComponent("popularReview", "/components/reviewcard?type=popular");
  toggleLi("popularLi");
  setTimeout(function () {
    scrollToTag("popularReview");
  }, 300);
};
const handleClickMostLabel = function () {
  console.log("postercard");
  loadComponent("mostReviewed", "/components/postercard?direction=vertical&count=6&type=trendrev");
  toggleLi("mostLi");
  setTimeout(function () {
    scrollToTag("mostReviewed");
  }, 300);
};
const handleClickViewReview = function (reviewId) {
  console.log("view review");
  loadComponent("modalPlace", `/components/view-review?tagId=modalPlace&reviewId=${reviewId}`);
  setTimeout(function () {
    if ($("#modalPlace").children().text().trim() === "리뷰를 확인하시려면 로그인해주세요") {
      $("#modalPlace").empty();
    }
  }, 2000);
};
const handleClickReviewEdit = function (code, reviewId) {
  console.log("edit review");
  loadComponent("modalContent", `/components/edit?tagId=modalContent&movieId=${code}&reviewId=${reviewId}`);
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
