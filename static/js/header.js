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

const tagsUp = {
  id: () => $("#" + TAG_ID.SIGN_UP_ID),
  pw: () => $("#" + TAG_ID.SIGN_UP_PW),
  confirm: () => $("#" + TAG_ID.SIGN_UP_CONFIRM),
  errorMsg: () => $("#" + TAG_ID.SIGN_UP_ERROR_MESSAGE),
};
const tagsIn = {
  id: () => $("#" + TAG_ID.SIGN_IN_ID),
  pw: () => $("#" + TAG_ID.SIGN_IN_PW),
  errorMsg: () => $("#" + TAG_ID.SIGN_IN_ERROR_MESSAGE),
};
const idValidator = (idVal) => (reg.id.test(idVal) && idVal ? { result: true } : { result: false, msg: "id error" });
const pwValidator = (pwVal) =>
  reg.password.test(pwVal) && pwVal ? { result: true } : { result: false, msg: "pw error" };
const confirmValidator = (pwVal, confirmVal) =>
  pwVal === confirmVal && confirmVal ? { result: true } : { result: false, msg: "confirm error" };
const signValidator = function ({ id, pw, confirm }) {
  const { result: resultId, msg: msgId } = idValidator(id().val());
  if (!resultId) return msgId;
  const { result: resultPw, msg: msgPw } = pwValidator(pw().val());
  if (!resultPw) return msgPw;
  if (confirm) {
    const { result: resultConfirm, msg: msgConfirm } = confirmValidator(pw().val(), confirm().val());
    if (!resultConfirm) return msgConfirm;
  }
  return { result: true };
};
const showErrorMsg = function (msgTag, { result, msg }) {
  if (!result) {
    msgTag().text(msg);
  } else {
    msgTag().text("");
  }
};

const handleInputSignUpId = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsUp.errorMsg, idValidator(value));
};
const handleInputSignUpPw = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsUp.errorMsg, pwValidator(value));
};
const handleInputSignUpConfirm = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsUp.errorMsg, confirmValidator(tagsUp.pw().val(), value));
};

const handleInputSignInId = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsIn.errorMsg, idValidator(value));
};
const handleInputSignInPw = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsIn.errorMsg, pwValidator(value));
};

const handleSubmitSignUp = function (event) {
  event.preventDefault();
  console.log(signValidator(tagsUp));
  // $.ajax({
  //   url: "/signup",
  //   data: {},
  //   method: "POST",
  //   success: function (res) {
  //     console.log(res);
  //   },
  // });
};
const handleSubmitSignIn = function (event) {
  event.preventDefault();
  console.log(signValidator(tagsIn));
  // $.ajax({
  //   url: "/signin",
  //   data: { username, password },
  //   method: "POST",
  //   success: function (res) {
  //     console.log(res);
  //   },
  // });
};
