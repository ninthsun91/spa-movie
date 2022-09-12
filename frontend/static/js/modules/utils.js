componentPosition = (tagId) => {
  const { left: x, top: y } = $("#" + tagId).offset();
  return { x, y };
};

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

const setMaxPageReview = (responseText, textStatus, req) => {
  console.log("setMaxPage")
  max_page = responseText.split("value=")[1].split("\"")[1]
  document.cookie = max_page
  console.log("max_page", max_page)
}