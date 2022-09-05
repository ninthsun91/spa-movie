const TAG_ID = {
  SIGN: "sign",
  SIGN_IN: "signIn",
  SIGN_UP: "signUp",
};

const sign = $("#" + TAG_ID.SIGN);
const signIn = $("#" + TAG_ID.SIGN_IN);
const signUp = $("#" + TAG_ID.SIGN_UP);

const handleClickSignIn = function () {
  loadComponent(TAG_ID.SIGN_IN, "components/sign_in", function () {
    sign.show();
    signIn.show();
    signUp.hide();
  });
};
const handleClickSignUp = function () {
  loadComponent(TAG_ID.SIGN_UP, "components/sign_up", function () {
    sign.show();
    signUp.show();
    signIn.hide();
  });
};
const hideSign = function () {
  sign.hide();
  signIn.hide();
  signUp.hide();
};
const handleSubmitSignIn = function (event) {
  event.preventDefault();
  $.ajax({
    url: "/signin",
    data: {},
    method: "POST",
    success: function (res) {
      console.log(res);
    },
  });
};
const handleSubmitSignUp = function (event) {
  event.preventDefault();
  $.ajax({
    url: "/signup",
    data: {},
    method: "POST",
    success: function (res) {
      console.log(res);
    },
  });
};
const handleClickReview = function () {
  console.log("review");
  loadRev();
};
const handleClickLogo = function () {
  loadHome();
};
