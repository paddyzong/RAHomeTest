# Step 1: Build the React application
FROM node:16 AS build

# Set working directory in container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project into the container
COPY . .

# Build the React application for production using craco
RUN npm run build

# Step 2: Serve the app with NGINX
FROM nginx:alpine

# Copy the build output to NGINX's default location
COPY --from=build /app/build /usr/share/nginx/html

# Expose the default port for NGINX
EXPOSE 80

# Optional: Customize NGINX config if needed
COPY nginx.conf /etc/nginx/nginx.conf

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
