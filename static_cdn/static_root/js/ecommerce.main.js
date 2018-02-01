$(document).ready(function () {
  let stripeFormModule = $('.stripe-payment-form');
  let stripeModuleToken = stripeFormModule.attr('data-token');
  let stripeModuleNextUrl = stripeFormModule.attr('data-next-url');
  let stipeModuleBtnTitle = stripeFormModule.attr('data-btn-title') || 'Add card';

  let stripeTemplate = $.templates("#stripeTemplate");
  let stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    btnTitle: stipeModuleBtnTitle
  };
  let stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext);

  stripeFormModule.html(stripeTemplateHtml);

  let paymentForm = $('.payment-form');

  if (paymentForm.length > 1) {
    alert('Only one payment form is allowed per page');
    paymentForm.css('display', 'none')
  } else if (paymentForm.length === 1) {

    const pubKey = paymentForm.attr('data-token');
    const nextUrl = paymentForm.attr('data-next-url');

    // Create a Stripe client
    let stripe = Stripe(pubKey);

    // Create an instance of Elements
    let elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    let style = {
      base: {
        color: '#32325d',
        lineHeight: '18px',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };

    // Create an instance of the card Element
    let card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      let displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });

    // Handle form submission
    let form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error
          let errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Send the token to your server
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });

    function redirectToNext(nextPath, timeoffset) {
      if (nextPath) {
        setTimeout(function() {
          window.location.href = nextPath;
        }, timeoffset);
      }
    }

    function stripeTokenHandler(nextUrl, token) {
      const paymentMethodEndpoint = '/billing/payment-method/create/';
      let data = {
        'token': token.id
      };
      $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: 'POST',
        success: function(data) {
          let successMsg = data.message || 'Success! Your card was added.';
          console.log(data);
          card.clear();
          if (nextUrl){
            successMsg = successMsg + "<br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
          }
          if ($.alert) {
            $.alert(successMsg);
          } else {
            alert(successMsg);
          }
          redirectToNext(nextUrl, 1500);
        },
        error: function(error) {
          console.log(error);
        }
      })
    }
  }
});
