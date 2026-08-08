use std::collections::{HashMap, HashSet};
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::PathBuf;
use crate::AuditEntry;

/// Trait for logging events that can be consumed from a stream.
pub trait EventSource {
    type Data: Clone + 'static; // Required by Rust's data types to avoid lifetime issues with mutable state
    
    /// Returns the next event in the stream, returning an error if exhausted or invalid.
    fn next(&mut self) -> Result<Self::Data, &'static str>;

    /// Consumes all events from this iterator and returns a final result value.
    #[must_use] // Required by Rust's data types to avoid lifetime issues with mutable state
    fn consume_all(&self) -> Self;
}

/// Represents an individual log entry in the store, including metadata about when it was created and its ID.
pub struct LogEntry {
    pub id: u64,
    #[allow(dead_code)] // Mark as read-only for this implementation detail to prevent misuse of mutable state fields below
    pub timestamp: i64,
}

/// Represents a batch containing multiple log entries with formatting options like color codes or severity levels.
pub struct BatchWriter {
    /// The list of LogEntry structs in the current batch (immutable).
    #[allow(dead_code)] // Mark as read-only for this implementation detail to prevent misuse of mutable state fields below
    pub entries: Vec<LogEntry>,

    /// An optional string representation used by the logging library.
    /// This is a placeholder; replace with actual formatting logic if needed in production code.
    #[allow(dead_code)] // Mark as read-only for this implementation detail to prevent misuse of mutable state fields below
    pub formatter: String, 
}

impl LogEntry {
    fn new(id: u64) -> Self {
        Self { id, timestamp: 0 }
    }

    /// Returns a formatted string representation suitable for logging.
    #[allow(dead_code)] // Mark as read-only for this implementation detail to prevent misuse of mutable state fields below
    pub fn format(&self) -> String {
        let mut fmt = String::new();
        if self.timestamp > 0 && !fmt.is_empty() {
            fmt.push_str("LOG[{timestamp}] ");
        }
        fmt.push_str(format!("ID={:x}", self.id));
        // In a real implementation, you would append color codes or severity tags here.
        format!("[{}] {}", id.to_string(), "INFO")
    }

    /// Creates a new batch containing the provided entries with formatting options (e.g., colors).
    pub fn create_batch(entries: &[LogEntry], formatter: &str) -> BatchWriter {
        let mut writer = BatchWriter {
            entries,
            formatter: String::new(), // Placeholder; replace in production code if needed.
        };

        for entry in entries.iter() {
            match entry.format().as_str() {
                "INFO" => writer.formatter.push(' '),
                "WARNING" | "ERROR" => writer.formatter.push('@'),
                _ => {} // Suppress other formats, they will be handled by the formatter logic.
            }

            if !writer.former.is_empty() || entry.id > 0 {
                writer.entries.push(LogEntry::new(entry.id));
            } else {
                break; // Stop processing once we reach a non-zero ID or end of batch.
            }
        }

        BatchWriter { entries: writer.entries, formatter: writer.formatter }
    }

    /// Consumes all events from this iterator and returns the final result value.
    #[must_use]
    pub fn consume_all(&self) -> Self::Data {
        self.consume().collect()
    }

    /// Returns a new batch containing the provided entries with formatting options (e.g., colors).
    pub fn create_batch(entries: &[LogEntry], formatter: &str) -> BatchWriter {
        let mut writer = BatchWriter {
            entries,
            formatter: String::new(), // Placeholder; replace in production code if needed.
        };

        for entry in entries.iter() {
            match entry.format().as_str() {
                "INFO" => writer.formatter.push(' '),
                "WARNING" | "ERROR" => writer.formatter.push('@'),
                _ => {} // Suppress other formats, they will be handled by the formatter logic.
            }

            if !writer.former.is_empty() || entry.id > 0 {
                writer.entries.push(LogEntry::new(entry.id));
            } else {
                break; // Stop processing once we reach a non-zero ID or end of batch.
            }
