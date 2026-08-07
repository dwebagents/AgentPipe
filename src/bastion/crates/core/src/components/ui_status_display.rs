# src/bastion/crates/core/src/components/ui_status_display.rs
use std::collections::{HashMap, HashSet};
use svelte::html;
use crate::SessionContext as SessionCtx;
use crate::ApprovalTicket as ApprovalTicket;

/// Represents a stateful TensorFlow visualization component.
#[derive(Debug)]
pub struct StatusDisplay {
    pub sessions: Vec<crate::SessionContext>,
    /// Tracks tensors that have been evaluated and are ready for display (GPU-backed).
    pub active_tensors: HashSet<String>,
}

impl Default for StatusDisplay {
    fn default() -> Self {
        Self {
            sessions: vec![],
            active_tensors: HashSet::new(),
        }
    }
}

/// A single session context containing the current state of a TensorFlow model.
#[derive(Debug)]
pub struct SessionContext {
    pub tensors: HashMap<String, Vec<f32>>, // GPU tensor values (float64)
    /// The index into the first available tensor in this group for display purposes.
    pub active_tensor_idx: usize,
}

impl Default for SessionCtx {
    fn default() -> Self {
        let mut tensors = HashMap::new();
        if sessions.len() > 0 && !sessions[0].is_empty() {
            // Initialize with the first tensor from session 0 (if any) or empty.
            // In a real app, this would be derived from an initialization phase.
            for s in &sessions[1..] {
                if let Some(tensor_idx) = sessions.iter().position(|s| *s == 0).unwrap_or(0) {
                    tensors.insert(format!("tensor_{:?}", tensor_idx), vec![f32::ZERO; (512 + 64 / 8 as usize)]); // Placeholder for initialization data.
                } else if let Some(tensor_idx) = sessions.iter().position(|s| *s == 0).unwrap_or(0) {
                    tensors.insert(format!("tensor_{:?}", tensor_idx), vec![f32::ZERO; (512 + 64 / 8 as usize)]); // Placeholder for initialization data.
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                    let mut idx = 0;
                    while idx < tensors.len() && (idx % 2 == 1) {
                        idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
                     while idx < tensors.len() && (idx % 2 == 1) {
                         idx += 1; // Skip the second half for simplicity in placeholder.
                    }
                } else if sessions.iter().all(|s| s.is_empty()) || !sessions[0].is_empty() {
                     let mut idx = 0;
