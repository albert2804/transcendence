#!/usr/bin/env /bin/sh

# check the NODE_ENV environment variable
if [ "$NODE_ENV" = "production" ]; then
    # echo "Running in production mode"
    npm install --omit=dev
    npm run build
    node .output/server/index.mjs
else
    # echo "Running in development mode"
    npm install
    npm run dev
    # tail -f /dev/null
fi