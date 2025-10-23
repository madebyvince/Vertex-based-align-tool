# Contributing to Vertex Align Tool

Thank you for considering contributing to the Vertex Based Align Tool! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your Blender version
- Screenshots or error messages if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- A clear description of the enhancement
- Why this would be useful
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style below
3. **Test your changes** thoroughly in Blender
4. **Update documentation** if you're adding new features
5. **Submit a pull request** with a clear description of your changes

## Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions focused on a single task
- Use Blender's naming conventions for operators and panels:
  - Operator classes: `OBJECT_OT_operator_name`
  - Panel classes: `VIEW3D_PT_panel_name`
  - Operator IDs: `object.operator_name`

## Testing

Before submitting a pull request:
- Test the add-on in Blender 3.0+
- Test both position-only and position+rotation alignment
- Test edge cases (invalid selections, missing objects, etc.)
- Ensure the add-on can be installed, enabled, and disabled without errors

## Questions?

Feel free to open an issue if you have any questions about contributing!
