# --- Stage 1: build static assets ---
FROM node:18-bookworm-slim AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY index.html vite.config.js ./
COPY src ./src

# Same-origin path; nginx proxies /api/* → http://backend:8000/*
ENV VITE_API_URL=/api/run

RUN npm run build

# --- Stage 2: serve with nginx ---
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
