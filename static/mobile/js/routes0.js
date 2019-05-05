"use strict";
var routes = [
  // Index page

  {
    path: '/',
    url: '/oauth/login/google-oauth2/',
    name: 'home',
  },
  {
    path: '/',
    url: 'http://comparatest.cl/index.html',
    name: 'home',
  },
  // About page
  {
    path: '/shop/',
    url: 'http://comparatest.cl/pages/shop.html',
    name: 'shop',
  },
  // Profile page
  {
    path: '/profile/',
    url: 'http://comparatest.cl/pages/profile.html',
    name: 'profile',
  },
  // AD Detail
  {
    path: '/ad_detail/',
    url: 'http://comparatest.cl/pages/ad_detail.html',
    name: 'ad_detail',
  },
  // AD Detail user
  {
    path: '/ad_detail_user/',
    url: 'http://comparatest.cl/pages/ad_detail_user.html',
    name: 'ad_detail_user',
  },
  // Add Ad
  {
    path: '/add_ad/',
    url: 'http://comparatest.cl/pages/add_ad.html',
    name: 'add_ad',
  },
  // Pages
  {
    path: '/pages/',
    url: 'http://comparatest.cl/pages/pages.html',
    name: 'pages',
  },
  // walk
  {
    path: '/walk/',
    url: 'http://comparatest.cl/pages/walk.html',
    name: 'walk',
  },
  // Login
  {
    path: '/login/',
    url: 'http://comparatest.cl/pages/login.html',
    name: 'login',
  },
  // Sign up
  {
    path: '/signup/',
    url: 'http://comparatest.cl/pages/signup.html',
    name: 'signup',
  },
  // categories
  {
    path: '/categories/',
    url: 'http://comparatest.cl/pages/categories.html',
    name: 'categories',
  },
  // Sellers
  {
    path: '/sellers/',
    url: 'http://comparatest.cl/pages/sellers.html',
    name: 'categories',
  },
  // Default route (404 page). MUST BE THE LAST
  {
    path: '(.*)',
    url: './pages/404.html',
    // url: './pages/perfil.html',
  },
];
