###########################################################################################
### Stage 0: Build
FROM node:20.9.0-bullseye as build

# Swith Workdiectory
WORKDIR /app

# Copy source code
COPY . .

# Install dependencies
# Replace with `npm ci` once a package-lock is added to the project
RUN npm install

# Build the application
RUN npm run build

###########################################################################################
### Stage 1: Deploy
FROM nginx:1.24.0-alpine as deploy

WORKDIR /app

# Copy built artifacts
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx serves on port 80
EXPOSE 80

###########################################################################################