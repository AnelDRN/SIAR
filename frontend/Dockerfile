# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install app dependencies
# RUN npm install

# Bundle app source
COPY . .

# Creates a "production" build
# RUN npm run build

# The main command to run when the container starts
CMD ["npm", "start"]
