#!/usr/bin/env /bin/sh

npm install
npm run build
npm run generate
npm run dev
#tail -f /dev/null