"use strict";
// Dom7
var $ = Dom7;

// Init App
var app = new Framework7({
  root: '#app',
  theme: 'ios',
  routes: routes,
  cache: false,
  cacheDuration: 0
});


var swiper = app.swiper.create('.swiper-container');

app.request.getJSON('http://127.0.0.1:8000/api/products/?format=json', function (data) {
  var result = data['result']
  $(result).forEach(function(v,i){
    console.log('ji');
  });
});


var range = app.range.create({
  el: '.range-price',
  on: {
    change: function (e) {
      $('.price-min').html(e.value[0]+"$");
      $('.price-max').html(e.value[1]+"$");
    }
  }
})
