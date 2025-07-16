# frontend/Dockerfile
FROM node:22-alpine AS frontend-builder

WORKDIR /app
COPY . .

RUN npm install && npm run build

FROM nginx:alpine
COPY --from=frontend-builder /app/dist /usr/share/nginx/html