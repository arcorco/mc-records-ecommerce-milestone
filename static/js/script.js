$(document).ready(function () {
  $('.slider').slider();
  $('select').formSelect();
  $('.sidenav').sidenav();

  var slider = document.getElementById('price-slider');
  
  noUiSlider.create(slider, {
    start: [0, 20],
    step: 1,
    connect: true,
    range: {
      'min': 0,
      'max': 20
    }
  });

  slider.noUiSlider.on('update', function (values, handle) {
    var value = slider.noUiSlider.get();
    price_min = value[0];
    price_max = value[1];
    console.log(value);
    $('#price_min').attr("value", price_min);
    $('#price_max').attr("value", price_max);
  });

  $('#filter-button').addEventListener.on('click', function() {
    var artists = $("#artist").val();
    $("#artist").attr("value", artists);
  });
});