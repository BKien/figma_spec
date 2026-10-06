-- Apply after compiling schema.dbml to MySQL 8.0 SQL.
-- MySQL has no native range exclusion constraint. The following SERIALIZABLE
-- InnoDB trigger contract locks conflicting allocation ranges.

DELIMITER $$

CREATE PROCEDURE assert_taxi_allocation_available(
  IN p_booking_id CHAR(36),
  IN p_driver_id CHAR(36),
  IN p_vehicle_id CHAR(36),
  IN p_pickup_at DATETIME,
  IN p_dropoff_at DATETIME
)
BEGIN
  DECLARE v_conflict_id CHAR(36) DEFAULT NULL;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_conflict_id = NULL;

  IF p_dropoff_at <= p_pickup_at THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Taxi allocation interval must be positive';
  END IF;

  SELECT booking_id INTO v_conflict_id
  FROM taxi_allocations
  WHERE booking_id <> p_booking_id
    AND (driver_id = p_driver_id OR vehicle_id = p_vehicle_id)
    AND p_pickup_at < dropoff_at
    AND pickup_at < p_dropoff_at
  LIMIT 1
  FOR UPDATE;

  IF v_conflict_id IS NOT NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Taxi resource allocation overlaps an existing booking';
  END IF;
END$$

CREATE TRIGGER taxi_allocation_guard_insert
BEFORE INSERT ON taxi_allocations
FOR EACH ROW
BEGIN
  CALL assert_taxi_allocation_available(
    NEW.booking_id, NEW.driver_id, NEW.vehicle_id, NEW.pickup_at, NEW.dropoff_at
  );
END$$

CREATE TRIGGER taxi_allocation_guard_update
BEFORE UPDATE ON taxi_allocations
FOR EACH ROW
BEGIN
  CALL assert_taxi_allocation_available(
    NEW.booking_id, NEW.driver_id, NEW.vehicle_id, NEW.pickup_at, NEW.dropoff_at
  );
END$$

DELIMITER ;

ALTER TABLE search_snapshot_items
  ADD CONSTRAINT snapshot_one_offer CHECK (
    (stay_offer_id IS NOT NULL)
    + (taxi_offer_id IS NOT NULL)
    + (flight_offer_id IS NOT NULL) = 1
  );
ALTER TABLE search_snapshots
  ADD CONSTRAINT snapshot_positive_window CHECK (valid_until > captured_at);
ALTER TABLE reviews
  ADD CONSTRAINT review_one_booking CHECK (
    (stay_booking_id IS NOT NULL) + (taxi_booking_id IS NOT NULL) <= 1
  ),
  ADD CONSTRAINT review_rating_range CHECK (rating BETWEEN 1 AND 5),
  ADD CONSTRAINT published_review_has_time CHECK (
    published = FALSE OR published_at IS NOT NULL
  );
ALTER TABLE budget_trips
  ADD CONSTRAINT trip_publication_window CHECK (
    publish_until IS NULL OR publish_until > publish_from
  );

-- Allocation mutations must run in SERIALIZABLE InnoDB transactions so the
-- indexed range reads above prevent concurrent phantom overlaps.
