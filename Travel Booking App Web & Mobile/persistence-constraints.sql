-- Apply after compiling schema.dbml to PostgreSQL SQL.
-- DBML does not express PostgreSQL range exclusion constraints.
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE taxi_allocations
  ADD CONSTRAINT taxi_allocation_positive_interval CHECK (dropoff_at > pickup_at),
  ADD CONSTRAINT taxi_driver_no_overlap EXCLUDE USING gist
    (driver_id WITH =, tstzrange(pickup_at, dropoff_at, '[)') WITH &&),
  ADD CONSTRAINT taxi_vehicle_no_overlap EXCLUDE USING gist
    (vehicle_id WITH =, tstzrange(pickup_at, dropoff_at, '[)') WITH &&);

ALTER TABLE search_snapshot_items
  ADD CONSTRAINT snapshot_one_offer CHECK
    (num_nonnulls(stay_offer_id, taxi_offer_id, flight_offer_id) = 1);
ALTER TABLE search_snapshots
  ADD CONSTRAINT snapshot_positive_window CHECK (valid_until > captured_at);
ALTER TABLE reviews
  ADD CONSTRAINT review_one_booking CHECK (num_nonnulls(stay_booking_id, taxi_booking_id) <= 1),
  ADD CONSTRAINT review_rating_range CHECK (rating BETWEEN 1 AND 5),
  ADD CONSTRAINT published_review_has_time CHECK (NOT published OR published_at IS NOT NULL);
ALTER TABLE budget_trips
  ADD CONSTRAINT trip_publication_window CHECK (publish_until IS NULL OR publish_until > publish_from);
