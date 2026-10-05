from yoyo import step


steps = [
    step(
        """
        ALTER TABLE incidents
        ADD COLUMN created_at TIMESTAMPTZ
            NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ADD COLUMN updated_at TIMESTAMPTZ
            NOT NULL DEFAULT CURRENT_TIMESTAMP;
        """,
        """
        ALTER TABLE incidents
        DROP COLUMN updated_at,
        DROP COLUMN created_at;
        """,
    ),

    step(
        """
        CREATE OR REPLACE FUNCTION set_incidents_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER incidents_set_updated_at
        BEFORE UPDATE ON incidents
        FOR EACH ROW
        EXECUTE FUNCTION set_incidents_updated_at();
        """,
        """
        DROP TRIGGER IF EXISTS incidents_set_updated_at
        ON incidents;

        DROP FUNCTION IF EXISTS set_incidents_updated_at();
        """,
    ),
]