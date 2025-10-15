# Base image
FROM node:16-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json . 
COPY package-lock.json . 
RUN npm install

# Copy project
COPY . .

# Default command
CMD ["npm", "start"]
