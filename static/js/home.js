const leftChevron = () => $("#leftChevron");
const rightChevron = () => $("#rightChevron");
const imgbox = () => $(".carousel-box");
const carouselContainer = () => $(".carousel-constainer");
const lastImgBox = () => $(".carousel-constainer .carousel-box:last-child");
const firstImgBox = () => $(".carousel-constainer .carousel-box:first-child");
const indicator = () => $(".indicator");
const slugs = (number) => $(`.slug:nth-child(${number})`);

let numberIndicating = 0;
let clickable = true;
const calculating = (num) => (((num % 3) + 3) % 3) + 1;
const shrinkSlug = function (num) {
  slugs(calculating(num)).css("width", "15px");
};
const handleClickLeftChevron = function () {
  if (clickable) {
    clickable = false;
    shrinkSlug(numberIndicating);
    numberIndicating -= 1;
    slugs(calculating(numberIndicating)).css("width", "50px");

    imgbox().css("transition", "all 0.5s");
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
    shrinkSlug(numberIndicating);
    numberIndicating += 1;
    slugs(calculating(numberIndicating)).css("width", "50px");

    imgbox().css("transition", "all 0.5s");
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
