# syntax=docker/dockerfile:1

FROM node:20-alpine3.18 AS build

WORKDIR /app/

# Add and install node_modules
ADD ./package.json /app/package.json
RUN npm install

# Add env variables
ADD ./.docker.env /app/.env

# Add (config and manage) files
ADD ./index.html /app/index.html
ADD ./package-lock.json /app/package-lock.json
ADD ./vite.config.js /app/vite.config.js

# Add script-files
ADD ./public /app/public
ADD ./src /app/src

# build project
RUN npm run build


FROM nginx:stable

# Add nginx config and app source
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]
