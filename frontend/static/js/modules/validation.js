const reg = {
  id: /^(?=.*[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣])[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣|0-9]{3,15}$/,
  password: /^(?=.*[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣])[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣|0-9]{8,15}$/,
  title: /^(?=.*[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣])[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣|0-9]{3,30}$/,
  content: /^(?=.*[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣])[a-z|A-Z|ㅏ-ㅣ|ㄱ-ㅎ|가-힣|0-9]{3,300}$/,
  email: /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/,
  contact: /^[\d]{2,3}-[\d]{3,4}-[\d]{4}$/,
};

/**에러403 핸들러
 * msg: 팝업모달에 표시할 메시지 */
const handler403Error = (msg) => {
  loadComponent("modalPlace", `/components/popup?msg=${encodeURIComponent(msg)}`);
  setTimeout(function () {
    if ($("#modalPlace").children().text().trim() === msg) {
      $("#modalPlace").empty();
    }
  }, 3000);
}