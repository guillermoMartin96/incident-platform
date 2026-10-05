from yoyo import step


steps = [
    step(
        """
        CREATE TABLE incidents (
            incident_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

            service VARCHAR(255) NOT NULL,

            severity VARCHAR(20) NOT NULL
                CHECK (
                    severity IN (
                        'low',
                        'medium',
                        'high',
                        'critical'
                    )
                ),

            description TEXT NOT NULL,

            resolved BOOLEAN NOT NULL DEFAULT FALSE
        );
        """,
        """
        DROP TABLE incidents;
        """,
    )
]