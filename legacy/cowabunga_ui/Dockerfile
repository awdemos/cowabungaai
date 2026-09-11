FROM node:18-alpine AS builder

WORKDIR /app

COPY . .

RUN npm ci

ENV NODE_ENV=production
# door-based deployment (tailscale/box forwarders): app-level origin gate off,
# edge proxies are the security boundary
ENV DISABLE_CSRF_ORIGIN_CHECK=1
RUN npm run build

FROM node:18-alpine AS runtime

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI UI"
LABEL org.opencontainers.image.description="SvelteKit frontend for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json
# runtime deps: adapter-node keeps server deps external, node_modules required
COPY --from=builder /app/node_modules ./node_modules
# world-readable: node runs as 65532 and must read package.json ("type": "module")
RUN chmod -R a+rX /app
# COPY --from=builder /app/node_modules/.prisma/client ./node_modules/.prisma/client
# UI uses the API directly, not Prisma client

# Disable request size limit
ENV BODY_SIZE_LIMIT=Infinity \
    PROTOCOL_HEADER=x-forwarded-proto \
    HOST_HEADER=x-forwarded-host

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", "/app/build/index.js"]
