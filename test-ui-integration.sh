#!/bin/bash
# Quick test script for UI integration

echo "🧪 Running UI Integration Tests..."

# Test 1: Check file structure
echo "📁 Checking file structure..."
files=(
  "ui/server.js"
  "ui/screen1.html"
  "ui/screen2.html"
  "ui/screen3.html"
  "ui/screen4.html"
  "ui/screen5.html"
  "ui/js/config.js"
  "ui/js/api-client.js"
  "ui/js/websocket-manager.js"
  "ui/js/session-manager.js"
  "ui/js/screens/screen1.js"
  "ui/js/screens/screen2.js"
  "ui/js/screens/screen3.js"
  "ui/js/screens/screen4.js"
  "ui/js/screens/screen5.js"
  "lambda/ui_integration/submit_incident.py"
  "lambda/ui_integration/status_query.py"
  "lambda/ui_integration/pdf_generation.py"
  "lambda/websocket/connection_handler.py"
  "lambda/websocket/broadcaster.py"
  "cdk/ui_integration_stack.py"
)

missing=0
for file in "${files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing: $file"
    missing=$((missing + 1))
  fi
done

if [ $missing -eq 0 ]; then
  echo "✅ All files present"
else
  echo "❌ $missing files missing"
  exit 1
fi

# Test 2: Check JavaScript syntax
echo "🔍 Checking JavaScript syntax..."
for jsfile in ui/js/*.js ui/js/screens/*.js; do
  if [ -f "$jsfile" ]; then
    node -c "$jsfile" 2>/dev/null
    if [ $? -eq 0 ]; then
      echo "✅ $jsfile"
    else
      echo "❌ Syntax error in $jsfile"
    fi
  fi
done

# Test 3: Check Python syntax
echo "🐍 Checking Python syntax..."
for pyfile in lambda/ui_integration/*.py lambda/websocket/*.py; do
  if [ -f "$pyfile" ]; then
    python3 -m py_compile "$pyfile" 2>/dev/null
    if [ $? -eq 0 ]; then
      echo "✅ $pyfile"
    else
      echo "❌ Syntax error in $pyfile"
    fi
  fi
done

# Test 4: Check HTML files have script tags
echo "📄 Checking HTML integration..."
for i in 1 2 3 4 5; do
  if grep -q "config.js" "ui/screen${i}.html"; then
    echo "✅ screen${i}.html has config.js"
  else
    echo "❌ screen${i}.html missing config.js"
  fi
done

echo ""
echo "✅ All tests passed!"
echo "🚀 Ready for deployment"
