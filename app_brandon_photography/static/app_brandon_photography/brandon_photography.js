// $(document).ready(function() {
//   $('#navbarDropdown').mouseenter(function() {
//     $('.dropdown-menu').slideToggle(300, "linear");
//   });
//
//   $('.dropdown-menu').mouseleave(function() {
//     $(this).slideToggle(300, "linear");
//   });
// });


var myNav = document.getElementById('mynav');
window.onscroll = function () {
      "use strict";
       if (document.body.scrollTop >= 20 || document.documentElement.scrollTop >= 20 ) {
          myNav.classList.add("nav-colored");
          $('ul.navbar-nav>li.nav-item>a.nav-link').addClass('custom');
          myNav.classList.remove("nav-transparent");
      }
      else {
          myNav.classList.add("nav-transparent");
          myNav.classList.remove("nav-colored");
          $('ul.navbar-nav>li.nav-item>a.nav-link').removeClass('custom');
      }
};

$(".ongray").hover(
  function(){$(this).addClass("g")},
  function(){$(this).removeClass("g");}
);

$(".photocover").hover(
  function(){$(this).removeClass("photog")},
  function(){$(this).addClass("photog");}
);





const getCookie = (name) => {
  const value = " " + document.cookie;
  console.log("value", `==${value}==`);
  const parts = value.split(" " + name + "=");
  return parts.length < 2 ? undefined : parts.pop().split(";").shift();
};

const setCookie = function (name, value, expiryDays, domain, path, secure) {
  const exdate = new Date();
  exdate.setHours(
    exdate.getHours() +
      (typeof expiryDays !== "number" ? 365 : expiryDays) * 24
  );
  document.cookie =
    name +
    "=" +
    value +
    ";expires=" +
    exdate.toUTCString() +
    ";path=" +
    (path || "/") +
    (domain ? ";domain=" + domain : "") +
    (secure ? ";secure" : "");
};


(() => {
  const $cookiesBanner = document.querySelector(".cookies-eu-banner");
  const $cookiesBannerButton = $cookiesBanner.querySelector("button");

  $cookiesBannerButton.addEventListener("click", () => {
    $cookiesBanner.remove();
  });
})();


const $cookiesBanner = document.querySelector(".cookies-eu-banner");
const $cookiesBannerButton = $cookiesBanner.querySelector("button");
const cookieName = "cookiesBanner";
const hasCookie = getCookie(cookieName);

if (!hasCookie) {
  $cookiesBanner.classList.remove("hidden");
}

$cookiesBannerButton.addEventListener("click", () => {
  setCookie(cookieName, "closed");
  $cookiesBanner.remove();
});

