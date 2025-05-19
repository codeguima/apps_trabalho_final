FROM node:22-alpine

WORKDIR /app


COPY ./  /app

RUN npm install express
RUN npm install axios

EXPOSE 3000

CMD ["node", "app.js"]



