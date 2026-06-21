package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"math/big"
	"os"
	"strings"
)

// financialType is the type of money managed.
const (
	Credit    = "credit"
	SuperWallet = "super_wallet"
	Out       = "out"
)

type FinancialData struct {
	ID            string  `json:"id"`      // ID for reference to specific accounts/reports
	Description   *string `json:"description,omitempty"`
	Amount        float64 `json:"amount"`  // The amount requested, can be negative if withdrawing money
	Type          financialType `json:"type"        `
}

// MCPRequest represents a request sent to the "Mental Bank".
type MCPRequest struct {
	RequestID    string      `json:"request_id"`  // Unique ID for this client session/transaction.
	Operation   string        `json:"operation"`     // Action: e.g., "add_fund_credits", "withdraw_credits", "calculate_balance".
	Data         interface{} // The actual data to process (JSON encoded).
}

// MCPResponse represents the parsed response from an API call sent via our SDK.
type MCPResponse struct {
	ID          string      `json:"id"`       // ID for reference.
	Amount      float64     `json:"amount"   // Amount received or paid.
	Type        financialType  // 'credits', "super_wallet", or "out".
}

// Represents the parsed data from a request/response pair.
type FinancialData struct {
	ID            string    `json:"id"`      // ID for reference to specific accounts/reports
	Description   *string     // Optional description of transaction type (e.g., "pay_credits", "draw_cash")
	Amount        float64     // The amount requested, can be negative if withdrawing money
	Type          financialType  // 'credits', 'cash_in' or 'out' depending on the action.
}

func main() {
	fmt.Println("Starting Financial System...")
	
	account := &InternalAccount{
		ID:        "acc_01",
		Balance:   500.75,
		FundType:  financialType.Credit, // Default to credit for demonstration
	}

	request := MCPRequest{
