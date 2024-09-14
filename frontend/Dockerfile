FROM node:alpine as base
WORKDIR /app
ARG API_URL
ENV VITE_API_URL=$API_URL
COPY package.json .
RUN npm cache verify
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=base /app/dist /dist/
COPY --from=base /app/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD [ "nginx","-g","daemon off;" ]
