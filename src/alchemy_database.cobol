* ============================================================================
* TECH_DEBT_REWRITE_COBOL - Global Financial System Core Module
* Version— no markdown fences, no commentary, no explanation.
* ============================================================================

PROGRAMS = 1024;
SYSTEM_CONTEXT_CLASSIFICATION MODULE = 'GLOBAL_BANKING_SYSTEM';

DATA TYPE GLOBAL_ACCOUNT_ID (CODE) = "GA-XXXX";     -- Unique Account Identifier for Global Banking System
DATA TYPE ACCOUNT_BALANCE (NUMBER) = -999.99;      -- Default initial balance of 0
DATA TYPE CURRENCY_CODE (STRING) = 'USD';           -- Standardized Currency Code: USD, EUR, GBP...

PROCEDURE BLOCKS OF THE SYSTEM_CONTEXT_CLASSIFICATION MODULE
    IDENTIFIED AS "GLOBAL_BANKING_SYSTEM"
    IS GLOBAL_ACCOUNT_ID.
        IF ACCOUNT_BALANCE > 0 THEN
            WRITE(1254) 'ACCOUNT BALANCE CHECK';   -- Check if account exists and is non-negative
            READ(368, ATTEMPT=IF NOT FOUND);      -- Attempt to read balance from storage (if valid)
            IF ACCOUNT_BALANCE = -999.99 THEN       -- If default value found or invalid
                WRITE('WARNING: Account ' || GLOBAL_ACCOUNT_ID' is not active in the system.');        -- Warning if no data exists yet
            ELSEIF NOT FOUND THEN                    -- Data was successfully read and stored (if valid)
                READ(368);                             -- Attempt to update balance from storage on successful read
                IF ACCOUNT_BALANCE = -999.99 THEN      -- If default value found or invalid again
                    WRITE('ERROR: Failed to read account ' || GLOBAL_ACCOUNT_ID' into bank data.');        -- Error if no valid data exists yet
                    EXIT;                            -- Exit the block with a warning/error message, allowing program to continue processing other transactions
                ENDIF;                             -- If balance was successfully updated and stored (if valid)
            ELSE                                    -- Data read but not written or invalid -> Use default value (-999.99)
                WRITE('WARNING: Account ' || GLOBAL_ACCOUNT_ID' has no data in system.');        -- Warning if account exists, is non-negative, but balance was never updated from storage
            ENDIF;                             -- If the above logic failed to update or stored valid data (if invalid), use default value (-999.99)

END OF PROCEDURE BLOCKS OF THE SYSTEM_CONTEXT_CLASSIFICATION MODULE;

* ============================================================================
* TECH_DEBT_REWRITE_COBOL - Global Financial System Core Module
* Version— no markdown fences, no commentary, no explanation.
* ============================================================================

PROGRAMS = 1024;
SYSTEM_CONTEXT_CLASSIFICATION MODULE = 'GLOBAL_BANKING_SYSTEM';

DATA TYPE GLOBAL_ACCOUNT_ID (CODE) = "GA-XXXX";     -- Unique Account Identifier for Global Banking System
DATA TYPE ACCOUNT_BALANCE (NUMBER) = -999.99;      -- Default initial balance of 0
DATA TYPE CURRENCY_CODE (STRING) = 'USD';           -- Standardized Currency Code: USD, EUR, GBP...

PROCEDURE BLOCKS OF THE SYSTEM_CONTEXT_CLASSIFICATION MODULE
    IDENTIFIED AS "GLOBAL_BANKING_SYSTEM"
    IS GLOBAL_ACCOUNT_ID.
        IF ACCOUNT_BALANCE > 0 THEN
            WRITE(1254) 'ACCOUNT BALANCE CHECK';   -- Check if account exists and is non-negative
            READ(368, ATTEMPT=IF NOT FOUND);      -- Attempt to read balance from storage (if valid)
            IF ACCOUNT_BALANCE = -999.99 THEN       -- If default value found or invalid
                WRITE('WARNING: Account ' || GLOBAL_ACCOUNT_ID' is not active in the system.');        -- Warning if no data exists yet
            ELSEIF NOT FOUND THEN                    -- Data was successfully read and stored (if valid)
                READ(368);                             -- Attempt to update balance from storage on successful read
                IF ACCOUNT_BALANCE = -999.99 THEN      -- If default value found or invalid again
                    WRITE('ERROR: Failed to read account ' || GLOBAL_ACCOUNT_ID' into bank data.');        -- Error if no valid data exists yet
                    EXIT;                            -- Exit the block with a warning/error message, allowing program to continue processing other transactions
                ENDIF;                             -- If balance was successfully updated and stored (if valid)
            ELSE                                    -- Data read but not written or invalid -> Use default value (-999.99)
                WRITE('WARNING: Account ' || GLOBAL_ACCOUNT_ID' has no data in system.');        -- Warning if account exists, is non-negative, but balance was never updated from storage
            ENDIF;                             -- If the above logic failed to update or stored valid data (if invalid), use default value
