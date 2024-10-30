# events-web-gui/Dockerfile

# Stage 1: Build the Angular app with Node.js
FROM node:14 AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY events-web-gui/package*.json ./
RUN npm install

# Copy Angular app source files
COPY events-web-gui/ ./

# Build the Angular app for production
RUN npm run build --prod

# Stage 2: Serve the app with Nginx
FROM nginx:alpine


# Copy the built files from the previous stage
COPY --from=build /app/dist/events-web-gui /usr/share/nginx/html

# Copy custom Nginx config
COPY events-web-gui/nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod -R 755 /usr/share/nginx/html/assets

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
