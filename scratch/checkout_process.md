# Checkout Process

1. Cart -> Checkout View
    - Login/Register or Enter an Email (as Guest)
    - Shipping Address
    - Billing Info
        - Billing Address
        - Credit Card / Payment

2. Billing App
    - Billing Profile
        - User or Email (Guest Email)
        - Generating payment processor token (Stripe or Braintree)

3. Orders / Invoices App
    - Connecting the Billing Profile
    - Shipping / Billing Address
    - Cart
    - Status -- Shipped? Cancelled?