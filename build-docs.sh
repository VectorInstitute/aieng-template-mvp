#!/bin/bash
set -e

# Build frontend as static site
echo "Building Next.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Create template-ui directory in docs/assets
echo "Setting up template UI in docs..."
mkdir -p docs/assets/template-ui
cp -r frontend/out/* docs/assets/template-ui/

# Ensure images are available in multiple locations
mkdir -p docs/assets/template-ui/images
cp -r frontend/public/images/* docs/assets/template-ui/images/

# Also copy images to root of template-ui
cp -r frontend/public/images/* docs/assets/template-ui/

# And to assets directory
mkdir -p docs/assets/images
cp -r frontend/public/images/* docs/assets/images/

# Build MkDocs site (which will include the template UI)
echo "Building MkDocs site..."
mkdocs build

# Copy images to multiple locations in the site directory
mkdir -p site/assets/template-ui/images
cp -r frontend/public/images/* site/assets/template-ui/images/

# Copy to root of template-ui
cp -r frontend/public/images/* site/assets/template-ui/

# Copy to site/assets/images
mkdir -p site/assets/images
cp -r frontend/public/images/* site/assets/images/

# Copy to site/images
mkdir -p site/images
cp -r frontend/public/images/* site/images/

# Add .nojekyll file to ensure GitHub Pages works correctly with underscore-prefixed files
touch site/.nojekyll

echo "Build complete! The combined site is in the 'site' directory."
echo "The template UI is accessible via the 'Template UI' tab in the documentation."
echo "To serve the site locally: cd site && python -m http.server 8000"
