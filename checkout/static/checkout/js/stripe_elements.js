/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
	base: {
		color: "#000",
		fontWeight: "500",
		fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
		fontSmoothing: "antialiased",
		fontSize: "16px",
		"::placeholder": {
			color: "#aab7c4",
		},
	},
	// Colors adjusted to match bootstrap danger class
	invalid: {
		color: "#dc3545",
		iconColor: "#dc3545",
	},
};
var card = elements.create("card", { style: style });
card.mount("#card-element");

// Handle realtime validation errors on the card element

card.addEventListener("change", function (event) {
	var errorDiv = document.getElementById("card-errors");
	if (event.error) {
		var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
            `;
		$(errorDiv).html(html);
	} else {
		errorDiv.textContent = "";
	}
});

// Handle form submit
var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
	ev.preventDefault();
	// Disable card element & submit button to prevent multiple submissions
	card.update({ disabled: true });
	//trigger overlay & fade out form when submit button is clicked
	$("#submit-button").attr("disabled", true);
	$("#payment-form").fadeToggle(100);
	$("#loading-overlay").fadeToggle(100);
	// If the client secret was rendered server-side as a data-secret attribute
	// on the <form> element, you can retrieve it here by calling `form.dataset.secret`
	stripe
		.confirmCardPayment(clientSecret, {
			payment_method: {
				card: card,
			},
		})
		.then(function (result) {
			if (result.error) {
				// Show error to your customer (e.g., insufficient funds)
				var errorDiv = document.getElementById("card-errors");
				var html = `
					<span class="icon" role="alert">
						<i class="fas fa-times"></i>
					</span>
					<span>${result.error.message}</span>`;
				$(errorDiv).html(html);
				//trigger overlay & fade out form when submit button is clicked
				$("#payment-form").fadeToggle(100); 
				$("#loading-overlay").fadeToggle(100);
				card.update({ disabled: false });
				$("#submit-button").attr("disabled", false);
			} else {
				// The payment has been processed!
				if (result.paymentIntent.status === "succeeded") {
					form.submit();
					// Show a success message to your customer
					// There's a risk of the customer closing the window before callback
					// execution. Set up a webhook or plugin to listen for the
					// payment_intent.succeeded event that handles any business critical
					// post-payment actions.
				}
			}
		});
});
