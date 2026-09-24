from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
KEY = 'WcpUgAYaQJA4J00rMaMgj8'
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + '\n', encoding='utf-8')
def numbered(items):
    return '\n'.join(f'{i}. {x}' for i,x in enumerate(items,1))
def figma(node):
    return f'https://www.figma.com/design/{KEY}/Euphoria?node-id={node.replace(":", "-")}'

# Schemas are shared wire vocabulary; tuples are name, type, description, example.
SCHEMAS = {
 'Money': [('amount','string','Decimal monetary amount.','29.00'),('currency','string','Currency code.','USD')],
 'ProductCard': [('id','string','Product identifier.','prd_01'),('title','string','Display title.','Printed shirt'),('brand','string','Brand display name.','Euphoria'),('imageUrl','string','Image URI.','https://example.com/shirt.jpg'),('price','Money','Displayed price.',{'amount':'29.00','currency':'USD'})],
 'Category': [('id','string','Category identifier.','cat_tops'),('name','string','Category display name.','Tops'),('imageUrl','string','Image URI.','https://example.com/tops.jpg')],
 'Promotion': [('id','string','Promotion identifier.','promo_01'),('heading','string','Display heading.','New arrivals'),('imageUrl','string','Image URI.','https://example.com/banner.jpg'),('targetCategoryId','string?','Category identifier or null.',None)],
 'Testimonial': [('id','string','Testimonial identifier.','test_01'),('name','string','Display name.','Sample customer'),('body','string','Displayed feedback.','Comfortable fabric.'),('rating','number','Displayed rating.',4)],
 'Storefront': [('promotions','Promotion[]','Promotional sections.',[]),('categories','Category[]','Category sections.',[]),('featured','ProductCard[]','Featured product cards.',[]),('testimonials','Testimonial[]','Displayed feedback.',[])],
 'Facet': [('value','string','Selection value.','black'),('label','string','Display label.','Black')],
 'CatalogResult': [('items','ProductCard[]','Product cards.',[]),('categories','Facet[]','Category choices.',[]),('colors','Facet[]','Color choices.',[]),('sizes','Facet[]','Size choices.',[]),('styles','Facet[]','Dress style choices.',[]),('total','integer','Result count.',0)],
 'Variant': [('id','string','Variant identifier.','var_01'),('size','string','Size display value.','M'),('color','string','Color display value.','Black'),('price','Money','Variant price.',{'amount':'29.00','currency':'USD'}),('purchasable','boolean','Public selection state.',True)],
 'Attribute': [('name','string','Attribute label.','Fabric'),('value','string','Attribute display value.','Cotton')],
 'ProductDetail': [('product','ProductCard','Main product card.',{}),('description','string','Description text.','Printed cotton shirt.'),('images','string[]','Image URIs.',[]),('rating','number','Displayed rating.',3.5),('commentCount','integer','Displayed comment count.',120),('questionCount','integer','Displayed question count.',4),('attributes','Attribute[]','Product attributes.',[]),('variants','Variant[]','Variant choices.',[]),('similarProducts','ProductCard[]','Related cards.',[])],
 'CartLine': [('id','string','Cart line identifier.','cl_01'),('variantId','string','Variant identifier.','var_01'),('title','string','Product display title.','Printed shirt'),('imageUrl','string','Image URI.','https://example.com/shirt.jpg'),('color','string','Selected color.','Black'),('size','string','Selected size.','M'),('quantity','integer','Displayed quantity.',1),('unitPrice','Money','Unit amount.',{'amount':'29.00','currency':'USD'}),('lineTotal','Money','Line amount.',{'amount':'29.00','currency':'USD'})],
 'Cart': [('id','string','Cart identifier.','cart_01'),('version','integer','Cart revision value.',1),('items','CartLine[]','Cart lines.',[]),('subtotal','Money','Displayed subtotal.',{'amount':'29.00','currency':'USD'})],
 'AddressInput': [('firstName','string','Given name.','Alex'),('lastName','string','Family name.','Lee'),('country','string','Country or region.','US'),('company','string?','Company text or null.',None),('street','string','Street address.','10 Sample Street'),('unit','string?','Apartment text or null.',None),('city','string','City text.','Sample City'),('state','string','State or region text.','CA'),('postalCode','string','Postal code text.','90001'),('phone','string','Telephone text.','+12025550123'),('instructions','string?','Delivery instruction text or null.',None)],
 'Address': [('id','string','Address identifier.','addr_01'),('details','AddressInput','Address fields.',{}),('defaultShipping','boolean','Displayed default shipping flag.',False),('defaultBilling','boolean','Displayed default billing flag.',False)],
 'Profile': [('id','string','Customer identifier.','cust_01'),('name','string','Customer display name.','Alex Lee'),('email','string','Email address.','alex@example.com'),('phone','string?','Telephone text or null.',None)],
 'AddressBook': [('version','integer','Address book revision value.',1),('items','Address[]','Saved address entries.',[])],
 'CheckoutRequest': [('cartVersion','integer','Cart revision value.',1),('billing','AddressInput','Billing fields.',{}),('shipping','AddressInput?','Shipping fields or null.',None),('sameAsBilling','boolean','Address choice value.',True)],
 'CheckoutPreview': [('cartVersion','integer','Cart revision value.',1),('items','CartLine[]','Order summary lines.',[]),('subtotal','Money','Displayed subtotal.',{'amount':'29.00','currency':'USD'}),('discount','Money','Displayed savings.',{'amount':'0.00','currency':'USD'}),('shipping','Money','Delivery amount.',{'amount':'5.00','currency':'USD'}),('total','Money','Displayed order total.',{'amount':'34.00','currency':'USD'}),('estimatedDelivery','string?','ISO 8601 date or null.',None)],
 'CheckoutSubmission': [('checkout','CheckoutRequest','Checkout fields.',{}),('displayedTotal','Money','Displayed amount value.',{'amount':'34.00','currency':'USD'}),('paymentMethod','string','Public enum: COD.','COD')],
 'OrderSummary': [('id','string','Order identifier.','ord_01'),('number','string','Display order number.','EU-1001'),('placedAt','string','ISO 8601 timestamp.','2026-09-24T02:00:00Z'),('status','string','Public enum: PLACED, IN_PROGRESS, SHIPPED, DELIVERED, CANCELLED.','PLACED'),('paymentMethod','string','Public enum: COD.','COD'),('estimatedDelivery','string?','ISO 8601 date or null.',None),('total','Money','Order amount.',{'amount':'34.00','currency':'USD'}),('items','CartLine[]','Order line display fields.',[])],
 'OrderEvent': [('status','string','Public enum: PLACED, IN_PROGRESS, SHIPPED, DELIVERED, CANCELLED.','PLACED'),('occurredAt','string','ISO 8601 timestamp.','2026-09-24T02:00:00Z'),('message','string','Timeline display message.','Order received.')],
 'OrderDetail': [('order','OrderSummary','Order summary.',{}),('events','OrderEvent[]','Timeline entries.',[])],
 'OrderResult': [('items','OrderSummary[]','Order summaries.',[])],
 'Wishlist': [('items','ProductCard[]','Saved product cards.',[]),('recentlyViewed','ProductCard[]','Recently viewed cards.',[])],
 'Accepted': [('accepted','boolean','Public acknowledgement.',True)],
 'Confirmation': [('orderId','string','Order identifier.','ord_01'),('message','string','Confirmation display message.','Your Order is Confirmed')],
}

UCS = json.loads((ROOT / 'scripts/use-cases.json').read_text(encoding='utf-8'))
assert 17 <= len(UCS) <= 20, 'The package requires 17-20 use cases.'
assert all(len(u['rules']) >= 7 for u in UCS), 'Every use case requires at least seven BRs.'
SCHEMAS['Cart'] += [('shippingEstimate','Money','Displayed shipping estimate.',{'amount':'5.00','currency':'USD'}),('totalEstimate','Money','Displayed total estimate.',{'amount':'34.00','currency':'USD'})]

for uc in UCS:
    uid=f'UC-{uc["n"]:02}'
    rules=[]
    for i,(source,context,name,predicate) in enumerate(uc['rules'],1):
        kind,label=name.split(' ',1)
        rules.append(f'```ocl\n-- BR-{uid}-{i:02}\n-- Source: {source}\n{context}\n{kind} BR_{uid.replace("-","_")}_{i:02}_{label}:\n  {predicate}\n```')
    model=f'```plantuml\n@startuml\nclass {uc["service"]} {{\n  +{uc["operation"]}\n}}\n'
    if uc['service']=='CheckoutService': model+='class CheckoutService {\n  currency: String\n  deliveryCharge: Real\n}\n'
    model+='@enduml\n```'
    text=f'''# {uid} — {uc['name']}

### Description

{uc['desc']}

### Actors

Primary: {uc['actor']}. Supporting: web client and application service.

### Priority

{uc['priority']}.

### Trigger

**TRG-{uid}-01** — {uc['trigger']}

### Preconditions

- **PRE-{uid}-01** — {uc['pre']}

### Postconditions

- **POST-{uid}-01** — {uc['post']}

### Basic Flow

{numbered(uc['basic'])}

### Alternative Flows

#### AF-{uid}-01

{numbered(uc['alt'])}

### Exception Flows

#### EF-{uid}-01

{numbered(uc['err'])}

### UML Model

Vocabulary imports: [shared domain model](shared-domain-model.md). This local service model extends that vocabulary.

{model}

### Business Rules

{chr(10).join(rules)}

### Related UI

{chr(10).join(f'- [Figma node {n}]({figma(n)})' for n in uc['nodes'])}

### Related APIs

{chr(10).join(f'- [API-{a}](../api/api-{a.lower()}.md)' for a in uc['api'])}

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../ASSUMPTIONS.md) and [coverage](../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.
'''
    write(f'uc/uc-{uc["n"]:02}-{uc["slug"]}.md',text)

write('uc/README.md',f'# Use Case Index\n\n{len(UCS)} use cases; {sum(len(u["rules"]) for u in UCS)} business rules. Every use case has at least seven separately identified OCL rules. Conditions and interaction flows contain no rule references or policy definitions.\n\n'+ '\n'.join(f'- [UC-{u["n"]:02} — {u["name"]}](uc-{u["n"]:02}-{u["slug"]}.md) — {len(u["rules"])} BRs' for u in UCS)+'\n\n[Shared domain model](shared-domain-model.md)\n')

if __name__ == '__main__':
    print(f'Generated {len(UCS)} use cases.')

def sample(schema, depth=0):
    out={}
    for name,typ,desc,example in SCHEMAS[schema]:
        base=typ.rstrip('?')
        if example == {} and base in SCHEMAS:
            example=sample(base,depth+1)
        out[name]=example
    if schema=='Cart': out['items']=[sample('CartLine')]
    if schema=='CatalogResult': out.update(items=[sample('ProductCard')],total=1)
    if schema=='ProductDetail': out['variants']=[sample('Variant')]
    if schema=='CheckoutPreview': out['items']=[sample('CartLine')]
    if schema=='OrderSummary': out['items']=[sample('CartLine')]
    if schema=='OrderDetail': out['events']=[sample('OrderEvent')]
    if schema=='AddressBook': out['items']=[sample('Address')]
    if schema=='OrderResult': out['items']=[sample('OrderSummary')]
    return out

def field(name,typ,desc,example,required=True,default=None):
    nullable=typ.endswith('?')
    typ=typ.rstrip('?')
    if example == {} and typ in SCHEMAS:
        example=sample(typ)
    syntax='JSON type only.'
    if 'Decimal' in desc or 'decimal' in desc: syntax='Decimal string syntax: ^-?[0-9]+(?:\\.[0-9]+)?$.'
    if 'Currency code' in desc: syntax='Three uppercase ASCII letters.'
    if 'media type' in desc: syntax='HTTP media type syntax; allowed value application/json.'
    if 'HTTP cookie' in desc: syntax='HTTP Cookie header encoding.'
    if 'enum:' in desc: syntax='Membership in the public enum stated in the description.'
    elif 'ISO 8601 timestamp' in desc: syntax='ISO 8601 date-time syntax.'
    elif 'ISO 8601 date' in desc: syntax='ISO 8601 date syntax.'
    elif 'URI' in desc: syntax='Absolute URI syntax.'
    elif 'Email address' in desc: syntax='Email address syntax.'
    elif typ in SCHEMAS or typ.rstrip('[]') in SCHEMAS: syntax='Object or array shape defined in common-contract.md.'
    return f'''### `{name}`

- Type: {typ}.
- Required: {'Yes' if required else 'No'}.
- Nullable: {'Yes' if nullable else 'No'}.
- Default: {json.dumps(default) if default is not None else 'None'}.
- Validation: {syntax}
- Description: {desc}
- Example: `{json.dumps(example,ensure_ascii=True)}`.
'''

common='''# Common Wire Contract

These proposed HTTP contracts describe a new application boundary. No deployed Euphoria API was inspected. Field names, routes, envelopes, transport authentication, and public codes are implementation assumptions.

## Transport

HTTPS; JSON UTF-8. Success bodies contain `data` and `requestId`. Error bodies contain `error` and `requestId`; `error` contains `code` and `message`. `requestId` is an opaque string. All timestamps use ISO 8601 UTC text; dates use YYYY-MM-DD. Identifiers are opaque JSON strings. Monetary amounts use decimal strings and currency uses a currency-code string. No binary floating-point number is used for money on the wire.

## Object definitions

Each object below is reusable by reference from the individual contracts. Every field is required unless its individual definition says otherwise. Nullable fields are sent as JSON null. Arrays are JSON arrays. Example values illustrate transport shape. This document defines no domain decisions.

'''
for schema,fields in SCHEMAS.items():
    common+=f'## {schema}\n\n'
    for args in fields: common+=field(*args)+'\n'
write('api/common-contract.md',common)

APIS=[
 ('STOREFRONT','Read storefront','GET','/v1/storefront',False,None,'Storefront',[],[]),
 ('CATALOG','Read product listing','GET','/v1/products',False,None,'CatalogResult',[],[
  ('categoryId','string?','Category selection value.',None,False),('colors','string[]','Repeated query parameter, for example colors=black&colors=blue.',[],False),('sizes','string[]','Repeated query parameter, for example sizes=M&sizes=L.',[],False),('styles','string[]','Repeated query parameter, for example styles=Casual.',[],False),('minAmount','string','Decimal text value.','0.00',False),('maxAmount','string?','Decimal text value or omitted.',None,False),('sort','string','Public enum: NEW, RECOMMENDED.','RECOMMENDED',False)]),
 ('PRODUCT','Read product detail','GET','/v1/products/{productId}',False,None,'ProductDetail',[('productId','string','Opaque product identifier.','prd_01')],[]),
 ('CART','Read cart','GET','/v1/me/cart',True,None,'Cart',[],[]),
 ('CHECKOUT-PREVIEW','Read checkout summary','POST','/v1/me/checkout/preview',True,'CheckoutRequest','CheckoutPreview',[],[]),
 ('ORDER-CREATE','Submit cash-on-delivery order','POST','/v1/me/orders',True,'CheckoutSubmission','Confirmation',[],[]),
 ('RESET-REQUEST','Request reset email','POST','/v1/password-reset-requests',False,'ResetEmail','Accepted',[],[]),
 ('PROFILE','Read profile','GET','/v1/me/profile',True,None,'Profile',[],[]),
 ('ADDRESSES','Read address book','GET','/v1/me/addresses',True,None,'AddressBook',[],[]),
 ('ADDRESS-CREATE','Add address','POST','/v1/me/addresses',True,'NewAddress','AddressBook',[],[]),
 ('WISHLIST','Read wishlist','GET','/v1/me/wishlist',True,None,'Wishlist',[],[]),
 ('ORDERS','Read order history','GET','/v1/me/orders',True,None,'OrderResult',[],[('tab','string','Public enum: ACTIVE, CANCELLED, COMPLETED.','ACTIVE',False)]),
 ('ORDER-DETAIL','Read order detail','GET','/v1/me/orders/{orderId}',True,None,'OrderDetail',[('orderId','string','Opaque order identifier.','ord_01')],[]),
]
SCHEMAS['ResetEmail']=[('email','string','Email address.','alex@example.com')]
SCHEMAS['NewAddress']=[('details','AddressInput','Address fields.',{}),('defaultShipping','boolean','Checkbox value.',False),('defaultBilling','boolean','Checkbox value.',False),('expectedVersion','integer','Address book revision value.',1)]
# Append the two operation-specific object definitions.
with (ROOT/'api/common-contract.md').open('a',encoding='utf-8') as f:
    for schema in ['ResetEmail','NewAddress']:
        f.write(f'\n## {schema}\n\n')
        for args in SCHEMAS[schema]: f.write(field(*args)+'\n')

for aid,name,method,path,auth,body,result,params,queries in APIS:
    related=[u for u in UCS if aid in u['api']]
    txt=f'''# API-{aid} — {name}

## API ID

`API-{aid}`

## API Name

{name}.

## Related Use Case IDs

{chr(10).join(f'- `UC-{u["n"]:02}` — [specification](../uc/uc-{u["n"]:02}-{u["slug"]}.md)' for u in related)}

## Method

`{method}`

## Path

`{path}`

## Description

{name} for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

## Authentication

{'Cookie named euphoria_session.' if auth else 'None.'}

## Authorization

{'Access outcomes are represented by HTTP 401 and HTTP 403.' if auth else 'Public operation.'}

## Request Headers

'''
    txt+=field('Accept','string','Response media type.','application/json')
    if body: txt+='\n'+field('Content-Type','string','Request media type.','application/json')
    if auth: txt+='\n'+field('Cookie','string','HTTP cookie encoding; euphoria_session carries an opaque value.','euphoria_session=opaque-session-value')
    if auth and method!='GET': txt+='\n'+field('X-CSRF-Token','string','Opaque request header value.','opaque-csrf-value')
    if aid=='ORDER-CREATE': txt+='\n'+field('Idempotency-Key','string','Opaque request key.','request_01')
    txt+='\n## Path Parameters\n\n'+ ('\n'.join(field(*a) for a in params) if params else 'None.\n')
    txt+='\n## Query Parameters\n\n'+ ('\n'.join(field(*a) for a in queries) if queries else 'None.\n')
    txt+='\n## Request Body\n\n'
    if body:
        txt+=field('body',body,f'JSON object; full {body} field definitions are in common-contract.md.',sample(body))
        txt+='\n```json\n'+json.dumps(sample(body),indent=2)+'\n```\n'
    else: txt+='None.\n'
    status=202 if aid=='RESET-REQUEST' else 200
    txt+=f'\n## Success Response — HTTP {status}\n\nContent-Type: application/json.\n\n'
    txt+=field('data',result,f'{result} object; all nested fields are defined in common-contract.md.',sample(result))
    txt+='\n'+field('requestId','string','Opaque response correlation identifier.','req_01')
    txt+='\n```json\n'+json.dumps({'data':sample(result),'requestId':'req_01'},indent=2)+'\n```\n'
    errors=[(400,'MALFORMED_REQUEST','Malformed wire input.')]
    if auth: errors += [(401,'AUTHENTICATION_REJECTED','Rejected authentication context.'),(403,'ACCESS_REJECTED','Rejected access context.')]
    if params or aid=='CATALOG': errors += [(404,'RESOURCE_UNAVAILABLE','Unavailable resource response.')]
    if aid in ['CHECKOUT-PREVIEW','ORDER-CREATE','ADDRESS-CREATE']: errors += [(409,'OPERATION_CONFLICT','Operation conflict.'),(422,'REQUEST_REJECTED','Operation rejected.')]
    if aid=='CATALOG': errors += [(422,'REQUEST_REJECTED','Operation rejected.')]
    if aid=='RESET-REQUEST': errors += [(429,'REQUEST_LIMITED','Request temporarily limited.')]
    errors += [(503,'SERVICE_UNAVAILABLE','Temporary service failure.')]
    for status,code,trigger in errors:
        txt+=f'\n## Error Response — HTTP {status}\n\n- Trigger: {trigger}\n\nContent-Type: application/json.\n\n'
        txt+=field('error','object','Error object with code and message.',{'code':code,'message':trigger})
        txt+='\n'+field('error.code','string',f'Public enum: {code}.',code)
        txt+='\n'+field('error.message','string','Display message.',trigger)
        txt+='\n'+field('requestId','string','Opaque response correlation identifier.','req_01')
    txt+='\n## Notes\n\nThis is a proposed contract, not a discovered endpoint. Field definitions in [common wire definitions](common-contract.md) are part of this contract. There are no pagination parameters in this version. All declared errors use the stated JSON envelope.\n'
    write(f'api/api-{aid.lower()}.md',txt)
write('api/README.md','# API Index\n\n[Common wire definitions](common-contract.md)\n\n'+'\n'.join(f'- [API-{a[0]} — {a[1]}](api-{a[0].lower()}.md)' for a in APIS))
print(f'Generated {len(APIS)} API contracts.')
