const leftChevron = () => $("#leftChevron");
const rightChevron = () => $("#rightChevron");
const imgbox = () => $(".img-box");
const carouselContainer = () => $(".carousel-constainer");
const lastImgBox = () => $(".carousel-constainer .img-box:last-child");
const firstImgBox = () => $(".carousel-constainer .img-box:first-child");
let clickable = true;
const handleClickLeftChevron = function () {
  if (clickable) {
    clickable = false;
    imgbox().css("transition", "all 1s");
    imgbox().css("transform", `translateX(100vw)`);
    setTimeout(function () {
      imgbox().css("transition", "none");
      lastImgBox().prependTo(carouselContainer());
      imgbox().css("transform", `translateX(0vw)`);
      clickable = true;
    }, 1000);
    console.log("chevron left");
  }
};
const handleClickRightChevron = function () {
  if (clickable) {
    clickable = false;
    imgbox().css("transition", "all 1s");
    imgbox().css("transform", `translateX(-100vw)`);
    setTimeout(function () {
      imgbox().css("transition", "none");
      firstImgBox().appendTo(carouselContainer());
      imgbox().css("transform", `translateX(0vw)`);
      clickable = true;
    }, 1000);
    console.log("chevron right");
  }
};
