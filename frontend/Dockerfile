# ---- Build stage ----
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source files
COPY . ./

# Build Next.js (static generation)
RUN npm run build

# ---- Runtime stage ----
FROM nginx:alpine
COPY --from=builder /app/.next /usr/share/nginx/html/.next
COPY --from=builder /app/public /usr/share/nginx/html/public
COPY --from=builder /app/next.config.js /usr/share/nginx/html/next.config.js
COPY --from=builder /app/package.json /usr/share/nginx/html/package.json

# Expose HTTP port (Render will map $PORT to 80 automatically)
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
