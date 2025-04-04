FROM node:23 AS build

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm i --save-dev @types/bootstrap
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]