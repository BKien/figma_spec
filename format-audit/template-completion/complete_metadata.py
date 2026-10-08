"""Complete only Not specified metadata; preserve all existing text and code blocks."""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from format_from_template import field_parts, sections
from format_tripma import fences, encode_formatted

AUDIT = ROOT / 'format-audit/template-completion'
MISSING = re.compile(r'(?P<label>Type|Format|Required|Nullable|Trigger|Description|Example|Note|Notes|Default|Allowed values?|Validation):[ \t]*(?P<value>Not specified\.)', re.I)
UUIDS = {name: str(uuid.uuid5(uuid.NAMESPACE_URL, 'example.invalid/' + name)) for name in ['id', 'flightId', 'returningFlightId', 'bookingId', 'passengerId', 'userId', 'cancellationId', 'shareId', 'reviewId', 'participantId', 'sessionId']}
DESC = {
    'email': 'Email address.', 'password': 'Submitted account password.',
    'callbackUrl': 'Client callback URI.', 'csrfToken': 'Opaque CSRF token submitted by the client.',
    'user': 'Public user representation.', 'id': 'Identifier of the represented resource.',
    'username': 'Account display username.', 'session': 'Session representation.',
    'issues': 'Optional array of protocol-level field issues.', 'field': 'Request field path associated with this issue.',
    'code': 'Public machine-readable outcome or issue code.',
    'retryable': 'Indicates whether the public response suggests retrying the request.',
    'agreeTerms': 'Submitted terms acceptance flag.', 'receiveDealAlerts': 'Deal-alert subscription flag.',
    'confirmationCode': 'Booking confirmation access code.',
    'bookingStatus': 'Public booking state.', 'refundStatus': 'Public refund state.',
    'cancellationFee': 'Reported cancellation fee in the response currency.',
    'refundAmount': 'Reported refund amount in the response currency.',
    'currency': 'ISO 4217 currency code for monetary values.',
    'departingFlight': 'Outbound flight representation.', 'returningFlight': 'Return flight representation.',
    'fromCity': 'Departure city label.', 'toCity': 'Arrival city label.',
    'airlineName': 'Airline display name.', 'duration': 'Flight duration display text.',
    'stopsNumber': 'Reported number of flight stops.', 'fromToTime': 'Departure and arrival time display text.',
    'subtotalPrice': 'Reported flight subtotal in the response currency.',
    'taxesAndFees': 'Reported taxes and fees in the response currency.',
    'passengers': 'Passenger representations.', 'firstName': 'Given name.', 'lastName': 'Family name.',
    'seatAssignments': 'Passenger seat assignment representations.', 'seatNumber': 'Seat label.',
    'seatClass': 'Public cabin-class value.', 'baggage': 'Passenger baggage representations.',
    'checkedBags': 'Reported checked bag count.', 'payment': 'Payment representation.',
    'paymentMethod': 'Public payment method value.', 'nameOnCard': 'Cardholder display name.',
    'cardLastFour': 'Last four digits displayed for the payment card.',
    'expireDate': 'Payment-card expiry date in the declared wire format.',
    'priceBreakdown': 'Itemized monetary response amounts.', 'flightSubtotal': 'Reported flight subtotal.',
    'baggageFees': 'Reported baggage fees.', 'upgradeFees': 'Reported cabin or seat upgrade fees.',
    'total': 'Reported total amount.', 'seatSelectionContextKey': 'Opaque reference to the submitted seat-selection context.',
    'cardNumber': 'Card number submitted through this declared payment field.',
    'securityCode': 'Card security code submitted through this declared payment field.',
    'providerToken': 'Opaque payment-provider token.', 'billingAddress': 'Submitted billing address.',
    'sameAsPrimaryPassenger': 'Client flag selecting the primary passenger address.',
    'addressLine1': 'First street address line.', 'addressLine2': 'Additional street address line.',
    'city': 'City display label.', 'region': 'Region or state label.', 'postalCode': 'Postal code.',
    'country': 'Country label.', 'paymentStatus': 'Public payment state.',
    'paymentAccountDisplay': 'Payment account display summary.',
    'passengerRef': 'Client passenger reference.', 'recipientEmails': 'Recipient email address array.',
    'deliveries': 'Itinerary delivery outcome representations.', 'recipientEmail': 'Recipient email address.',
    'deliveryStatus': 'Public itinerary delivery state.', 'necessary': 'Necessary-cookie consent flag.',
    'analytics': 'Analytics-cookie consent flag.', 'personalization': 'Personalization-cookie consent flag.',
    'marketing': 'Marketing-cookie consent flag.', 'policyVersion': 'Consent policy version string.',
    'cursor': 'Opaque pagination cursor.', 'limit': 'Requested page size.',
    'items': 'Resource representations returned in this page.',
    'reviewerDisplayName': 'Reviewer display name.', 'reviewerImagePath': 'Reviewer image URI or path.',
    'rating': 'Reported numeric rating.', 'content': 'Review text.',
    'nextCursor': 'Opaque cursor for a subsequent page, or null when the response declares no cursor.',
    'placeName': 'Destination or place display name.', 'imagePath': 'Image URI or path.',
    'price': 'Reported price in the response currency.', 'description': 'Display description text.',
    'startDate': 'Submitted outbound travel date.', 'endDate': 'Submitted return travel date.',
    'type': 'Trip-type flag: true denotes round-trip and false denotes one-way.',
    'adults': 'Submitted adult passenger count.', 'minors': 'Submitted minor passenger count.',
    'departingFlights': 'Outbound flight results.', 'arrivingFlights': 'Return flight results.',
    'availableSeats': 'Reported available seat count.', 'availableSeatClasses': 'Reported public cabin-class values.',
    'stopsInfo': 'Flight stop display summary.', 'priceGrid': 'Price points for travel-date combinations.',
    'departingDate': 'Outbound date for this price point.', 'returningDate': 'Return date for this price point.',
    'minPrice': 'Reported lowest amount for this price point.', 'priceHistory': 'Historical price point representations.',
    'recordedDate': 'Date represented by this historical price point.', 'averagePrice': 'Reported average price.',
    'priceRating': 'Public price trend summary.', 'projectedPrice': 'Reported projected price.',
    'projectedChangePercent': 'Reported projected percentage change.', 'recommendation': 'Public recommendation value.',
    'upcomingTrips': 'Upcoming trip representations.', 'completedTrips': 'Completed trip representations.',
    'cancelledTrips': 'Cancelled trip representations.', 'timingStatus': 'Public trip timing classification.',
    'passengerCount': 'Reported passenger count.', 'selectionContextKey': 'Opaque flight-selection context reference.',
    'primaryPassengerRef': 'Client reference identifying the primary passenger.',
    'passengerType': 'Public passenger category.', 'middleName': 'Middle name.', 'suffix': 'Name suffix.',
    'dateOfBirth': 'Passenger birth date.', 'phone': 'Telephone contact string.',
    'redressNumber': 'Submitted passenger redress reference.', 'knownTravelerNumber': 'Submitted known-traveler reference.',
    'departingCheckedBags': 'Submitted outbound checked bag count.', 'returningCheckedBags': 'Submitted return checked bag count.',
    'emergencyContact': 'Emergency contact representation.', 'usePrimaryPassenger': 'Client flag selecting the primary passenger contact.',
    'passengerContextKey': 'Opaque passenger-information context reference.',
    'makeDefault': 'Client flag requesting the default payment-method setting.',
    'displayName': 'Public display label.', 'isDefault': 'Reported default payment-method flag.',
    'businessSeats': 'Business cabin seat representations.', 'economySeats': 'Economy cabin seat representations.',
    'available': 'Reported availability flag.', 'motivation': 'Destination promotional display text.',
}
STRINGS = {
    'email': 'alex@example.com', 'recipientEmail': 'friend@example.com', 'recipientEmails': 'friend@example.com',
    'password': 'ExamplePassword42!', 'callbackUrl': 'https://example.com/account',
    'csrfToken': 'csrf-example-01', 'username': 'alexmorgan', 'confirmationCode': 'TRP7K2',
    'fromCity': 'San Francisco', 'toCity': 'Tokyo', 'airlineName': 'Example Air',
    'duration': '11h 30m', 'fromToTime': '09:00 - 20:30', 'seatNumber': '12A',
    'nameOnCard': 'Alex Morgan', 'cardLastFour': '4242', 'cardNumber': '4242424242424242',
    'securityCode': '123', 'providerToken': 'provider-token-example-01',
    'addressLine1': '123 Example Street', 'addressLine2': 'Apartment 4', 'city': 'San Francisco',
    'region': 'California', 'postalCode': '94103', 'country': 'United States',
    'paymentAccountDisplay': 'Visa ending in 4242', 'passengerRef': 'passenger_01', 'primaryPassengerRef': 'passenger_01',
    'policyVersion': '2026-10', 'cursor': 'opaque-page-cursor-01', 'nextCursor': 'opaque-page-cursor-02',
    'nextReactionCursor': 'opaque-reaction-cursor-02', 'reactionCursor': 'opaque-reaction-cursor-01',
    'reviewerDisplayName': 'Alex Morgan', 'reviewerImagePath': 'https://example.com/images/reviewer.jpg',
    'content': 'A comfortable trip with helpful staff.', 'placeName': 'Kyoto',
    'imagePath': 'https://example.com/images/travel.jpg', 'description': 'A comfortable stay near the city center.',
    'stopsInfo': 'Nonstop', 'selectionContextKey': 'flight-selection-example-01',
    'seatSelectionContextKey': 'seat-selection-example-01', 'passengerContextKey': 'passenger-context-example-01',
    'firstName': 'Alex', 'middleName': 'Taylor', 'lastName': 'Morgan', 'suffix': 'Jr.',
    'phone': '+14155550123', 'redressNumber': '1234567', 'knownTravelerNumber': '123456789',
    'displayName': 'Alex Morgan', 'motivation': 'Explore local culture and memorable landmarks.',
    'currency': 'USD', 'paymentMethod':'CREDIT_CARD', 'searchContextId': 'search-context-example-01', 'offerId': 'offer_01JABCDEF',
    'quoteId': 'quote_01JABCDEF', 'title': 'A weekend in Kyoto', 'name': 'Example Riverside Hotel',
    'microphoneDeviceId': 'microphone-device-01', 'cameraDeviceId': 'camera-device-01',
    'speakerDeviceId': 'speaker-device-01', 'virtualBackgroundId': 'background-01',
    'imageUrl': 'https://example.com/images/travel.jpg', 'imageUrls': 'https://example.com/images/travel.jpg',
    'destinationName': 'Kyoto', 'stayName': 'Example Riverside Hotel', 'countryCode': 'JP',
    'address': '123 Example Street, Kyoto', 'authorName': 'Alex Morgan', 'comment': 'A comfortable stay.',
    'fullName': 'Alex Morgan', 'vehicleName': 'Example Sedan', 'vehicleCategory': 'SEDAN',
    'category': 'MEDIUM', 'transmission': 'AUTOMATIC', 'electricType': 'HYBRID',
    'registrationNumber': 'EXAMPLE-123', 'paymentMode': 'PAY_DRIVER', 'originCode': 'SGN',
    'destinationCode': 'HND', 'carrierCode': 'EX', 'providerId': 'provider_a',
}
NUMBERS = {
    'adults': 1, 'minors': 0, 'stopsNumber': 0, 'availableSeats': 24, 'checkedBags': 1,
    'departingCheckedBags': 1, 'returningCheckedBags': 1, 'passengerCount': 1, 'rating': 5,
    'limit': 20, 'offset': 0, 'total': 300, 'reviewCount': 25, 'snapshotVersion': 1,
    'cancellationFee': 25, 'refundAmount': 275, 'subtotalPrice': 250, 'flightSubtotal': 250,
    'taxesAndFees': 25, 'baggageFees': 15, 'upgradeFees': 10, 'price': 300, 'minPrice': 280,
    'averagePrice': 320, 'projectedPrice': 300, 'projectedChangePercent': -6.25,
    'daysRemaining': 3, 'durationMinutes': 660, 'availableRooms': 4, 'passengers': 1,
    'distanceFromCenterKm': 2.5, 'mileageAllowanceKm': 150, 'seatCapacity': 4,
    'seats': 4, 'largeBagCapacity': 2, 'smallBagCapacity': 2,
    'latitude': 35.0116, 'longitude': 135.7681,
}
ERROR_MESSAGES = {'400': 'The request does not match the declared wire schema.', '401': 'Authentication was not accepted.', '403': 'Access to this operation was not accepted.', '404': 'The requested resource was not found.', '409': 'The request conflicts with the current operation.', '422': 'The request could not be processed.', '429': 'Too many requests.', '500': 'An unexpected server error occurred.', '502': 'An upstream service returned an unusable response.', '503': 'The service is temporarily unavailable.'}
PRIORITIES = {
    'Clicon Ecommerce Marketplace': {**dict.fromkeys([1,2,3,4,5,6,7,8,12,15,16], 'High'), **dict.fromkeys([9,10,11,13,17,18,19], 'Medium'), 14:'Low',20:'Low'},
    'DH Dental Recruitment': {**dict.fromkeys([1,2,3,4,5,6,8,12,13,14,20], 'High'), **dict.fromkeys([7,9,11,15,16,17,18,19], 'Medium'),10:'Low'},
    'EdTech Education Dashboard': {**dict.fromkeys([1,2,3,4,5,6,7,8,9,13,14,15,16,17,18,19,20], 'High'),10:'Medium',11:'Medium',12:'Medium'},
}

def leaf(name):
    return name.split(' / ')[0].split('.')[-1].replace('[]','')

def text_value(raw):
    raw = raw.strip().strip('`').rstrip('.').strip('`')
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw.strip('"')

def enum_first(meta):
    raw = meta.get('Allowed values', meta.get('Allowed value','')).split('\n')[0]
    if not raw or 'Not specified' in raw:
        return None
    values = re.findall(r'`([^`]+)`', raw) or [x.strip().strip('"') for x in re.split(r'[,;]', raw)]
    return values[0] if values else None

def format_header(name):
    return {'Authorization':'Bearer token', 'Accept':'HTTP media type', 'Content-Type':'HTTP media type', 'Idempotency-Key':'Opaque HTTP header value', 'Cookie':'HTTP Cookie', 'X-CSRF-Token':'Opaque HTTP header value', 'X-Confirmation-Code':'Opaque HTTP header value'}[leaf(name)]

def description(name, section, meta, api_name):
    part = leaf(name)
    if name.startswith('headers.'):
        return {'Content-Type':'Media type of the request body.', 'Accept':'Requested response media type.', 'Idempotency-Key':'Opaque command reference carried by the HTTP header.', 'X-Confirmation-Code':'Booking confirmation access code carried by the HTTP header.', 'Set-Cookie':'Cookie setting returned by the endpoint.'}[part]
    if part == 'success': return 'Indicates whether the HTTP operation completed successfully.'
    if part == 'message': return 'Public error outcome summary.' if section.startswith('Error') else 'Human-readable operation outcome summary.'
    if part == 'data': return 'Endpoint-specific response payload.'
    if part == 'status':
        return 'Public consent state.' if 'COOKIE' in api_name else 'Public payment state.' if '.payment.' in name else 'Public booking state.'
    if part.endswith('Id'):
        noun = re.sub(r'(?<!^)([A-Z])', r' \1', part[:-2]).lower()
        return f'{noun.capitalize()} identifier.'
    if part.endswith('At') or part in ['expiresAt', 'journeyEndAt']:
        word = re.sub(r'(?<!^)([A-Z])', r' \1', part).lower()
        return f'{word.capitalize()} timestamp in the declared ISO 8601 format.'
    if part == 'date': return 'Flight departure date-time in the declared ISO 8601 format.'
    if part in DESC: return DESC[part]
    raise ValueError(f'No description decision for {section}/{name}')

def trigger(name, section, meta, method):
    required = meta.get('Required','').splitlines()[0].lower().startswith('yes')
    parent = name.split(' / ')[0].rsplit('.',1)[0] if '.' in name.split(' / ')[0] else None
    status = re.search(r'HTTP (\d{3})', section)
    if section == 'Request Header(s)':
        return f'Every {method} request to this endpoint.' if required else f'When the client supplies the {leaf(name)} header.'
    if section == 'Path Parameter(s)': return f'Every request using the {leaf(name)} path segment.'
    if section == 'Query Parameter(s)': return f'Every request includes the {leaf(name)} query parameter.' if required else f'When the client supplies the {leaf(name)} query parameter.'
    if section == 'Request Body':
        if parent: return f'When the containing {parent} object or array item is supplied in the request body.' if required else f'When the client includes this optional property in the containing {parent} object or array item.'
        return 'Every request body sent to this endpoint.' if required else 'When the client includes this property in the request body.'
    if section == 'Success Response Header(s)': return 'Returned with the successful HTTP response.'
    if status:
        base = f'Included in the HTTP {status[1]} ' + ('error' if section.startswith('Error') else 'success') + ' response'
        if parent and parent not in ['headers']:
            base += f' when the containing {parent} object or array item is present and non-null'
            if not required:base += ' and this optional property is returned'
        elif not required:
            base += ' when this optional field is returned'
        return base + '.'
    raise ValueError(f'Unknown Trigger section {section}')

def note(name, section):
    if section == 'Request Header(s)':
        return {'Authorization':'Uses the HTTP Bearer authentication scheme.', 'Content-Type':'Identifies the media type of the submitted request body.', 'Accept':'Identifies the requested response media type.', 'Cookie':'Carries semicolon-separated HTTP cookie pairs.', 'Idempotency-Key':'Transmit the command reference as a single header value.', 'X-CSRF-Token':'Transmit the opaque token as a single header value.', 'X-Confirmation-Code':'Transmit the confirmation code as a single header value.'}.get(leaf(name), 'Header names are case-insensitive.')
    if section.startswith('Error'):
        return 'Field of the JSON error response; nested requiredness applies when its containing object or array item is present.' if '.' in name else 'Field of the JSON error response.'
    return 'None'

def primitive(name, meta, section, api_id, package):
    part = leaf(name)
    typ = meta.get('Type','string').splitlines()[0].lower()
    fmt = meta.get('Format','').lower()
    if 'Example' in meta and not meta['Example'].lower().startswith('not specified'):
        return text_value(meta['Example'])
    if name.startswith('headers.'):
        return {'Accept':'application/json', 'Content-Type':'application/json', 'Idempotency-Key':'command-example-01', 'X-Confirmation-Code':'TRP7K2', 'Set-Cookie':'tripma_consent=opaque-consent-value; Path=/; SameSite=Lax'}[part]
    returning='returningFlight' in name or 'arrivingFlights' in name or 'inboundSegments' in name
    completed='completedTrips' in name
    cancelled='cancelledTrips' in name
    if part == 'seatClass' and 'businessSeats' in name:return 'BUSINESS'
    if part == 'seatNumber' and 'businessSeats' in name:return '2A'
    if part == 'bookingStatus' and cancelled:return 'CANCELLED'
    if part == 'timingStatus':return 'COMPLETED' if completed else 'CANCELLED' if cancelled else 'UPCOMING'
    if part == 'paymentStatus':return 'COMPLETED'
    if part == 'deliveryStatus' and section.startswith('Error'):
        return 'FAILED'
    enum = enum_first(meta)
    if enum is not None and 'array' not in typ: return enum
    if meta.get('Default') and 'array' not in typ: return text_value(meta['Default'].splitlines()[0])
    if typ == 'boolean':
        return part not in ['retryable','receiveDealAlerts','analytics','personalization','marketing','hasMore','partial','pictureInPicture']
    if typ in ['integer','number'] or 'nullable number' in typ:
        if part == 'total' and typ == 'integer':return 1
        return NUMBERS.get(part,1)
    if 'UUID' in meta.get('Format','') or (package.startswith('100ms') and (part.endswith('ParticipantId') or 'UUID' in meta.get('Description',''))):
        if part in ['flightId','returningFlightId'] and returning:return UUIDS['returningFlightId']
        if part=='id' and 'Seats' in name:return str(uuid.uuid5(uuid.NAMESPACE_URL,'example.invalid/'+name.split('.')[1]))
        if part=='bookingId' and (completed or cancelled):return str(uuid.uuid5(uuid.NAMESPACE_URL,'example.invalid/'+('completed-booking' if completed else 'cancelled-booking')))
        if package.startswith('100ms'):return '11111111-1111-4111-8111-111111111111'
        return UUIDS.get(part, UUIDS['id'])
    if '4217' in fmt: return 'USD'
    if 'email' in fmt or 'email string' in typ:return STRINGS.get(part, 'alex@example.com')
    if 'date' in fmt or 'iso 8601' in fmt or 'iso 8601' in typ:
        if 'COOKIE' in api_id and part=='expiresAt':return '2027-04-05T09:00:00Z'
        if part in ['dateOfBirth']:return '1990-01-15'
        if part == 'expireDate': return '2030-12-01'
        if (fmt.strip() == 'date' or 'date string' in typ or 'iso 8601 date' == fmt.strip()) and 'date-time' not in fmt and 'date-time' not in typ:
            return '2026-10-10' if part not in ['endDate','returningDate'] else '2026-10-17'
        day='2026-09-10' if completed else '2026-10-17' if returning else '2026-10-10'
        if part in ['createdAt','cancelledAt','bookedAt','preparedAt','decidedAt','publishedAt','reviewedAt']:day='2026-09-01' if completed and part=='bookedAt' else '2026-10-07'
        time='T20:30:00Z' if part in ['arrivalAt','expiresAt','validUntil','journeyEndAt','dropoffAt'] else 'T09:00:00Z'
        if package.startswith('Travel') and part=='arrivalAt':time='T14:30:00Z'
        return day+time
    if part == 'message':
        status = re.search(r'HTTP (\d{3})', section)
        return ERROR_MESSAGES.get(status[1] if status else '', 'Request completed successfully.') if section.startswith('Error') else 'Request completed successfully.'
    if part == 'field':return 'email' if 'AUTH' in api_id else 'request'
    if part == 'code':return 'INVALID_FORMAT' if section.startswith('Error') else 'UPSTREAM_UNAVAILABLE'
    if part in ['bookingStatus','status','refundStatus']:
        if part == 'refundStatus':return 'COMPLETED'
        if 'COOKIE' in api_id:return 'REJECTED_OPTIONAL'
        if 'CANCEL' in api_id:return 'CANCELLED'
        return 'CONFIRMED'
    if part in ['fromCity','toCity'] and returning:return 'Tokyo' if part=='fromCity' else 'San Francisco'
    if part in ['originCode','destinationCode'] and returning:return 'HND' if part=='originCode' else 'SGN'
    if part=='city' and ('data[]' in name):return 'Kyoto'
    if package.startswith('Travel'):
        if part in ['authorName','fullName'] and 'TAXI' not in api_id:return 'A***'
        if part=='name' and 'destination' in name:return 'Kyoto'
        if part=='displayName' and 'vehicle' in name:return 'Example Sedan'
        if part in ['category','vehicleCategory']:return 'MEDIUM'
        if part=='currency' and 'TAXI' in api_id:return 'LKR'
    if part in STRINGS:return STRINGS[part]
    if part == 'id':
        if package.startswith('Travel'):
            resource='destination' if 'destination' in name else 'driver' if 'driver' in name else 'vehicle' if 'vehicle' in name else 'offer' if 'offer' in name else 'trip' if 'BUDGET' in api_id else 'stay' if 'STAY' in api_id else 'booking'
            return resource+'_01JABCDEF'
        return UUIDS['id']
    if part.endswith('Id'):return part[:-2].lower() + '_example_01'
    if part in ['attractions','amenities']:return 'Historic district' if part == 'attractions' else 'Wi-Fi'
    if part in ['destinations','reviews']:return 'READY'
    if part == 'authenticated':return True
    raise ValueError(f'No scalar example for {package}/{api_id}/{section}/{name}/{typ}')

def expanded_fields(fields):
    index = {}
    for name,value in fields:
        _, meta = field_parts(value)
        for alias in name.split(' / '):
            names = [alias.replace('*Trips',n) for n in ['upcomingTrips','completedTrips','cancelledTrips']] if '*Trips' in alias else [alias]
            for item in names:index[item] = (value,meta)
    return index

def common_representations(package):
    file = package/'01-inception/api/common-contract.md'
    if not file.exists():return {}
    result = {}
    for name,value in sections(file.read_text(encoding='utf-8-sig'),2):
        fields = []
        for prop,body in sections(value,3):
            normalized = re.sub(r'^- ', '', body, flags=re.M)
            fields.append((prop.strip('`'), normalized))
        if fields:result[name] = expanded_fields(fields)
    return result

def example(name, meta, body, index, section, api_id, package, common, depth=0):
    if depth > 12:raise ValueError('Example nesting exceeds schema depth')
    typ = meta.get('Type','string').splitlines()[0].lower()
    named = re.search(r'object \((\w+)\)',typ,re.I)
    if named:
        common_name = next((k for k in common if k.lower()==named[1].lower()),None)
        if common_name is None:raise ValueError(f'Missing representation {named[1]}')
        obj={}
        for prop,(value,details) in common[common_name].items():
            if details.get('Required','').startswith('Yes'):
                obj[prop]=None if details.get('Nullable','').startswith('Yes') else example(prop,details,value,common[common_name],section,api_id,package,common,depth+1)
        if common_name=='SessionSummary':
            obj['hostParticipantId']='11111111-1111-4111-8111-111111111111'
            if api_id in ['API-LIVE-STREAM-CONTROL','API-SESSION-STATE','API-SESSION-DEPARTURE','API-SPOTLIGHT-UPDATE','API-SESSION-JOIN']:obj['status']='LIVE'
            if api_id=='API-SESSION-DEPARTURE':obj['hostParticipantId']='22222222-2222-4222-8222-222222222222'
            if api_id=='API-SPOTLIGHT-UPDATE':obj['spotlightedParticipantId']='11111111-1111-4111-8111-111111111111'
        if common_name=='Stream' and api_id=='API-LIVE-STREAM-CONTROL':obj['status']='STARTING'
        if common_name=='Recording' and api_id=='API-RECORDING-CONTROL':obj['status']='STARTING'
        if common_name=='Participant' and api_id=='API-SESSION-DEPARTURE':
            obj['role']='VIEWER';obj['status']='LEFT';obj['leftAt']='2026-09-22T09:05:00Z'
        if common_name=='Participant' and api_id=='API-STAGE-REQUEST-CREATE':obj['role']='VIEWER'
        if common_name=='MediaPreference' and api_id=='API-PREFERENCES-UPDATE':
            obj.update(microphoneDeviceId='microphone-device-01',cameraDeviceId='camera-device-01',speakerDeviceId='speaker-device-01',virtualBackgroundId='11111111-1111-4111-8111-111111111111')
        if common_name=='ViewPreference' and api_id=='API-PREFERENCES-UPDATE':
            obj.update(focusedParticipantId='11111111-1111-4111-8111-111111111111',sidePanel='CHAT')
        return obj
    if 'money object' in typ:return {'amount':300.0,'currency':'LKR' if 'TAXI' in api_id else 'USD'}
    if 'array' in typ:
        path = name if name.endswith('[]') else name+'[]'
        item_meta = index.get(path)
        if item_meta and 'array' not in item_meta[1].get('Type',''):
            return [example(path,item_meta[1],item_meta[0],index,section,api_id,package,common,depth+1)]
        children = [k for k in index if k.startswith(path+'.')]
        if children:
            return [example(path,{'Type':'object'},'',index,section,api_id,package,common,depth+1)]
        if 'object' in typ or re.search(r'^- Fields',body,re.M):
            return [example(path,{'Type':'object'},body,index,section,api_id,package,common,depth+1)]
        enums = enum_first(meta)
        if enums is not None:return [enums]
        child_type = typ.replace(' array','') if typ != 'array' else 'string'
        return [primitive(name,{'Type':child_type},section,api_id,package)]
    if 'object' in typ:
        children={}
        for key,(value,details) in index.items():
            if key.startswith(name+'.'):
                remainder=key[len(name)+1:]
                if '.' not in remainder:
                    child=remainder.removesuffix('[]')
                    if child not in children or not remainder.endswith('[]'):
                        children[child]=(key,value,details)
        if children:
            return {prop:example(key,details,value,index,section,api_id,package,common,depth+1) for prop,(key,value,details) in children.items() if details.get('Required','').lower().startswith('yes') or (section=='Request Body' and name=='payment' and prop in ['nameOnCard','cardNumber','securityCode','expireDate'])}
        line = re.search(r'^- Fields(?: when non-null)?: (.+)$',body,re.M)
        if line:
            obj={}
            for prop,t in re.findall(r'`([^`]+)` \(([^)]+)\)',line[1]):
                if prop in ['outboundSegments','inboundSegments']:
                    segments=re.search(r'^- Segment fields \(both arrays\): (.+)$',body,re.M)
                    obj[prop]=[{child:primitive(name+'.'+prop+'[].'+child,{'Type':child_type},section,api_id,package) for child,child_type in re.findall(r'`([^`]+)` \(([^)]+)\)',segments[1])}]
                elif t == 'object' and prop == 'location':
                    obj[prop]={'name':'Kyoto','countryCode':'JP'}
                else:
                    obj[prop]=example(name+'.'+prop,{'Type':t},'',{},section,api_id,package,common,depth+1)
            return obj
        if leaf(name)=='location':return {'name':'Kyoto','countryCode':'JP'}
        raise ValueError(f'No object schema for {package}/{api_id}/{name}')
    return primitive(name,meta,section,api_id,package)

def complete_api(path,package):
    original=path.read_bytes();text=original.decode('utf-8-sig').replace('\r\n','\n')
    method=re.search(r'^### Method\n\s*`?([A-Z]+)',text,re.M)[1]
    api_id=re.search(r'^api_id: (.+)$',text,re.M)[1]
    common=common_representations(package)
    replacements=[]
    counters=Counter()
    api_sections=sections(text,2)
    success_index={}
    for heading,body in api_sections:
        if heading.startswith('Success Response'):
            success_index.update(expanded_fields(sections(body,3)))
    for section,body in api_sections:
        fields=sections(body,3)
        if not fields or section in ['General Information','Notes']:continue
        index={**success_index,**expanded_fields(fields)} if section.startswith('Error') else expanded_fields(fields)
        for name,value in fields:
            _,meta=field_parts(value)
            for missing in MISSING.finditer(value):
                label=missing['label']
                if label == 'Format':new=format_header(name)
                elif label == 'Trigger':new=trigger(name,section,meta,method)
                elif label == 'Note':new=note(name,section)
                elif label == 'Description':new=description(name,section,meta,api_id)
                elif label == 'Example':
                    alias=name.split(' / ')[0].replace('*Trips','upcomingTrips')
                    data=example(alias,meta,value,index,section,api_id,package.name,common)
                    new=json.dumps(data,ensure_ascii=False,separators=(', ', ': '))
                else:raise ValueError(f'Unexpected missing field {label} in {path}')
                replacements.append({'section':section,'field':name,'label':label,'value':new})
                counters[label]+=1
    lines=text.splitlines(keepends=True)
    section=None;field=None;queue={(r['section'],r['field'],r['label']):r['value'] for r in replacements}
    for i,line in enumerate(lines):
        if line.startswith('## '):section=line[3:].strip();field=None
        elif line.startswith('### '):field=line[4:].strip()
        if section is not None and field is not None:
            def replace(m):
                new=queue[(section,field,m['label'])]
                return m['label']+': '+new
            lines[i]=MISSING.sub(replace,line)
    completed=''.join(lines)
    if re.search(r'Not specified',completed,re.I):raise ValueError(f'Unfilled placeholder in {path}')
    if fences(text)!=fences(completed):raise ValueError(f'Code block changed in {path}')
    return encode_formatted(original,completed),counters,replacements

def main():
    packages=sorted(p for p in ROOT.iterdir() if p.is_dir() and (p/'01-inception').is_dir())
    totals=Counter();per_package=defaultdict(Counter);planned=[];decisions=[]
    for package in packages:
        for path in sorted((package/'01-inception').rglob('*.md')):
            if not re.match(r'(?i)^(api-.+|uc-\d{2}-.+)\.md$',path.name):continue
            text=path.read_text(encoding='utf-8-sig')
            if not re.search('Not specified',text,re.I):continue
            if path.name.lower().startswith('uc-'):
                number=int(re.search(r'uc-(\d{2})-',path.name,re.I)[1]);priority=PRIORITIES[package.name][number]
                raw=path.read_bytes();before=raw.decode('utf-8-sig').replace('\r\n','\n')
                after,n=re.subn(r'(?<=### Priority\n\n)Not specified in the supplied source\.',priority,before)
                if n!=1:raise ValueError(f'Unexpected UC placeholder {path}')
                encoded=encode_formatted(raw,after);counts=Counter({'Priority':1})
                edits=[{'section':'Functional Use-Case Specification','field':'Priority','label':'Priority','value':priority}]
            else:encoded,counts,edits=complete_api(path,package)
            planned.append((path,encoded));totals.update(counts);per_package[package.name].update(counts)
            decisions.append({'file':path.relative_to(ROOT).as_posix(),'replacements':edits})
    report={'status':'planned','counts':dict(totals),'total_replacements':sum(totals.values()),'changed_documents':len(planned),'packages':{k:dict(v) for k,v in per_package.items()},
            'basis':['Explicit user authorization to decide unspecified metadata from repository and supplied template.','Existing known metadata is preserved.','Triggers describe wire field presence and declared HTTP outcome only.','Nested JSON examples follow declared field schemas; named objects resolve through package-local common-contract.md.','Priorities: High for core actor goals and account access/security, Medium for supporting features, Low for supplementary features.'],
            'decisions':decisions}
    AUDIT.mkdir(parents=True,exist_ok=True)
    (AUDIT/'metadata-decisions.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if '--apply' in sys.argv:
        for path,data in planned:path.write_bytes(data)
        report['status']='applied'
        (AUDIT/'metadata-decisions.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','counts','changed_documents','packages']},indent=2))

if __name__ == '__main__':main()
