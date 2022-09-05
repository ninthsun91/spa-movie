const TAG_ID = {
  SIGN: "sign",
  SIGN_IN: "signIn",
  SIGN_UP: "signUp",
  SIGN_UP_ID: "signUpId",
  SIGN_UP_PW: "signUpPw",
  SIGN_UP_CONFIRM: "signUpConfirm",
  SIGN_UP_ERROR_MESSAGE: "signUpErrorMessage",
  SIGN_IN_ID: "signInId",
  SIGN_IN_PW: "signInPw",
  SIGN_IN_ERROR_MESSAGE: "signInErrorMessage",
};

const sign = () => $("#" + TAG_ID.SIGN);
const signIn = () => $("#" + TAG_ID.SIGN_IN);
const signUp = () => $("#" + TAG_ID.SIGN_UP);

const handleClickSignIn = function () {
  loadComponent(TAG_ID.SIGN_IN, "/signin", function () {
    sign().show();
    signIn().show();
    signUp().hide();
  });
};
const handleClickSignUp = function () {
  loadComponent(TAG_ID.SIGN_UP, "/signup", function () {
    sign().show();
    signUp().show();
    signIn().hide();
  });
};
const hideSign = function () {
  sign().hide();
  signIn().hide();
  signUp().hide();
};
const handleClickReview = function () {
  loadRev();
};
const handleClickLogo = function () {
  loadHome();
};

const signUpId = () => $("#" + TAG_ID.SIGN_UP_ID);
const signUpPw = () => $("#" + TAG_ID.SIGN_UP_PW);
const signUpConfirm = () => $("#" + TAG_ID.SIGN_UP_CONFIRM);
const signUpErrorMessage = () => $("#" + TAG_ID.SIGN_UP_ERROR_MESSAGE);
const signInId = () => $("#" + TAG_ID.SIGN_IN_ID);
const signInPw = () => $("#" + TAG_ID.SIGN_IN_PW);
const signInErrorMessage = () => $("#" + TAG_ID.SIGN_IN_ERROR_MESSAGE);

const handleSubmitSignIn = function (event) {
  event.preventDefault();
  const username = signInId().val();
  const password = signInPw().val();
  const isIdValid = reg.id.test(username);
  const isPwValid = reg.password.test(password);
  if (isIdValid && isPwValid) {
    $.ajax({
      url: "/signin",
      data: { username, password },
      method: "POST",
      success: function (res) {
        console.log(res);
      },
    });
  } else if (!isIdValid && !isPwValid) {
    signInErrorMessage().text = "id pw error";
  } else if (!isIdValid) {
    signInErrorMessage().text = "id error";
  } else {
    signInErrorMessage().text = "pw error";
  }
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

const validateSignUp = function () {
  const idVal = signUpId().val();
  const pwVal = signUpPw().val();
  const confirmVal = signUpConfirm().val();
  if (!reg.id.test(idVal) && idVal !== "") {
    signUpErrorMessage().text("id error");
  } else if (!reg.password.test(pwVal) && pwVal !== "") {
    signUpErrorMessage().text("pw error");
  } else if (pwVal !== confirmVal && confirmVal !== "") {
    signUpErrorMessage().text("confirm error");
  } else {
    signUpErrorMessage().text("");
  }
};
const validateSignIn = function () {
  const idVal = signInId().val();
  const pwVal = signInPw().val();
  if (!reg.id.test(idVal) && idVal !== "") {
    signInErrorMessage().text("id error");
  } else if (!reg.password.test(pwVal) && pwVal !== "") {
    signInErrorMessage().text("pw error");
  } else {
    signInErrorMessage().text("");
  }
};

const handleInputSignUpId = function () {
  validateSignUp();
};
const handleInputSignUpPw = function () {
  validateSignUp();
};
const handleInputSignUpConfirm = function () {
  validateSignUp();
};

const handleInputSignInId = function (event) {
  validateSignIn();
};
const handleInputSignInPw = function (event) {
  validateSignIn();
};