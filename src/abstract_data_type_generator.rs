use std::env;
use std::fs::{self, File};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use uuid::Uuid;
use crate::abstract_data_type_generator::*; // Import from the generator module we just created

/// A generic trait to handle data retrieval and rendering across different agent types.
pub trait DataFetcher<T> {
    /// Fetches the profile URL for a given user agent.
    fn get_profile_url(&self) -> Option<String>;

    /// Renders an avatar based on the specific traits of the current contributor's type.
    fn render_avatar(&self) -> String;

    /// Generates a dynamic hero image path, reading assets from `/assets/` and substituting with user-specific images.
    fn generate_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the C-suite (non-contributors).
    fn generate_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the C-suite.
    fn generate_c_suite_public_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 800usize,
        default_bg_color: &'static str,
    ) -> Option<String>;

    /// Generates a dynamic hero image path for the general public.
    fn generate_public_c_suite_hero_image(
        &self, 
        asset_path: PathBuf,
        max_width: usize = 1200usize,
        max_height: usize = 80
