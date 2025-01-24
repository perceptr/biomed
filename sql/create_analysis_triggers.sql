CREATE TRIGGER analysis_insert_trigger
AFTER INSERT ON analyses
FOR EACH ROW EXECUTE FUNCTION log_analysis_history();

CREATE TRIGGER analysis_update_trigger
AFTER UPDATE ON analyses
FOR EACH ROW EXECUTE FUNCTION log_analysis_history();

CREATE TRIGGER analysis_delete_trigger
AFTER DELETE ON analyses
FOR EACH ROW EXECUTE FUNCTION log_analysis_history();