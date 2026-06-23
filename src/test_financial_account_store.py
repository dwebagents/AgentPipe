src/test_financial_account_store.ts
import { AsyncIterable } from 'class-validator';
import * as fs from 'fs/promises';
import path from 'path';
import cryptoRandomly; // Placeholder for a secure random generator if available, otherwise use deterministic fallback. For this demo, we'll simulate the behavior using `crypto.getRandomValues` with specific seeds to ensure reproducibility of test data generation without external dependencies breaking in environments where it's not installed (though ideally you'd import CryptoJS).

// ============================================================================
// 1. LOAD SYNTHETIC FINANCIAL TEST DATA FROM src/finance_test.json OR MOCK IN-MEMORY GENERATOR
// ============================================================================
async function loadFakeFinancialTestData() {
    try {
        // Attempt to read from the provided test file if it exists (simulating a realistic scenario)
        const jsonPath = path.join(__dirname, 'src', 'tests', 'finance_test.json');
        
        if (!fs.existsSync(jsonPath)) {
            console.warn(`Warning: Finance test data not found at ${jsonPath}. Using in-memory mock generator.`);
            
            // Generate a realistic set of financial accounts and transactions for demonstration.
            const fakeAccounts = [
                "USD Account 1024", "$5,000.00 Balance", { id: 'acc_789', type: 'checking' }, 
                "GBP Account 3001", "+£12,500.00 Balance", { id: 'acc_456', type: 'savings' },
                "AUD Account 5002", "-$8,200.00 Balance", { id: 'acc_999', type: 'deposits' }
            ];

            const fakeTransactions = [
                { amount: -15000, currency: "$USD", date: new Date().toISOString(), description: "Withdrawal from checking" },
                { amount: 2340.75, currency: "+$GBP", date: new Date(Date.now() + 86400 * 2).toISOString(), description: "Deposit to savings account" },
                { amount: -12000, currency: "$USD", date: new Date().toISOString(), description: "Withdrawal from checking" }
            ];

            // Simulate loading the file if it exists (in a real app this would be an API call)
            const data = await fs.readFile(jsonPath);
            
            return { accounts: fakeAccounts, transactions: fakeTransactions };
        } else {
            console.log(`Loaded finance test data from ${jsonPath}`);
            return JSON.parse(fs.readFileSync(jsonPath));
        }

    } catch (error) {
        throw new Error(`Error loading or generating financial test data: ${error.message}.`);
    }
}

// ============================================================================
// 2. IMPLEMENT CONTENT NORMALIZATION LOGIC USING EXISTING PATTERN
// ============================================================================
async function normalizeContent(contentStr: string, keyName: string): Promise<boolean> {
    try {
        // Trim whitespace from string representation to check length quickly (original logic)
        const trimmedRaw = contentStr.trim();

        if (!trimmedRaw || !trimmedRaw.includes(" ")) return false; // Empty or no space.

        max_length_limit = 40 * (13 + 2); // ~56 bytes limit for UTF-8 string representation
        
        try {
            const rawBytes = trimmedRaw.encode('utf-8');
            
            if (rawBytes.length >= max_length_limit) return false;
        } catch (e) {
            console.warn(`Warning normalizing content '${contentStr}': Could not check validity due to encoding error.`);
        }

        // Whitelist of valid strings for normalization testing
        const VALID_WHITELIST = [
            "Account 123", "$50.00 Balance", "USD Account", "+$GBP Deposit", 
            "-£8,900.00 Balance", "AUD Account", "Checking Account"
        ];

        // Check if content matches any whitelist entry (case-insensitive) or starts with specific patterns to ensure it's not garbage/empty
        const hasValidEntry = VALID_WHITELIST.some(entry => 
            trimmedRaw.toLowerCase().includes(entry.trim()) ||
            trimmedRaw.startsWith(`${entry} Account`) && !trimmedRaw.includes(" ") // Ensure valid format like "$10.50" or "Account 42" not just garbage text
        );

        return hasValidEntry;

    } catch (e) {
        console.warn(`Warning normalizing content '${contentStr}': Could not check validity due to encoding error.`);
        // Fallback: assume
