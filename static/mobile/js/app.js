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


// app range price
$$('#price-filter').on('range:change', function (e, range) {
  console.log('cambiando price');
  // $$('.price-value').text('$'+(range.value[0])+' - $'+(range.value[1]));
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

$$('.infinite-scroll-content').on('infinite', function () {
  console.log('infinite');
});

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

// $$(document).on("click", "#btn_category", function(){
//   console.log('working Contrast');
//   app.router.navigate("/categories/");
// });

// $$('.smart-select').on('open', function (e, popup) {
//   console.log('About popup open');
// });

$$(document).on('smartselect:open', function () {
  console.log('page open smart');
  app.sheet.close('.my-sheet');
  // app.popup.close('.popup-about');
});
$$(document).on('smartselect:closed', function () {
  console.log('page close smart');
  app.sheet.open('.my-sheet');
  // app.popup.open('.popup-about');
});


$$(document).on("click", "#back-filter-product", function(){
  console.log('categoria close');
  app.sheet.open('.my-sheet');
  // app.popup.open('.popup-about');

});


$$(document).on("click", "#btn-categoria-filter", function(){
  console.log('enviar a filtro de categoria');
  var id = $$(this).attr('id-categoria')
  console.log(id);
  var url_get = '?'
  if(id){
    url_get = url_get + 'category=' + id
  }
  app.preloader.show();
  app.router.navigate("/products/"+url_get);
  // app.sheet.open('.my-sheet');
  // app.popup.open('.popup-about');

});


$$(document).on("click", "#btn-shop-index", function(){
  console.log('enviar a filtro de shop2');
  var id = $$(this).attr('id_shop')
  console.log(id);
  var url_get = '?'
  if(id){
    url_get = url_get + 'shop=' + id
  }
  app.sheet.close('.shop-sheet');
  app.preloader.show();
  app.router.navigate("/products/"+url_get);
  // app.sheet.open('.my-sheet');
  // app.popup.open('.popup-about');

});

$$(document).on("click", "#btn-brand-index", function(){
  console.log('enviar a filtro de brand');
  var id = $$(this).attr('id_brand')
  console.log(id);
  var url_get = '?'
  if(id){
    url_get = url_get + 'brand=' + id
  }
  app.sheet.close('.brand-sheet');
  app.preloader.show();
  app.router.navigate("/products/"+url_get);
  // app.sheet.open('.my-sheet');
  // app.popup.open('.popup-about');

});


$$(document).on("click", "#filter-product", function(){
  console.log('Aplicar filtro');
  var formData = ""
  formData = app.form.convertToData('#form-filter');
  console.log(formData);
  // console.log(e.detail.xhr);
  // formData.forEach(function(v,i){
  //   console.log(v);
  // });
  var url_get = '?'
  if(formData["q"]){
    url_get = url_get + 'q=' + formData["q"] + '&'
  }
  if(formData["shop"]){
    url_get = url_get + 'shop=' + formData["shop"] + '&'
  }
  if(formData["category"]){
    url_get = url_get + 'category=' + formData["category"] + '&'
  }
  if(formData["page"]){
    url_get = url_get + 'page=' + formData["page"] + '&'
  }
  if(formData["min_price"]){
    url_get = url_get + 'min_price=' + formData["min_price"] + '&'
  }
  if(formData["max_price"]){
    url_get = url_get + 'max_price=' + formData["max_price"] + '&'
  }
  if(formData["brand"]){
    url_get = url_get + 'brand=' + formData["brand"] + '&'
  }
  // var d = formData["q"]

  // d = $.param( formData );
  console.log(url_get);
  app.preloader.show();
  app.router.navigate("/products/"+url_get);
});
// $$(document).on('smartselect:close', function () {
//   console.log('page open smart');
// })


$$(document).on('page:init', '.page[data-name="products"]', function (e) {
  console.log('page init product');
  app.preloader.hide();
  // app.infinite.create($$('.page-content'));


});

$$(document).on("click", "#categoria-smart", function(){
  console.log('categoria close');
  app.sheet.close('.my-sheet');
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
    url_get = url_get + 'q=' + formData["q"] + '&'
  }
  if(formData["shop"]){
    url_get = url_get + 'shop=' + formData["shop"] + '&'
  }
  if(formData["category"]){
    url_get = url_get + 'category=' + formData["category"] + '&'
  }
  if(formData["page"]){
    url_get = url_get + 'page=' + formData["page"] + '&'
  }
  if(formData["min_price"]){
    url_get = url_get + 'min_price=' + formData["min_price"] + '&'
  }
  if(formData["max_price"]){
    url_get = url_get + 'max_price=' + formData["max_price"] + '&'
  }
  if(formData["brand"]){
    url_get = url_get + 'brand=' + formData["brand"] + '&'
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
