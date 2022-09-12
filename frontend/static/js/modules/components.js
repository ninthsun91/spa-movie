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
    "/components/postercard" +
      "?direction=horizontal" +
      "&query=search" +
      "&keyword=" +
      encodeURIComponent(keyword) +
      "&chevron=off" +
      "&is_home=no"
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
  loadComponent(
    "modalContent", 
    "/components/upsert" +
    "?tagId=modalContent" +
    "&movieId=" + code
    );
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
      // loadPage("/rev", handleLoadRev);
      // console.log(msg);

      loadComponent("popupPlace", "/components/popup-review-create?type=success");
      if ($("#recentCheckBox").is(":checked")) {
        loadComponent(
          "recentReview", 
          "/components/reviewcard" +
          "?query=recentrev" +
          "&is_home=no"
          );
      }
      if ($("#popularCheckBox").is(":checked")) {
        loadComponent(
          "popularReview", 
          "/components/reviewcard" +
          "?query=popular" +
          "&is_home=no"
          );
      }
      if ($("#mostCheckBox").is(":checked")) {
        loadComponent(
          "mostReviewed",
          "/components/postercard" +
            "?direction=vertical" +
            "&query=trendrev" +
            "&chevron=on" +
            "is_home=no"
        );
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
const handleClickReviewDelete = function (reviewId) {
  modalPlace().empty();
  $.get(`/delete?reviewId=${reviewId}`, (res)=>{
    msg = encodeURIComponent(res.msg)
    loadComponent("popupPlace", "/components/popup?msg="+msg);
      if ($("#recentCheckBox").is(":checked")) {
        loadComponent(
          "recentReview", 
          "/components/reviewcard" +
          "?query=recentrev" +
          "&is_home=no"
          );
      }
      if ($("#popularCheckBox").is(":checked")) {
        loadComponent(
          "popularReview", 
          "/components/reviewcard" +
          "?query=popular" +
          "&is_home=no"
          );
      }
      if ($("#mostCheckBox").is(":checked")) {
        loadComponent(
          "mostReviewed",
          "/components/postercard" +
            "?direction=vertical" +
            "&query=trendrev" +
            "&chevron=on" +
            "is_home=no"
        );
      }
      timeout = setTimeout(function () {
        popupPlace().empty();
      }, 3000);
  })
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
  console.log("mooovie left", query, direction, page)

  switch (query) {
    case "trend":
      loadComponent(
        "movieListTrending",
        "/components/postercard" + 
        "?direction=vertical" + 
        "&query=trend" + 
        "&chevron=on" + 
        "&is_home=yes"
      );
      break;
    case "now":
      loadComponent(
        "movieListNow", 
        "/components/postercard?" +
        "direction=vertical" +
        "&query=now" +
        "&chevron=on" +
        "&is_home=yes"
        );
      break;
    case "trendrev":
      loadComponent(
        "mostReviewed", 
        "/trendrev" +
        "?query=trendrev" +
        "&direction=" + direction
        );
      break;
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickMovieRight = (query, direction) => {
  page = Number(getCookie(query)) + 1;
  if (page === 11) page = 1;
  document.cookie = `${query}=${page}`;
  console.log("mooovie right", query, direction, page)

  switch (query) {
    case "trend":
      loadComponent(
        "movieListTrending",
        "/components/postercard" + 
        "?direction=vertical" + 
        "&query=trend" + 
        "&chevron=on" + 
        "&is_home=yes"
      );
      break;
    case "now":
      loadComponent(
        "movieListNow", 
        "/components/postercard?" +
        "direction=vertical" +
        "&query=now" +
        "&chevron=on" +
        "&is_home=yes"
        );
      break;
    
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickReviewLeft = (query, direction=undefined) => {
  page = Number(getCookie(query)) - 1;
  
  switch (query) {
    case "trendrev":
      if (page === 0) page = 10;
      document.cookie = `${query}=${page}`;
      console.log("mooovie left", query, direction, page)
      loadComponent(
        "mostReviewed",
        "/components/postercard" + 
        "?direction=horizontal" + 
        "&query=trendrev" + 
        "&chevron=on" + 
        "&is_home=no"
      );
      break;
    case "recentrev":
      max_page = Math.ceil(Number(getCookie(`${query}_max`)));
      if (page === 0) page = max_page;
      document.cookie = `${query}=${page}`;
      console.log("review left", query, max_page, page)
      loadComponent("recentReview", `/recentrev?query=recentrev&is_home=no`);
      break;
    case "popular":
      max_page = Math.ceil(Number(getCookie(`${query}_max`)));
      if (page === 0) page = max_page;
      document.cookie = `${query}=${page}`;
      console.log("review left", query, max_page, page)
      loadComponent("popularReview", `/popular?query=popular&is_home=no`);
      break;
    }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};

const handleClickReviewRight = (query, direction=undefined) => {
  page = Number(getCookie(query)) + 1;

  switch (query) {
    case "trendrev":
      if (page === 11) page = 1;
      document.cookie = `${query}=${page}`;
      console.log("mooovie right", query, direction, page)
      loadComponent(
        "mostReviewed",
        "/components/postercard" + 
        "?direction=horizontal" + 
        "&query=trendrev" + 
        "&chevron=on" + 
        "&is_home=no"
      );
      break;
    case "recentrev":
      max_page = Math.ceil(Number(getCookie(`${query}_max`)));
      if (page === max_page + 1) page = 1;
      document.cookie = `${query}=${page}`;
      console.log("review right", query, max_page, page)      
      loadComponent("recentReview", `/recentrev?query=recentrev&is_home=no`);
      break;
    case "popular":
      max_page = Math.ceil(Number(getCookie(`${query}_max`)));
      if (page === max_page + 1) page = 1;
      document.cookie = `${query}=${page}`;
      console.log("review right", query, max_page, page)  
      loadComponent("popularReview", `/popular?query=popular&is_home=no`);
      break;
    
  }
  $("#modalPlace").empty();
  $("#popupPlace").empty();
};
