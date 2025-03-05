# Installation

This guide will help you install Mubble and set up your development environment.

## Requirements

- Python 3.8 or higher
- pip or poetry package manager

## Installing with pip

The simplest way to install Mubble is using pip:

```bash
pip install mubble
```

To install a specific version:

```bash
pip install mubble==1.6.0
```

## Installing with Poetry

If you're using Poetry for dependency management:

```bash
poetry add mubble
```

## Installing from Source

You can also install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/vladislavkovalskyi/mubble.git#master
```

Or with Poetry:

```bash
poetry add git+https://github.com/vladislavkovalskyi/mubble.git#master
```

## Verifying Installation

To verify that Mubble has been installed correctly, you can run a simple Python script:

```python
import mubble

print(f"Mubble installed successfully!")
```

## Optional Dependencies

Mubble works out of the box with its default dependencies. However, you might want to install additional packages for specific features:

- `aiosonic`: For an alternative HTTP client with potentially better performance
- `msgpack`: For efficient serialization of callback data

Install these with:

```bash
pip install mubble[full]
```

Or with Poetry:

```bash
poetry add mubble[full]
```

## Next Steps

Now that you have Mubble installed, check out the [Quick Start](quickstart.md) guide to create your first bot. 