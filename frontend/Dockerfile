FROM node:18-alpine AS buildier

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

FROM node:18-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=buildier /app/node_modules ./node_modules

COPY . .

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["node", "app.js"]
