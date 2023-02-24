$(document).ready(function() {
    $(".link").click(function(){
        window.location.href = $(this).attr('data-url')
    });

    $(".filter-button").click(function() {
        var value = $(this).attr('data-filter');

        if (value == "all") {
            //$('.filter').removeClass('hidden');
            $('.filter').show('1000');
        } else {
            $('.filter[filter-item="' + value + '"]').removeClass('hidden');
            $(".filter").not('.filter[filter-item="' + value + '"]').addClass('hidden');
            $(".filter").not('.' + value).hide('3000');
            $('.filter').filter('.' + value).show('3000');
        }
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});

$('.slider-for').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.slider-nav'
});
$('.slider-nav').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    dots: true,
    focusOnSelect: true,
    responsive: [
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 1,
          }
        },
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 2,
          }
        }
      ]
});

$body = $("body");

$(document).on({
    ajaxStart: function () {
        $body.addClass("loading");
    },
    ajaxStop: function () {
        $body.removeClass("loading");
    },
});

(function ($) {
    $(document).on("submit", "form.ajax", function (e) {
        e.preventDefault();
        var $this = $(this);
        var data = new FormData(this);
        var action_url = $this.attr("action");
        var isReset = $this.hasClass("reset");
        var isReload = $this.hasClass("reload");
        var isRedirect = $this.hasClass("redirect");

        $.ajax({
            url: action_url,
            type: "POST",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            dataType: "json",

            success: function (data) {
                var status = data.status;
                var title = data.title;
                var message = data.message;
                var pk = data.pk;
                var redirect = data.redirect;
                var redirect_url = data.redirect_url;

                if (status == "true") {
                    if (title) {
                        title = title;
                    } else {
                        title = "Success";
                    }

                    Swal.fire({
                        title: title,
                        text: message,
                        icon: "success",
                    }).then(function () {
                        if (isRedirect) {
                            window.location.href = redirect_url;
                        }
                        if (isReload) {
                            window.location.reload();
                        }
                        if (isReset) {
                            window.location.reset();
                        }
                    });
                } else {
                    if (title) {
                        title = title;
                    } else {
                        title = "An Error Occurred";
                    }
                    Swal.fire({
                        title: title,
                        text: message,
                        icon: "error",
                    });
                }
            },
            error: function (data) {
                var title = "An error occurred";
                var message = "something went wrong";
                Swal.fire({
                    title: title,
                    text: message,
                    icon: "error",
                });
            },
        });
    });

    $(document).on("click", ".p-cart-btn", function (e) {
        e.preventDefault();
        $this = $(this);
        var text = $this.attr("data-text");
        var type = "success";
        var id = $this.attr("data-id");
        var url = $this.attr("data-url");

        $.ajax({
            type: "GET",
            url: url,
            dataType: "json",
            data: { pk: id },

            success: function (data) {
                var message = data.message;
                var status = data.status;
                var reload = data.reload;
                var redirect = data.redirect;
                var redirect_url = data.redirect_url;
                var title = data.title;

                if (status == "true") {
                    if (title) {
                        title = title;
                    } else {
                        title = "Success";
                    }

                    Swal.fire({
                        title: title,
                        text: message,
                        icon: "success",
                    }).then(function () {
                        if (redirect == "true") {
                            window.location.href = redirect_url;
                        }
                        if (reload == "true") {
                            window.location.reload();
                        }
                    });
                } else {
                    if (title) {
                        title = title;
                    } else {
                        title = "An Error Occurred";
                    }
                    Swal.fire({ title: title, text: message, icon: "error" });
                }
            },
            error: function (data) {
                var title = "An error occurred";
                var message = "An error occurred. Please try again later.";
                Swal.fire({ title: title, text: message, icon: "error" });
            },
        });
    });

    $(".search-wrapper > a").on("click", function (e) {
        e.preventDefault();
        $(".search-form").toggleClass("active");
    });

    $(".settings-wrapper > a").on("click", function (e) {
        e.preventDefault();
        $(".settings-content").toggleClass("active");
    });

    $(".cart-wrapper > a").on("click", function (e) {
        e.preventDefault();
        $(".cart-item-wrapper").toggleClass("active");
    });



})(jQuery);

jQuery('<div class="quantity-button quantity-up">+</div>').insertAfter(".quantity input");
jQuery('<div class="quantity-button quantity-down">-</div>').insertBefore(".quantity input");
jQuery(".quantity").each(function () {
    var spinner = jQuery(this),
        input = spinner.find('input[type="number"]'),
        btnUp = spinner.find(".quantity-up"),
        btnDown = spinner.find(".quantity-down"),
        min = input.attr("min"),
        max = input.attr("max");

    btnUp.click(function () {
        var oldValue = parseFloat(input.val());
        if (oldValue >= max) {
            var newVal = oldValue;
        } else {
            var newVal = oldValue + 1;
        }
        spinner.find("input").val(newVal);
        spinner.find("input").trigger("change");
    });

    btnDown.click(function () {
        var oldValue = parseFloat(input.val());
        if (oldValue <= min) {
            var newVal = oldValue;
        } else {
            var newVal = oldValue - 1;
        }
        spinner.find("input").val(newVal);
        spinner.find("input").trigger("change");
    });
});


document.addEventListener('readystatechange', event => {
    if (event.target.readyState === "complete") {
        var clockdiv = document.getElementsByClassName("product-card");
        var countDownDate = new Array();
        for (var i = 0; i < clockdiv.length; i++) {
            countDownDate[i] = new Array();
            countDownDate[i]['el'] = clockdiv[i];
            countDownDate[i]['time'] = new Date(clockdiv[i].getAttribute('data-date')).getTime();
            countDownDate[i]['days'] = 0;
            countDownDate[i]['hours'] = 0;
            countDownDate[i]['seconds'] = 0;
            countDownDate[i]['minutes'] = 0;
        }

        var countdownfunction = setInterval(function() {
            for (var i = 0; i < countDownDate.length; i++) {
                var now = new Date().getTime();
                var distance = countDownDate[i]['time'] - now;
                countDownDate[i]['days'] = Math.floor(distance / (1000 * 60 * 60 * 24));
                countDownDate[i]['hours'] = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                countDownDate[i]['minutes'] = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                countDownDate[i]['seconds'] = Math.floor((distance % (1000 * 60)) / 1000);

                if (distance < 0) {
                    countDownDate[i]['el'].querySelector('.days').innerHTML = 0;
                    countDownDate[i]['el'].querySelector('.hours').innerHTML = 0;
                    countDownDate[i]['el'].querySelector('.minutes').innerHTML = 0;
                    countDownDate[i]['el'].querySelector('.seconds').innerHTML = 0;
                } else {
                    countDownDate[i]['el'].querySelector('.days').innerHTML = countDownDate[i]['days'];
                    countDownDate[i]['el'].querySelector('.hours').innerHTML = countDownDate[i]['hours'];
                    countDownDate[i]['el'].querySelector('.minutes').innerHTML = countDownDate[i]['minutes'];
                    countDownDate[i]['el'].querySelector('.seconds').innerHTML = countDownDate[i]['seconds'];
                }

            }
        }, 1000);
    }
});



$(document).on('click', '.ajax_button', function(e) {
    e.preventDefault();
    $this = $(this);
    var url = $this.attr('data-url');
    var id = $this.attr('data-id');
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        data: {
            pk: id
        },
        success: function(data) {
            var message = data.message;
            var status = data.status;
            var reload = data.reload;
            var redirect = data.redirect;
            var redirect_url = data.redirect_url;
            var title = data.title;

            if (status == "true") {
                window.location.reload();
            } else {
                title = "An Error Occurred";
                Swal.fire({
                    title: title,
                    icon: "error"
                });
            }
        },
        error: function(data) {
            var title = "An error occurred";
            var message = "An error occurred. Please try again later.";
            Swal.fire({
                title: title,
                text: message,
                icon: "error"
            });
        }
    });
});
