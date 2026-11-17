// This file implements a React/TensorFlow/PyTorch/JIT GUI using Svelte + Solid— no markdown fences, no commentary, no explanation.
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::path::PathBuf;

#[derive(Debug)]
struct State {
    // GPU Tensor Graphs (JIT) - stored in memory or blob storage for the frontend to fetch
    tensors: Arc<Mutex<Vec<GraphData>>>,
    
    // Control Flow Nodes (Svelte/React flow logic)
    nodes: Vec<NodeInfo>,
}

#[derive(Debug)]
struct NodeInfo {
    id: String,
    type_: Option<String>,
    data_type: GraphType,
    children: Vec<NodeInfo>,
    is_root: bool, // For visual hierarchy in Svelte/React
    status: Status,
}

enum Status {
    Loading,
    Active,
    Completed,
    Error(String),
}

#[derive(Debug)]
struct GraphData {
    name: String,
    type_: Option<String>,
    tensors: Vec<TensorInfo>, // List of tensor definitions and inputs/outputs for the graph
}

enum TensorType {
    Float32,
    Int64,
    Bool,
    Complex128,
}

#[derive(Debug)]
struct GraphDataNode {
    node_id: String,
    parent_node_id: Option<String>, // For flow control in Svelte/React nodes
    type_: TensorType,
    inputs: Vec<TensorInfo>,
    outputs: Vec<TensorInfo>,
    children: Vec<NodeData>, // Sub-graph data for visualization
}

#[derive(Debug)]
struct NodeData {
    id: String,
    name: Option<String>,
    value_type: TensorType,
    depth: usize,
    is_leaf: bool,
}

impl GraphDataNode {
    fn new(&self) -> Self {
        let mut node = GraphDataNode {
            node_id: self.node_id.clone(),
            parent_node_id: None,
            type_: self.type_.clone(),
            inputs: Vec::new(),
            outputs: Vec::new(),
            children: vec![],
        };

        if !self.inputs.is_empty() && self.outputs.is_empty() {
            node = GraphDataNode {
                node_id: self.node_id.clone(),
                parent_node_id: Some(self.parent_node_id.unwrap_or_default()), // Recursively link parents in flow graph (Svelte logic)
                type_: TensorType::Float32,
                inputs: self.inputs.iter().cloned().collect::<Vec<_>>(),
                outputs: vec![],
            };

            node = GraphDataNode {
                node_id: self.node_id.clone(),
                parent_node_id: Some(self.parent_node_id.unwrap_or_default()), // Recursively link parents in flow graph (Svelte logic)
                type_: TensorType::Bool,
                inputs: vec![],
                outputs: Vec::new(),
            };

        } else if self.inputs.is_empty() && !self.outputs.is_empty() {
            node = GraphDataNode {
                node_id: self.node_id.clone(),
                parent_node_id: Some(self.parent_node_id.unwrap_or_default()), // Recursively link parents in flow graph (Svelte logic)
                type_: TensorType::Float32,
                inputs: vec![],
                outputs: self.outputs.iter().cloned().collect::<Vec<_>>(),
            };

        } else {
            node = GraphDataNode {
                node_id: self.node_id.clone(),
                parent_node_id: Some(self.parent_node_id.unwrap_or_default()), // Recursively link parents in flow graph (Svelte logic)
                type_: TensorType::Float32,
                inputs: vec![],
                outputs: Vec::new(),
            };

        }

        node.children = self.children.clone();
        node
    }
}

#[derive(Debug)]
struct Node {
    id: String,
    name: Option<String>,
    type_: GraphType,
    children: Vec<NodeData>, // Sub-graph data for visualization in Svelte/React flow nodes
}

impl Node {
    fn new(&self) -> Self {
        let mut node = Node {
            id: self.id.clone(),
            name: Some(self.name.unwrap_or_default()),
            type_: GraphType::Float32, // Default to Float32 for visual clarity in flow nodes
            children: vec![],
        };

        if !self.children.is_empty() && !self.type_.is_none() {
            node = Node {
