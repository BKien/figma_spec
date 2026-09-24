# Euphoria Apparel Shopping

The customer-facing domain of the inspected Euphoria website. Terms describe the supported shopping, account-reading, and cash-on-delivery order experience.

## Language

**Shopper**: A person exploring apparel or reviewing a shopping cart.
_Avoid_: User when the shopping role matters.

**Customer**: The account holder associated with personal information, saved addresses, wishlist entries, and orders.
_Avoid_: Account as a synonym for the person.

**Product**: An apparel design presented with a title, description, imagery, and category.
_Avoid_: SKU, variant.

**Variant**: A particular size-and-color choice for a product.
_Avoid_: Product when a selected apparel option matters.

**Category**: A named grouping used to discover apparel.
_Avoid_: Dress style, which is a separate filter concept.

**Cart**: The shopper's current collection of selected apparel lines before an order is placed.
_Avoid_: Order, checkout.

**Cart line**: A selected variant and its quantity within a cart.
_Avoid_: Product when quantity and chosen options matter.

**Checkout**: The interaction in which the shopper supplies address details, reviews the order summary, and submits the purchase.
_Avoid_: Payment as a synonym for the whole interaction.

**Order**: The recorded purchase presented in confirmation, order history, and order detail.
_Avoid_: Cart, transaction.

**Order line**: The apparel description, chosen options, quantity, and price recorded with an order.
_Avoid_: Current cart line.

**Cash on delivery**: The checkout payment choice labeled Cash on delivery in the design.
_Avoid_: PayPal, card payment.

**Billing address**: The address supplied for billing details.
_Avoid_: Delivery address when the billing role matters.

**Shipping address**: The address used for delivery of an order.
_Avoid_: Billing address unless the shopper selected the same address for both roles.

**Address book**: The collection of saved customer addresses with displayed shipping and billing defaults.
_Avoid_: Profile as a synonym for the collection.

**Wishlist**: The customer's saved product collection displayed in the Wishlist area.
_Avoid_: Cart.

**Recently viewed product**: A product displayed in the Recently Viewed section.
_Avoid_: Wishlist entry.

**Order event**: A dated progress entry shown with an order.
_Avoid_: Status when referring to an individual historical entry.

**Reset email request**: The request acknowledged by the Check Email screen.
_Avoid_: Password reset completion.
