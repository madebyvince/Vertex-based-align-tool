# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-12-31

### Added
- Support for 3-vertex alignment enabling complete 3D orientation matching
- "Mark Source Vertex 3" and "Mark Target Vertex 3" operators
- Sequential alignment algorithm: first aligns vertices 1-2, then rotates around 1→2 axis to align vertex 3
- Third vertex display in UI panel for both source and target objects
- Automatic position correction after final rotation to ensure perfect alignment

### Changed
- Updated "Align objects" button to show three modes: "Position Only", "Partial Rotation", or "Full Rotation"
- Enhanced alignment logic to handle 1, 2, or 3 vertex configurations automatically

### Improved
- More robust alignment for complex orientations
- Complete control over all three rotation axes
- Better handling of edge cases in rotation calculations

## [3.0.0] - 2025-10-23

### Added
- Explicit target vertex marking with dedicated buttons
- Smart single "Align objects" button that automatically detects alignment mode
- Separate display sections for source and target objects in UI panel
- Visual feedback showing which vertices are marked with checkmarks
- Dynamic button text showing whether rotation will be applied

### Changed
- Replaced separate "Align Position Only" and "Align Position + Rotation" buttons with single smart "Align objects" button
- Improved UI layout with clearer separation between source and target
- Renamed "Clear Marked Vertices" to "Clear All" for brevity

### Improved
- More intuitive workflow with explicit target marking
- Better visual feedback throughout the process
- Clearer instructions in the panel

## [2.0.0] - 2025-10-23

### Added
- Rotation alignment feature using two vertices per object
- "Mark Source Vertex 2" button for direction definition
- "Align Position + Rotation" operator
- Validation to ensure vertex 2 is different from vertex 1

### Changed
- Updated UI to accommodate rotation features
- Enhanced instructions to cover both alignment modes

## [1.0.0] - 2025-10-23

### Added
- Initial release
- Basic position-only alignment using single vertex per object
- "Mark Source Vertex" button
- "Align Position Only" operator
- Panel in 3D Viewport sidebar
- Clear marked vertices functionality
- Basic instructions in UI
