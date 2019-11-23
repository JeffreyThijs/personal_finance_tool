$('.navbar-nav .nav-link').click(function(){
    console.log("hello");
    $('.navbar-nav .nav-link').removeClass('active');
    $(this).addClass('active');
})

