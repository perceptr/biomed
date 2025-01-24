CREATE OR REPLACE FUNCTION log_analysis_history()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO analysis_history (
            analysis_id,
            user_id,
            name,
            s3_address,
            assigned_operator_id,
            result,
            status,
            created_at,
            updated_at,
            operation,
            operation_timestamp
        ) VALUES (
            OLD.id,
            OLD.user_id,
            OLD.name,
            OLD.s3_address,
            OLD.assigned_operator_id,
            OLD.result,
            OLD.status,
            OLD.created_at,
            OLD.updated_at,
            'DELETE',
            NOW()
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO analysis_history (
            analysis_id,
            user_id,
            name,
            s3_address,
            assigned_operator_id,
            result,
            status,
            created_at,
            updated_at,
            operation,
            operation_timestamp
        ) VALUES (
            NEW.id,
            NEW.user_id,
            NEW.name,
            NEW.s3_address,
            NEW.assigned_operator_id,
            NEW.result,
            NEW.status,
            NEW.created_at,
            NEW.updated_at,
            'UPDATE',
            NOW()
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO analysis_history (
            analysis_id,
            user_id,
            name,
            s3_address,
            assigned_operator_id,
            result,
            status,
            created_at,
            updated_at,
            operation,
            operation_timestamp
        ) VALUES (
            NEW.id,
            NEW.user_id,
            NEW.name,
            NEW.s3_address,
            NEW.assigned_operator_id,
            NEW.result,
            NEW.status,
            NEW.created_at,
            NEW.updated_at,
            'INSERT',
            NOW()
        );
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;