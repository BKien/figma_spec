# Tripma Full Database Schema — UC-01 to UC-16

```dbml
Enum seat_class {
  ECONOMY
  BUSINESS
}

Enum passenger_type {
  ADULT
  MINOR
}

Enum booking_status {
  CONFIRMED
  CANCELLED
}

Enum payment_method {
  CREDIT_CARD
  GOOGLE_PAY
  APPLE_PAY
  PAYPAL
  CRYPTO
}

Enum payment_status {
  PENDING
  AUTHORIZED
  DECLINED
  COMPLETED
  FAILED
}

Enum refund_status {
  COMPLETED
  NOT_REQUIRED
}

Enum itinerary_delivery_status {
  SENT
  FAILED
}

Table cities {
  id char(36) [pk, not null]
  name varchar(120) [not null]
  country_code char(2) [not null]
  time_zone varchar(64) [not null]
  active boolean [not null, default: true]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (name, country_code) [unique, name: 'uq_cities_name_country_code']
    active [name: 'idx_cities_active']
  }
}

Table users {
  id char(36) [pk, not null]
  email varchar(320) [not null, unique]
  password_hash varchar(255) [not null]
  username varchar(80) [not null, unique]
  display_name varchar(120)
  profile_image_path varchar(500)
  receive_deal_alerts boolean [not null, default: false]
  terms_accepted_at datetime(3) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]
}

Table customer_reviews {
  id char(36) [pk, not null]
  user_id char(36) [not null]
  rating tinyint [not null]
  content varchar(2000) [not null]
  reviewed_at datetime(3) [not null]
  published boolean [not null, default: false]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (published, reviewed_at) [name: 'idx_customer_reviews_published_reviewed_at']
    (user_id, reviewed_at) [name: 'idx_customer_reviews_user_reviewed_at']
  }
}

Table flights {
  id char(36) [pk, not null]
  origin_city_id char(36) [not null]
  destination_city_id char(36) [not null]
  airline_name varchar(120) [not null]
  image_path varchar(500)
  departure_at datetime(3) [not null]
  arrival_at datetime(3) [not null]
  stops_number smallint [not null, default: 0]
  stops_info varchar(500)
  subtotal_price decimal(12,2) [not null]
  taxes_and_fees decimal(12,2) [not null]
  baggage_fee_per_bag decimal(12,2) [not null, default: 0]
  currency char(3) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (origin_city_id, destination_city_id, departure_at) [name: 'idx_flights_route_departure']
    airline_name [name: 'idx_flights_airline_name']
  }

}

Table route_price_history {
  id char(36) [pk, not null]
  origin_city_id char(36) [not null]
  destination_city_id char(36) [not null]
  recorded_at datetime(3) [not null]
  price decimal(12,2) [not null]
  currency char(3) [not null]
  created_at datetime(3) [not null]

  indexes {
    (origin_city_id, destination_city_id, recorded_at) [name: 'idx_route_price_history_route_recorded_at']
  }

}

Table seats {
  id char(36) [pk, not null]
  flight_id char(36) [not null]
  seat_number varchar(8) [not null]
  seat_class seat_class [not null]
  available boolean [not null, default: true]
  price decimal(12,2) [not null]
  currency char(3) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (flight_id, seat_number) [unique, name: 'uq_seats_flight_id_seat_number']
    (flight_id, available, seat_class) [name: 'idx_seats_flight_available_class']
  }

}

Table bookings {
  id char(36) [pk, not null]
  user_id char(36)
  departing_flight_id char(36) [not null]
  returning_flight_id char(36)
  status booking_status [not null]
  confirmation_code char(12) [not null, unique]
  idempotency_key varchar(128) [not null, unique]
  flight_subtotal decimal(12,2) [not null]
  taxes_and_fees decimal(12,2) [not null]
  baggage_fees decimal(12,2) [not null]
  upgrade_fees decimal(12,2) [not null]
  total decimal(12,2) [not null]
  currency char(3) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (user_id, created_at) [name: 'idx_bookings_user_created_at']
  }

}

Table booking_cancellation_terms {
  id char(36) [pk, not null]
  booking_id char(36) [not null, unique]
  policy_code varchar(64) [not null]
  cancellation_deadline_at datetime(3) [not null]
  refund_rate decimal(5,4) [not null]
  cancellation_fee decimal(12,2) [not null]
  currency char(3) [not null]
  created_at datetime(3) [not null]
}

Table passenger_infos {
  id char(36) [pk, not null]
  booking_id char(36) [not null]
  passenger_ref varchar(64) [not null]
  passenger_type passenger_type [not null]
  first_name varchar(100) [not null]
  middle_name varchar(100)
  last_name varchar(100) [not null]
  suffix varchar(30)
  date_of_birth date [not null]
  email varchar(320)
  phone varchar(32)
  redress_number varchar(50)
  known_traveler_number varchar(50)
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (booking_id, passenger_ref) [unique, name: 'uq_passenger_infos_booking_id_passenger_ref']
    booking_id [name: 'idx_passenger_infos_booking_id']
  }
}

Table emergency_contacts {
  id char(36) [pk, not null]
  booking_id char(36) [not null, unique]
  first_name varchar(100) [not null]
  last_name varchar(100) [not null]
  email varchar(320) [not null]
  phone varchar(32) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]
}

Table passenger_baggage {
  id char(36) [pk, not null]
  passenger_info_id char(36) [not null]
  flight_id char(36) [not null]
  checked_bags smallint [not null, default: 0]
  fee decimal(12,2) [not null, default: 0]
  currency char(3) [not null]
  created_at datetime(3) [not null]

  indexes {
    (passenger_info_id, flight_id) [unique, name: 'uq_passenger_baggage_passenger_flight']
  }

}

Table seat_assignments {
  id char(36) [pk, not null]
  passenger_info_id char(36) [not null]
  flight_id char(36) [not null]
  seat_id char(36) [not null]
  upgrade_amount decimal(12,2) [not null, default: 0]
  currency char(3) [not null]
  created_at datetime(3) [not null]

  indexes {
    (passenger_info_id, flight_id) [unique, name: 'uq_seat_assignments_passenger_flight']
    (flight_id, seat_id) [unique, name: 'uq_seat_assignments_flight_seat']
  }

}

Table payment_infos {
  id char(36) [pk, not null]
  booking_id char(36) [not null, unique]
  payment_method payment_method [not null]
  status payment_status [not null]
  provider_transaction_id varchar(191) [not null, unique]
  payment_token_encrypted varbinary(1024)
  name_on_card varchar(150)
  card_last_four char(4)
  expire_date date
  amount decimal(12,2) [not null]
  currency char(3) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

}

Table booking_cancellations {
  id char(36) [pk, not null]
  booking_id char(36) [not null, unique]
  cancellation_term_id char(36) [not null, unique]
  refund_status refund_status [not null]
  cancellation_fee decimal(12,2) [not null]
  refund_amount decimal(12,2) [not null]
  currency char(3) [not null]
  provider_refund_id varchar(191) [unique]
  idempotency_key varchar(128) [not null, unique]
  cancelled_at datetime(3) [not null]
}

Table saved_payment_methods {
  id char(36) [pk, not null]
  user_id char(36) [not null]
  source_payment_info_id char(36) [not null, unique]
  payment_method payment_method [not null]
  provider_instrument_ref_encrypted varbinary(1024) [not null]
  name_on_card varchar(150) [not null]
  card_last_four char(4) [not null]
  expire_date date [not null]
  is_default boolean [not null, default: false]
  idempotency_key varchar(128) [not null]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (user_id, idempotency_key) [unique, name: 'uq_saved_payment_methods_user_idempotency']
    (user_id, created_at) [name: 'idx_saved_payment_methods_user_created_at']
  }
}

Table share_itineraries {
  id char(36) [pk, not null]
  booking_id char(36) [not null]
  recipient_email varchar(320) [not null]
  delivery_status itinerary_delivery_status [not null]
  provider_message_id varchar(191) [unique]
  sent_at datetime(3)
  failed_at datetime(3)
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (booking_id, created_at) [name: 'idx_share_itineraries_booking_created_at']
  }

}

Table flight_deals {
  id char(36) [pk, not null]
  destination_city_id char(36) [not null]
  place_name varchar(160) [not null]
  image_path varchar(500) [not null]
  price decimal(12,2) [not null]
  currency char(3) [not null]
  description varchar(1000) [not null]
  active boolean [not null, default: true]
  display_order int [not null, default: 0]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (active, display_order) [name: 'idx_flight_deals_active_display_order']
  }
}

Table unique_places {
  id char(36) [pk, not null]
  destination_city_id char(36) [not null]
  place_name varchar(160) [not null]
  image_path varchar(500) [not null]
  price decimal(12,2) [not null]
  currency char(3) [not null]
  description varchar(1000) [not null]
  motivation varchar(1000) [not null]
  active boolean [not null, default: true]
  display_order int [not null, default: 0]
  created_at datetime(3) [not null]
  updated_at datetime(3) [not null]

  indexes {
    (active, display_order) [name: 'idx_unique_places_active_display_order']
  }
}

Ref fk_flights_origin_city: flights.origin_city_id > cities.id
Ref fk_flights_destination_city: flights.destination_city_id > cities.id
Ref fk_route_price_history_origin_city: route_price_history.origin_city_id > cities.id
Ref fk_route_price_history_destination_city: route_price_history.destination_city_id > cities.id
Ref fk_seats_flight: seats.flight_id > flights.id
Ref fk_bookings_user: bookings.user_id > users.id
Ref fk_customer_reviews_user: customer_reviews.user_id > users.id
Ref fk_bookings_departing_flight: bookings.departing_flight_id > flights.id
Ref fk_bookings_returning_flight: bookings.returning_flight_id > flights.id
Ref fk_booking_cancellation_terms_booking: booking_cancellation_terms.booking_id > bookings.id
Ref fk_passenger_infos_booking: passenger_infos.booking_id > bookings.id
Ref fk_emergency_contacts_booking: emergency_contacts.booking_id > bookings.id
Ref fk_passenger_baggage_passenger: passenger_baggage.passenger_info_id > passenger_infos.id
Ref fk_passenger_baggage_flight: passenger_baggage.flight_id > flights.id
Ref fk_seat_assignments_passenger: seat_assignments.passenger_info_id > passenger_infos.id
Ref fk_seat_assignments_flight: seat_assignments.flight_id > flights.id
Ref fk_seat_assignments_seat: seat_assignments.seat_id > seats.id
Ref fk_payment_infos_booking: payment_infos.booking_id > bookings.id
Ref fk_booking_cancellations_booking: booking_cancellations.booking_id > bookings.id
Ref fk_booking_cancellations_term: booking_cancellations.cancellation_term_id > booking_cancellation_terms.id
Ref fk_saved_payment_methods_user: saved_payment_methods.user_id > users.id
Ref fk_saved_payment_methods_source_payment: saved_payment_methods.source_payment_info_id > payment_infos.id
Ref fk_share_itineraries_booking: share_itineraries.booking_id > bookings.id
Ref fk_flight_deals_destination_city: flight_deals.destination_city_id > cities.id
Ref fk_unique_places_destination_city: unique_places.destination_city_id > cities.id
```
