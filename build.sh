#!/bin/bash
set -e

# Build MkDocs site
echo "Building MkDocs site..."
mkdocs build

# Build frontend as static site
echo "Building Next.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Move Next.js output to a temporary directory
echo "Preparing to merge sites..."
mkdir -p tmp_next_out
cp -r frontend/out/* tmp_next_out/

# Create the combined site directory
echo "Creating combined site..."
mkdir -p combined_site

# Copy MkDocs site to combined site
cp -r site/* combined_site/

# Create app directory in the combined site and copy Next.js output there
mkdir -p combined_site/app
cp -r tmp_next_out/* combined_site/app/

# Create redirect from root to app
cat > combined_site/index.html <<EOL
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url='app/'" />
  <title>Vector Institute AI Engineering</title>
</head>
<body>
  <p>Redirecting to <a href="app/">Vector AI Engineering Template</a></p>
</body>
</html>
EOL

# Create navigation helper in the docs to app
cat > combined_site/to_app.html <<EOL
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url='app/'" />
  <title>Vector Institute AI Engineering</title>
</head>
<body>
  <p>Redirecting to <a href="app/">Vector AI Engineering Template</a></p>
</body>
</html>
EOL

# Clean up temp directory
rm -rf tmp_next_out

echo "Build complete! Combined site is in the 'combined_site' directory."
