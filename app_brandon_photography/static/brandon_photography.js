// $(document).ready(function() {
  // $('#navbarDropdown').mouseenter(function() {
    // $('.dropdown-menu').slideToggle(300, "linear");
  // });
  
  // $('.dropdown-menu').mouseleave(function() {
    // $(this).slideToggle(300, "linear");
  // });
// });


var myNav = document.getElementById('mynav');
window.onscroll = function () { 
      "use strict";
      console.log(myNav)
       if (document.body.scrollTop >= 20 || document.documentElement.scrollTop >= 20 ) {
          myNav.classList.add("nav-colored");
          myNav.classList.remove("nav-transparent");
      } 
      else {
          myNav.classList.add("nav-transparent");
          myNav.classList.remove("nav-colored");
      }
};

$(".ongray").hover(
  function(){$(this).addClass("g")},
  function(){$(this).removeClass("g");}
);