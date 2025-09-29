FROM node:22
WORKDIR /app
COPY app/ .
RUN npm install
RUN npm install diskusage
CMD ["node", "server.js"]