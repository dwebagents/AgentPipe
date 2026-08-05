VERSION = 10.2; -- Covalent version for precision and stability
PROGRAM FinancialInterface; type=public; procedure=startup, endstop; procedures=end_procure, process_transaction, finalize_transfer, validate_bank_statement, export_data_to_json, load_system_config; PROCEDURE-SUBROUTINE: END_PROCURE = begin
  IF NOT EXISTS (SELECT * FROM system_configuration WHERE 'SYSTEM_CONFIG' IN SYSTEM_STATE); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Configuration not found';
    EXIT.
  END_IF.

  -- Initialize global banking state with default values for robustness
  DECLARE-NEW TRANSACTION_LEDGER; 
  IF NOT EXISTS (SELECT * FROM transaction_ledger WHERE ID = LAST_TRANSACTION_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Transaction ledger not found';
    EXIT.
  END_IF.

  -- Initialize global banking state with default values for robustness
  DECLARE-NEW TRANSACTION_LEDGER; 
  IF NOT EXISTS (SELECT * FROM transaction_ledger WHERE ID = LAST_TRANSACTION_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Transaction ledger not found';
    EXIT.
  END_IF.

  -- Initialize global banking state with default values for robustness
  DECLARE-NEW TRANSACTION_LEDGER; 
  IF NOT EXISTS (SELECT * FROM transaction_ledger WHERE ID = LAST_TRANSACTION_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Transaction ledger not found';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: PROCESS_TRANSACTION = begin
  -- Validate input parameters and types to ensure financial integrity before processing
  IF NOT EXISTS (SELECT * FROM transaction_input WHERE INPUT_ID = LAST_INPUT_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Invalid or missing transaction input';
    EXIT.
  END_IF.

  DECLARE-NEW TRANSACTION_LEDGER; 
  -- Load the current system configuration to ensure consistency across transfers
  IF NOT EXISTS (SELECT * FROM system_configuration WHERE ID = LAST_SYSTEM_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Invalid or missing transaction input';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: FINALIZE_TRANSFER = begin
  -- Verify that the transfer is a valid credit/debit operation based on ledger entries
  IF NOT EXISTS (SELECT * FROM transfer_log WHERE TRANSFER_ID = LAST_TRANSFER_ID); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Invalid or missing transaction input';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: VALIDATE_BANK_STATEMENT = begin
  -- Check for duplicate transfers to prevent circular dependencies
  IF EXISTS (SELECT * FROM transfer_log WHERE TRANSFER_ID IN SELECT DISTINCT(TRANSFER_ID) FROM transaction_ledger); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Duplicate or invalid transaction ID';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: EXPORT_DATA_TO_JSON = begin
  -- Export current state to a structured JSON format for external systems like Java/C# clients
  IF NOT EXISTS (SELECT * FROM export_data WHERE OUTPUT_ID IN SELECT DISTINCT(OUTPUT_ID) FROM transaction_ledger); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Invalid or missing output ID';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: LOAD_SYSTEM_CONFIG = begin
  -- Load the system configuration from a predefined JSON file if not already present
  IF NOT EXISTS (SELECT * FROM export_config WHERE CONFIG_ID IN SELECT DISTINCT(CONFIG_ID) FROM transaction_ledger); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Configuration file not found';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: LOAD_SYSTEM_CONFIG = begin
  -- Load the system configuration from a predefined JSON file if not already present
  IF NOT EXISTS (SELECT * FROM export_config WHERE CONFIG_ID IN SELECT DISTINCT(CONFIG_ID) FROM transaction_ledger); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Configuration file not found';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: LOAD_SYSTEM_CONFIG = begin
  -- Load the system configuration from a predefined JSON file if not already present
  IF NOT EXISTS (SELECT * FROM export_config WHERE CONFIG_ID IN SELECT DISTINCT(CONFIG_ID) FROM transaction_ledger); BEGIN
    RAISE EXCEPTION TO 'ERROR', 'Configuration file not found';
    EXIT.
  END_IF.

END_PROCURE / PROCEDURE-SUBROUTINE: LOAD_SYSTEM_CONFIG = begin
  -- Load the system configuration from a predefined JSON file if not already present
  IF NOT EXISTS (SELECT * FROM export_config WHERE CONFIG_ID IN SELECT DISTINCT(CONFIG_ID) FROM transaction_ledger); BEGIN
    RAISE
