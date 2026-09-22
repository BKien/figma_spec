-- Apply after compiling schema.dbml to PostgreSQL SQL.
-- Conditional uniqueness and foreign keys are already generated from DBML.
-- This supplement enforces aggregate capacities under a locked session row.

CREATE FUNCTION enforce_participant_capacity() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  room sessions%ROWTYPE;
  member_count integer;
  stage_count integer;
BEGIN
  SELECT * INTO room FROM sessions WHERE id = NEW.session_id FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'Session unavailable' USING ERRCODE = '23503'; END IF;
  IF TG_OP = 'UPDATE' AND (NEW.session_id <> OLD.session_id OR NEW.principal_id <> OLD.principal_id) THEN
    RAISE EXCEPTION 'Membership identity is immutable' USING ERRCODE = '23514';
  END IF;
  IF NEW.status = 'JOINED' THEN
    IF room.status = 'ENDED' THEN RAISE EXCEPTION 'Session ended' USING ERRCODE = '23514'; END IF;
    IF (NEW.role = 'HOST') <> (NEW.principal_id = room.designated_host_principal_id) THEN
      RAISE EXCEPTION 'Host identity mismatch' USING ERRCODE = '23514';
    END IF;
    SELECT count(*) INTO member_count FROM participants WHERE session_id = NEW.session_id AND status = 'JOINED' AND id <> NEW.id;
    IF member_count >= (CASE WHEN room.kind = 'VIDEO_CONFERENCE' THEN 100 ELSE 1000 END) THEN
      RAISE EXCEPTION 'Session capacity exceeded' USING ERRCODE = '23514';
    END IF;
    IF room.kind = 'LIVE_STREAM' AND NEW.role <> 'VIEWER' THEN
      SELECT count(*) INTO stage_count FROM participants WHERE session_id = NEW.session_id AND status = 'JOINED' AND role <> 'VIEWER' AND id <> NEW.id;
      IF stage_count >= 10 THEN RAISE EXCEPTION 'Stage capacity exceeded' USING ERRCODE = '23514'; END IF;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER participant_capacity_guard BEFORE INSERT OR UPDATE ON participants
FOR EACH ROW EXECUTE FUNCTION enforce_participant_capacity();

ALTER TABLE participants ADD CONSTRAINT participant_display_name CHECK (display_name = btrim(display_name) AND char_length(display_name) BETWEEN 1 AND 50);
ALTER TABLE chat_messages ADD CONSTRAINT message_body_shape CHECK (body = btrim(body) AND char_length(body) BETWEEN 1 AND 1000);
ALTER TABLE chat_messages ADD CONSTRAINT message_sequence_positive CHECK (sequence > 0);
ALTER TABLE reaction_events ADD CONSTRAINT reaction_sequence_positive CHECK (sequence > 0);
ALTER TABLE content_shares ADD CONSTRAINT share_source_present CHECK (char_length(btrim(source_reference)) > 0);
ALTER TABLE idempotency_records ADD CONSTRAINT idempotency_key_present CHECK (char_length(btrim(idempotency_key)) > 0);
ALTER TABLE idempotency_records ADD CONSTRAINT idempotency_expiry CHECK (expires_at = completed_at + interval '24 hours');

-- All application mutations and trusted provider completions use SERIALIZABLE transactions.
-- They lock sessions.id before membership/resource reads and write the receipt in the same transaction.
-- Serialization failures are retried at the gateway; no partial HTTP success is returned.
