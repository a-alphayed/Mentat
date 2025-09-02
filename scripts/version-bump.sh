#!/bin/bash
# Version bumping script for Mentat Framework

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get current version
CURRENT_VERSION=$(cat VERSION)
echo -e "${GREEN}Current version: $CURRENT_VERSION${NC}"

# Parse version components
IFS='-' read -r VERSION_CORE VERSION_SUFFIX <<< "$CURRENT_VERSION"
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION_CORE"

# Get bump type
BUMP_TYPE="${1:-patch}"

case "$BUMP_TYPE" in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    echo -e "${YELLOW}Bumping MAJOR version${NC}"
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    echo -e "${YELLOW}Bumping MINOR version${NC}"
    ;;
  patch)
    PATCH=$((PATCH + 1))
    echo -e "${YELLOW}Bumping PATCH version${NC}"
    ;;
  *)
    echo -e "${RED}Invalid bump type. Use: major, minor, or patch${NC}"
    exit 1
    ;;
esac

# Construct new version
NEW_VERSION="$MAJOR.$MINOR.$PATCH"
if [ -n "$VERSION_SUFFIX" ]; then
  NEW_VERSION="$NEW_VERSION-$VERSION_SUFFIX"
fi

echo -e "${GREEN}New version: $NEW_VERSION${NC}"

# Update VERSION file
echo "$NEW_VERSION" > VERSION

# Update pyproject.toml
sed -i '' "s/^version = .*/version = \"$NEW_VERSION\"/" pyproject.toml

# Create git commit and tag
git add VERSION pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo -e "${GREEN}✅ Version bumped to $NEW_VERSION${NC}"
echo -e "${YELLOW}Don't forget to push: git push origin main --tags${NC}"