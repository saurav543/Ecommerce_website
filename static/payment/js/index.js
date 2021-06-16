var stripe = Stripe(STRIPE_PUBLISHABLE_KEY)
    // console.log(stripe)
var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');
// console.log(clientsecret);

var elements = stripe.elements();
// console.log(elements);

var style = {
    base: {
        color: "bg-light",
        lineHeight: '2.4',
        fontSize: '16px'
    }
}

var card = elements.create("card", { style: style });
card.mount("#card-element");
// var card = elements.create("card",{style:style})
card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = None;
        $('#card-errors').removeClass('alert alert-info');
    }
});


var form = document.getElementById('payment-form');
form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    console.log("hello form");
    var custName = document.getElementById('customer').value;
    var custAdd = document.getElementById('custAdd').value;
    var custAdd2 = document.getElementById('custAdd2').value;
    var postcode = document.getElementById('postcode').value;
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add/",
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post',
        },
        success: function(response) {
            console.log(response);
            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            line1: custAdd,
                            line2: custAdd2
                        },
                        name: custName
                    },
                }
            }).then(function(result) {
                if (result.error) {
                    console.log('payment error');
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        window.location.replace("http://127.0.0.1:8000/checkout/orderplaced/");
                    }
                }
            });
        },
        error: function(xhr, errmsg, err) {

        },
    });

})