const sign = () => $("#" + TAG_ID.SIGN);
const profile = () => $("#" + TAG_ID.PROFILE);

const handleClickSignIn = function () {
  loadComponent(TAG_ID.SIGN, "/components/signin?tagId=" + TAG_ID.SIGN, function () {
    sign().show();
  });
};
const handleClickSignInCancel = function () {
  sign().hide();
};
const handleClickSignUp = function () {
  loadComponent(TAG_ID.SIGN, "/components/signup?tagId=" + TAG_ID.SIGN, function () {
    sign().show();
  });
};
const handleClickSignUpCancel = function () {
  sign().hide();
};
const hideSign = function () {
  sign().hide();
  sign().empty();
};

const handleClickReview = function () {
  reloadPage(PATH_NAME.REV, handleLoadRev);
};

const handleClickLogo = function () {
  console.log("click logo");
  reloadPage(PATH_NAME.HOME, handleLoadHome);
};

// my page
const handleClickMyPage = function () {
  console.log("click profile");
  loadMyPage();
};

// profile
const handleClickProfile = function () {

  // console.log("testtest")

  // $.get("/test2", (res)=>{
  //   console.log(res)
  // })

  loadComponent(TAG_ID.PROFILE, "/components/profile/update?tagId=" + TAG_ID.PROFILE, function () {
    profile().show();
  });
};

const hideProfile = function () {
  profile().hide();
  profile().empty();
};

const handleClickProfileCancel = function () {
  profile().hide();
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
const tagsProfile = {
  pw: () => $("#" + TAG_ID.PROFILE_PW),
  confirm: () => $("#" + TAG_ID.PROFILE_CONFIRM),
  email: () => $("#" + TAG_ID.PROFILE_EMAIL),
  contact: () => $("#" + TAG_ID.PROFILE_CONTACT),
  address: () => $("#" + TAG_ID.PROFILE_ADDRESS),
  instagram: () => $("#" + TAG_ID.PROFILE_INSTAGRAM),
  errorMsg: () => $("#" + TAG_ID.PROFILE_ERROR_MESSAGE),
};
const idValidator = (idVal) => (reg.id.test(idVal) && idVal ? { isValid: true } : { isValid: false, msg: "id error" });
const pwValidator = (pwVal) =>
  reg.password.test(pwVal) && pwVal ? { isValid: true } : { isValid: false, msg: "pw error" };

const confirmValidator = (pwVal, confirmVal) =>
  pwVal === confirmVal && confirmVal ? { isValid: true } : { isValid: false, msg: "confirm error" };

const emailValidator = (emailVal) => 
  reg.email.test(emailVal) && emailVal ? { isValid: true } : { isValid: false, msg: "email error" };

  const contactValidator = (contactVal) => 
  reg.contact.test(contactVal) && contactVal ? { isValid: true } : { isValid: false, msg: "contact error" };

const signValidator = function ({ id, pw, confirm }) {
  const { isValid: isValidId, msg: msgId } = idValidator(id().val());
  if (!isValidId) return msgId;
  const { isValid: isValidPw, msg: msgPw } = pwValidator(pw().val());
  if (!isValidPw) return msgPw;
  if (confirm) {
    const { isValid: isValidConfirm, msg: msgConfirm } = confirmValidator(pw().val(), confirm().val());
    if (!isValidConfirm) return msgConfirm;
  }
  return { isValid: true };
};

const profileValidator = function ({ pw, confirm, email, contact }) {
  const { isValid: isValidPw, msg: msgPw } = pwValidator(pw().val());
  if (!isValidPw) return msgPw;
  if (confirm) {
    const { isValid: isValidConfirm, msg: msgConfirm } = confirmValidator(pw().val(), confirm().val());
    if (!isValidConfirm) return msgConfirm;
  } 
  const { isValid: isValidEmail, msg: msgEmail } = emailValidator(email().val());
  if (!isValidEmail) return msgEmail;
  const { isValid: isValidContact, msg: msgContact } = contactValidator(contact().val());
  if (!isValidContact) return msgContact;
  return { isValid: true };
  
};



const showErrorMsg = function (msgTag, { isValid, msg }) {
  if (!isValid) {
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


const handleInputProfilePw = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsProfile.errorMsg, pwValidator(value));
};

const handleInputProfileConfirm = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsProfile.errorMsg, confirmValidator(tagsProfile.pw().val(), value));
};

const handleInputProfileEmail = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsProfile.errorMsg, emailValidator(value));
};

const handleInputProfileContact = function (event) {
  const {
    target: { value },
  } = event;
  showErrorMsg(tagsProfile.errorMsg, contactValidator(value));
};


const handleSubmitSignUp = function (event) {
  event.preventDefault();
  // console.log(event);
  // console.log(signValidator(tagsUp));
  const { isValid } = signValidator(tagsUp);
  if (isValid) {
    const data = { username: tagsUp.id().val(), password: tagsUp.pw().val() };
    $.ajax({
      url: "/signup",
      data,
      method: "POST",
      success: function ({ msg }) {
        if (msg === "success") {
          loadComponent(TAG_ID.SIGN, "/components/signin?tagId=" + TAG_ID.SIGN, function () {
            sign().show();
          });
        }
      },
      complete: function () {},
    });
  }
};

const handleSubmitSignIn = function (event) {
  event.preventDefault();
  const { isValid } = signValidator(tagsIn);
  const data = { username: tagsIn.id().val(), password: tagsIn.pw().val() };
  if (isValid) {
    $.ajax({
      url: "/signin",
      data,
      method: "POST",
      success: function (res) {
        // console.log(res);
        const { pathname } = location;
        loadPage(pathname);
        // console.log("pathname", pathname);
        if (pathname === PATH_NAME.HOME) {
          setTimeout(function () {
            loadComponent(
              "movieListNow",
              "/components/postercard" +
                "?direction=vertical" +
                "&query=now" +
                "&chevron=on" +
                "is_home=yes"
            );
            loadComponent(
              "movieListTrending",
              "/components/postercard" +
                "?direction=vertical" +
                "&query=trend" +
                "&chevron=on" +
                "is_home=yes"
          }, 500);
        }
        if (pathname === PATH_NAME.REV) {
          setTimeout(function () {
            loadComponent("recentReview", "/components/reviewcard?query=recent&is_home=no");
            loadComponent("popularReview", "/components/reviewcard?query=popular&is_home=no");

            setTimeout(function () {
              reviewMenuSlideUp();
              reviewContainerWidthGrow();
            }, 300);
          }, 500);
        }
      },
      complete: function () {},
    });
  }
};

const handleSubmitProfile = function (event) {
  event.preventDefault();

  const { isValid } = profileValidator(tagsProfile);
  if (isValid) {
    const data = { 
      password: tagsProfile.pw().val(),
      email: tagsProfile.email().val(),
      contact: tagsProfile.contact().val(),
      address: tagsProfile.address().val(),
      instagram: tagsProfile.instagram().val(),
    }
    $.ajax({
      url: "/profile",
      data,
      method: "POST",
      success: function ({ msg }) {
        const { pathname } = location;
        loadPage(pathname);
      },
    });
  }
};

const handleClickLogOut = function () {
  // console.log("logout");
  document.cookie = "logintoken=; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
  const { pathname } = location;

  switch (pathname) {
    case PATH_NAME.REV:
      return loadPage(PATH_NAME.REV, handleLoadRev);
    case PATH_NAME.HOME:
      return loadPage(PATH_NAME.HOME, handleLoadHome);
    case PATH_NAME.MY_PAGE:
      return loadPage(PATH_NAME.MY_PAGE, handleLoadMyPage);
  }
};
