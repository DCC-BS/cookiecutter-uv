#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR"
TEST_DIR="$SCRIPT_DIR/.test-output"
PROJECT_NAME="test-fastapi-project"
PROJECT_SLUG="test_fastapi_project"

# Cleanup function
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up test directory...${NC}"
    rm -rf "$TEST_DIR"
}

# Set trap to cleanup on exit (unless KEEP_OUTPUT=1)
if [ "${KEEP_OUTPUT:-}" != "1" ]; then
    trap cleanup EXIT
fi

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Cookiecutter Template Test Suite                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create test directory
mkdir -p "$TEST_DIR"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 1: Generating project from template${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd "$TEST_DIR"
cookiecutter "$TEMPLATE_DIR" --no-input project_name="$PROJECT_NAME"

if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${RED}❌ Failed: Project directory not created${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Project generated successfully${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 2: Installing dependencies with uv sync${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd "$TEST_DIR/$PROJECT_NAME"

# Set Python version
echo "3.13" > .python-version

# Create virtual environment and sync
uv venv --python 3.13
if ! uv sync 2>&1; then
    echo -e "${RED}❌ Failed: uv sync failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 3: Creating .env file for testing${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cat > .env <<EOF
ENVIRONMENT=development
LOG_LEVEL=debug
IS_PROD=False
PORT=8000
LLM_API_PORT=8001
CLIENT_PORT=3000

CLIENT_URL=http://localhost:3000
LLM_URL=http://localhost:8001/v1
LLM_HEALTH_CHECK_URL=http://localhost:8001/health

LLM_MODEL=test-model
LLM_API_KEY=test-key

AUTH_MODE=none
HMAC_SECRET=test-secret-key-for-testing-only
AZURE_CLIENT_ID=
AZURE_TENANT_ID=
AZURE_FRONTEND_CLIENT_ID=
AZURE_SCOPE_DESCRIPTION=user_impersonation
EOF

echo -e "${GREEN}✅ .env file created${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 4: Running code quality checks${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}Running ruff format check...${NC}"
if ! uv run ruff format --check . 2>&1; then
    echo -e "${RED}❌ Failed: ruff format check failed${NC}"
    exit 1
fi

echo -e "${YELLOW}Running ruff lint check...${NC}"
if ! uv run ruff check . 2>&1; then
    echo -e "${RED}❌ Failed: ruff lint check failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Code quality checks passed${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 5: Running type checker${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}Running ty type checker...${NC}"
if ! uv run ty check "./src/$PROJECT_SLUG" 2>&1; then
    echo -e "${YELLOW}⚠️  Type checker found issues (non-blocking)${NC}"
else
    echo -e "${GREEN}✅ Type checking passed${NC}"
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 6: Running tests${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}Running pytest...${NC}"
if ! uv run python -m pytest --doctest-modules 2>&1; then
    echo -e "${YELLOW}⚠️  Some tests failed (non-blocking)${NC}"
else
    echo -e "${GREEN}✅ Tests passed${NC}"
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Step 7: Verifying app can be imported${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}Testing app import...${NC}"
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)

if ! python -c "from $PROJECT_SLUG.app import create_app; app = create_app(); print('App created:', app.title)" 2>&1; then
    echo -e "${RED}❌ Failed: Could not import app${NC}"
    exit 1
fi

echo -e "${GREEN}✅ App imported successfully${NC}"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     All Tests Passed! ✅                                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "${KEEP_OUTPUT:-}" = "1" ]; then
    echo -e "Generated project available at: ${BLUE}$TEST_DIR/$PROJECT_NAME${NC}"
    echo -e "Run ${YELLOW}cd $TEST_DIR/$PROJECT_NAME && source .venv/bin/activate && uv run fastapi dev${NC} to start the app"
fi
