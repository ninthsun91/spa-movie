const modalBackground = () => $("#modalBackground");
const moviesSearched = () => $("#moviesSearched");
const searchLeft = () => $("#searchLeft");
const searchRight = () => $("#searchRight");
const popupPlace = () => $("#popupPlace");
const modalPlace = () => $("#modalPlace");
const handleClickModalBack = function (tagToEmpty) {
  $("#" + tagToEmpty).empty();
};
const handleSubmitSearchMovie = function (event) {
  event.preventDefault();
  // console.log("search movie");
  keyword = $("#movieTitle").val();
  loadComponent(
    "moviesSearched",
    `/components/postercard?direction=horizontal&count=4&query=search&keyword=${encodeURIComponent(keyword)}`
  );
  searchLeft().show();
  searchRight().show();
};
const handleClickSearchLeft = function () {
  console.log("left");
};
const handleClickSearchRight = function () {
  console.log("right");
};

const handleClickMovieUpsert = function (code) {
  // console.log("upsert");
  loadComponent("modalContent", `/components/upsert?tagId=modalContent&movieId=${code}`);
  searchLeft().hide();
  searchRight().hide();
};

let timeout;
const handleSubmitMovieUpsirt = function (event, movieId, reviewId = undefined) {
  event.preventDefault();

  data = {
    code: movieId,
    title: $("#reviewTitle").val(),
    comment: $("#reviewContent").val(),
    userRating: 10,
  };
  // console.log(`review id = ${reviewId}`)
  if (reviewId.length === 24) {
    data.id = reviewId;
  }
  // console.log("data : ", data);

  $.ajax({
    url: "/review",
    data,
    method: "POST",
    success: function ({ msg }) {
      if (msg === "로그인 세션이 만료되었습니다.") {
        loadComponent("popupPlace", "/components/popup-review-create?type=logout");
        popupPlace().show();
      }
      modalPlace().empty();
      // console.log(msg);

      loadComponent("popupPlace", "/components/popup-review-create?type=success");
      if ($("#recentCheckBox").is(":checked")) {
        loadComponent("recentReview", "/components/reviewcard?type=recentrev");
      }
      if ($("#popularCheckBox").is(":checked")) {
        loadComponent("popularReview", "/components/reviewcard?type=popular");
      }
      if ($("#mostCheckBox").is(":checked")) {
        loadComponent("mostReviewed", "/components/postercard?direction=vertical&count=6&type=trendrev");
      }
      timeout = setTimeout(function () {
        popupPlace().empty();
      }, 3000);
    },
    complete: function () {
      // modalBackground().hide();
    },
  });
  // console.log("movie upsirt");
};
const handleClickMovieUpsirtCancel = function (makeEdit, reviewId) {
  if (makeEdit === "make") {
    loadComponent("modalContent", "/components/moviesearch?tagId=modalContent&cover=off");
    // console.log("movie make cancel");
  } else {
    loadComponent("modalPlace", `/components/view-review?tagId=modalPlace&cover=on&reviewId=${reviewId}`);
    // console.log("movie edit cancel");
  }
};
const handleClickPopupConfirm = function () {
  if (popupPlace().children().length === 0) {
    modalPlace().empty();
  } else {
    popupPlace().empty();
  }
  clearTimeout(timeout);
};

const handleClickReviewLike = function () {
  // console.log("like");
  const score = +$("#likeScore").text();
  $("#likeScore").text(score + 1);
};
const handleClickReviewDelete = function () {
  // console.log("delete");
};
const handleClickMoviePoster = function (code) {
  // console.log(code);
  loadComponent("modalPlace", `/components/movie-with-reviews?tagId=modalPlace&movieId=${code}`);
  // console.log("poster");
};

// movie card list button

const handleClickMovieLeft = (query, direction) => {
  page = Number(getCookie(query)) - 1;
  if (page === 0) page = 10;
  document.cookie = `${query}=${page}`;
  console.log("movieeeeeeeeeee leeeeeeeeeeft", query, page, direction);

  switch (query) {
    case "trend":
      loadComponent("movieListTrending", `/trend?query=trend&direction=${direction}`);
      break;
    case "now":
      loadComponent("movieListNow", `/now?query=now&direction=${direction}`);
      break;
    case "trendrev":
      loadComponent("mostReviewed", `/trendrev?query=trendrev&direction=${direction}`);
      break;
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickMovieRight = (query, direction) => {
  page = Number(getCookie(query)) + 1;
  if (page === 11) page = 1;
  document.cookie = `${query}=${page}`;
  console.log("moooooooovie riiiiiiiiiight", query, page, direction);

  switch (query) {
    case "trend":
      loadComponent("movieListTrending", `/trend?query=trend&direction=${direction}`);
      break;
    case "now":
      loadComponent("movieListNow", `/now?query=now&direction=${direction}`);
      break;
    case "trendrev":
      loadComponent("mostReviewed", `/trendrev?query=trendrev&direction=${direction}`);
      break;
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickReviewLeft = (query) => {
  console.log("reviewwww leeeeeeeeeeft")
  max_page = Math.ceil(Number(getCookie(`${query}_max`)))
  page = Number(getCookie(query)) -1;
  if (page === 0) page = max_page;
  document.cookie = `${query}=${page}`;

  switch (query) {
    case "recentrev":
      loadComponent("recentReview", `/recentrev?query=recentrev`);
      break;
    case "popular":
      loadComponent("popularReview", `/popular?query=popular`);
      break;
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickReviewRight = (query) => {
  console.log("reviewwww riiiiiiiiiight")
  max_page = Math.ceil(Number(getCookie(`${query}_max`)))
  page = Number(getCookie(query)) +1;
  if (page === max_page+1) page = 1;
  document.cookie = `${query}=${page}`;

  switch (query) {
    case "recentrev":
      loadComponent("recentReview", `/recentrev?query=recentrev`);
      break;
    case "popular":
      loadComponent("popularReview", `/popular?query=popular`);
      break;
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};
