"use strict"; 
var routes = [
  // Index page
  {
    path: '/',
    url: './index.html',
    name: 'home',
  },
  // About page
  {
    path: '/shop/',
    url: './pages/shop.html',
    name: 'shop',
  },
  // Profile page
  {
    path: '/profile/',
    url: './pages/profile.html',
    name: 'profile',
  },
  // AD Detail
  {
    path: '/ad_detail/',
    url: './pages/ad_detail.html',
    name: 'ad_detail',
  },
  // AD Detail user
  {
    path: '/ad_detail_user/',
    url: './pages/ad_detail_user.html',
    name: 'ad_detail_user',
  },
  // Add Ad
  {
    path: '/add_ad/',
    url: './pages/add_ad.html',
    name: 'add_ad',
  },
  // Pages
  {
    path: '/pages/',
    url: './pages/pages.html',
    name: 'pages',
  },
  // walk
  {
    path: '/walk/',
    url: './pages/walk.html',
    name: 'walk',
  },
  // Login
  {
    path: '/login/',
    url: './pages/login.html',
    name: 'login',
  },
  // Sign up
  {
    path: '/signup/',
    url: './pages/signup.html',
    name: 'signup',
  },
  // categories
  {
    path: '/categories/',
    url: './pages/categories.html',
    name: 'categories',
  },
  // Sellers
  {
    path: '/sellers/',
    url: './pages/sellers.html',
    name: 'categories',
  },
  // Default route (404 page). MUST BE THE LAST
  {
    path: '(.*)',
    url: './pages/404.html',
  },
];
