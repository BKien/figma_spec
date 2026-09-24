# Figma Source Manifest

- Package: Euphoria Ecommerce Apparels.
- Scope: the user-supplied copy of the Euphoria apparel ecommerce website template.
- Design URL: https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria---Ecommerce--Apparels--Website-Template--Community---Copy-
- Design file key: `WcpUgAYaQJA4J00rMaMgj8`.
- Original Community listing: https://www.figma.com/community/file/1250348068101895773/euphoria-ecommerce-apparels-website-template
- Community resource ID: `1250348068101895773`; distinct from the design file key.
- Original template publisher: Jhanvi Shah.
- Audit date: 2026-09-24.
- Document pages enumerated: `0:1` Webpage and `105:179` Styleguide.
- Inspected node boundary: metadata subtree of Webpage `0:1`, plus browser inspection of Checkout `235:1056` and Add Address `279:1003`.
- Source revision: unavailable; this is a dated observation, not a pinned Figma version.

## Evidence and limits

The Figma connector successfully returned the Webpage node hierarchy, screen names, dimensions, positions, and text-layer names. The full returned XML is saved in [page-0.xml](evidence/page-0.xml). The [screen inventory](evidence/screen-inventory.json) is derived from that XML. All listed screens are top-level frames parented by `0:1`.

Visibility flags, complete instance text overrides, prototype transitions, interactive behavior, and hidden-state completeness were not exposed by this metadata. Text-layer names are evidence of design content; they are not a full export of rendered characters. The connector reached its Starter-plan call limit before Styleguide inspection and additional screenshots. Browser canvas inspection supplied readable views of the checkout and address fields and action labels. Styleguide was enumerated but not inspected. No mobile frame was found among the 20 top-level Webpage frames; this does not establish that no mobile design exists elsewhere.

The earlier Community promotional image is contextual evidence only. It is not the source for node-level requirements in this package. No design nodes were changed.

## Screen inventory

| Screen | Node ID | Dimensions |
| --- | --- | --- |
| [Product detail Page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=1-2) | `1:2` | 1440 x 3338 |
| [Products List page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=64-33) | `64:33` | 1440 x 4894 |
| [home page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=85-1544) | `85:1544` | 1440 x 7819 |
| [Sign up page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=167-524) | `167:524` | 1440 x 1063 |
| [Sign In Page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=178-381) | `178:381` | 1440 x 1067 |
| [Reset Password](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=245-588) | `245:588` | 1440 x 1067 |
| [Check Email](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=270-721) | `270:721` | 1440 x 1067 |
| [Verification](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=270-792) | `270:792` | 1440 x 1067 |
| [Create New Password](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=250-710) | `250:710` | 1440 x 1067 |
| [Cart Page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=181-393) | `181:393` | 1440 x 2204 |
| [Empty Cart](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=190-423) | `190:423` | 1440 x 1584 |
| [Checkout](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=235-1056) | `235:1056` | 1440 x 3263 |
| [Confirmed Order](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=273-839) | `273:839` | 1440 x 1584 |
| [Error Page](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=274-1030) | `274:1030` | 1440 x 1479 |
| [Contact Details](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=275-1168) | `275:1168` | 1440 x 2159 |
| [Add Address](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=279-1003) | `279:1003` | 1440 x 2143 |
| [wishlist](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=290-855) | `290:855` | 1440 x 1767 |
| [Empty wishlist](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=299-1027) | `299:1027` | 1440 x 2195 |
| [My Order](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=290-1372) | `290:1372` | 1440 x 2143 |
| [Order Details](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=295-949) | `295:949` | 1440 x 1887 |

## Browser observation record

Checkout: First Name, Last Name, Country / Region, Company Name, Street Address, Apt/suite/unit, City, State, Postal Code, Phone; Continue to delivery; Save my information for a faster checkout; Same as Billing address / Use a different shipping address; delivery charge; Credit Card; Cash on delivery; Paypol; Pay Now. The card area shows card number, name, expiration, and security-code fields. Provider processing and results were not observed.

Add Address: the same address identity fields, Delivery Instruction, default shipping and default billing checkboxes, Save, and Cancel. The address book screen provides the corresponding saved-address display. No prototype edge was verified between them.

## Source chronology

The original Community link required browser authentication to open a design. The user then supplied this design copy. The connector initially required reauthentication, which the user completed; page enumeration and Webpage metadata subsequently succeeded. Later connector requests reported the Starter-plan call limit. These limits are recorded rather than treated as evidence of absent features.
