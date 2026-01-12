FROM node:18-alpine AS builder

RUN apk update && apk upgrade && \
    apk add --no-cache libreoffice openjdk11-jre fontconfig msttcorefonts-installer \
    && update-ms-fonts \
    && fc-cache -f

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=${JAVA_HOME}/bin:$PATH

WORKDIR /app

COPY . .

RUN npm ci

ENV NODE_ENV=production
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
# COPY --from=builder /app/node_modules/.prisma/client ./node_modules/.prisma/client
# UI uses Supabase directly, not Prisma client

# Disable request size limit
ENV BODY_SIZE_LIMIT=Infinity \
    PROTOCOL_HEADER=x-forwarded-proto \
    HOST_HEADER=x-forwarded-host

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

CMD ["build"]
