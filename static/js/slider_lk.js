$(document).ready(function () {
  $(".slider_box").slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    prevArrow: "<div class='slider_prev_events'></div>",
    nextArrow: "<div class='slider_next_events'></div>",
    responsive: [
      {
        breakpoint: 660,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          infinite: true,
        },
      },
      {
        breakpoint: 460,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  });
});
