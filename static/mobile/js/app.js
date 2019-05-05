"use strict";
// Dom7
var $$ = Dom7;
var host_site = 'https://comparagrow.cl'

// Init App
var app = new Framework7({
  root: '#app',
  theme: 'ios',
  routes: routes,
  cache: false,
  cacheDuration: 0
});

// ************************************************************************************************
// ************************************************************************************************
// seccion pagina productos
var allowInfinite = true;
// Last loaded index
var lastItemIndex = $$('.list li').length;
// Max items to load
var maxItems = 200;
// Append items per load
var itemsPerLoad = 20;

// ************************************************************************************************
// ************************************************************************************************


var swiper1 = app.swiper.create('#slide_button',{
  slidesPerView:2.5
});
var swiper2 = app.swiper.create('#slide_banner',{
  slidesPerView:1
});
var swiper1 = app.swiper.create('#swiper-container-rebajas',{
  slidesPerView:3
});
var swiper1 = app.swiper.create('#swiper-container-grow',{
  slidesPerView:3
});

app.request.getJSON(host_site+'/api/products/?format=json', function (data) {
  var result = data.results
  console.log(result);
  result.forEach(function(v,i){
    $$( "#swiper-wrapper-destacados" ).append('<div class="swiper-slide">'+
      "<a href=\"#\"><img src=\"http://127.0.0.1:8000/media/assets/product/152.jpg\" class=\"seller-img\"></a>"+
      "<div class=\"item-title\"><a href=\"/productos/publicity/redirect/carrusel_destacados/"+v.id+"\">"+v.name+"</a></div>"+
      "<div class=\"item-infos\">"+v.total+"</div>"+
      "</div>");
    console.log('ji');
  });
  var swiper = app.swiper.create('#swiper-container-destacados',{
    slidesPerView:3
  });
});

// $$(document).on('pageInit', function() {
//     console.log('test');
//     // var queryForm = null;
//     // $$('#query-submit').on('click', function () {
//     //  queryForm = app.formToJSON('#query-form');
//     //    console.log(JSON.stringify(queryForm));
//     // });
//     $('#btn_category').on('click', function () {
//         console.log('data');
//         app.router.navigate("/shop/?q=1");
//         console.log('click');
//     });
// });

$$(document).on("click", "#btn_category", function(){
  console.log('working Contrast');
  app.router.navigate("/categories/");
});

$$(document).on('page:init', '.page[data-name="products"]', function (e) {
  console.log('page init product');
  app.preloader.hide();
});

$$(document).on("click", "#btn_category", function(){
  console.log('working Contrast');
  app.router.navigate("/shop/?q=1");
});

$$(document).on("submit", "#form-search", function(e){
  e.preventDefault();
  var formData = ""
  formData = app.form.convertToData('#form-search');
  console.log(formData);
  // console.log(e.detail.xhr);
  // formData.forEach(function(v,i){
  //   console.log(v);
  // });
  var url_get = '?'
  if(formData["q"]){
    url_get = url_get + 'q=' + formData["q"]
  }
  if(formData["shop"]){
    url_get = url_get + 'shop=' + formData["shop"]
  }
  if(formData["order"]){
    url_get = url_get + 'order=' + formData["order"]
  }
  if(formData["page"]){
    url_get = url_get + 'page=' + formData["page"]
  }
  if(formData["min_price"]){
    url_get = url_get + 'min_price=' + formData["min_price"]
  }
  if(formData["max_price"]){
    url_get = url_get + 'max_price=' + formData["max_price"]
  }
  if(formData["brand"]){
    url_get = url_get + 'brand=' + formData["brand"]
  }
  // var d = formData["q"]

  // d = $.param( formData );
  console.log(url_get);
  app.preloader.show();
  app.router.navigate("/products/"+url_get);
  // app.router.navigate(
  // {
  // url:"/products/"+url_get,
  // ignoreCache:true,
  // reloadCurrent:true,
  // animate:false})
  // return false;
  // app.router.navigate("/shop/?q=1");
});


// app.router.loadPage('/pages/shop.html');

var range = app.range.create({
  el: '.range-price',
  on: {
    change: function (e) {
      $('.price-min').html(e.value[0]+"$");
      $('.price-max').html(e.value[1]+"$");
    }
  }
})
