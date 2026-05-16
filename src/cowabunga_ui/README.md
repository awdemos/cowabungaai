# CowabungaAI UI

> [!IMPORTANT]
> See the [UI package documentation](../../packages/UI/README.md) for general pre-requisites, dependent components, and package deployment instructions

This document is only applicable for spinning up the UI in a local Node development environment.

## Local Development Setup

> [!IMPORTANT]
> Execute the following commands from this sub-directory

### Running

1. Install dependencies

   ```bash
   npm install
   ```

2. Create a .env using the .env.example as a template.

3. Some backend functionality within the app requires libreoffice (for converting files to PDFs). While not required for
   the app to run, if you are running the app locally without using the Dockerfile (e.g. via npm run dev), you will
   need to install libreoffice.

   ex. ```brew install libreoffice``` or ```sudo apt install libreoffice```

4. Run the Node application and open in your default browser

   ```bash
   npm run dev -- --open
   ```

### Building

To create a production version of the app:

```bash
npm run build
```

You can preview the production build with ```npm run preview```.

### Configuration Options

#### API

It is recommended to run CowabungaAI with UDS, but if you want to run the UI locally (on localhost, e.g. for local development),
you can either:

1. Connect to a UDS deployed version of the CowabungaAI API

   **OR**

2. Connect to OpenAI directly.

Set the following .env variables:

```bash
DEFAULT_MODEL=vllm #for OpenAI it could be: gpt-3.5-turbo
LEAPFROGAI_API_BASE_URL=https://leapfrogai-api.uds.dev #for OpenAI it would be: https://api.openai.com
```

#### Authentication

The UI uses Keycloak (via UDS) for authentication. When the UI and API are deployed with UDS, everything will be configured properly automatically.

For local development, ensure the following environment variables are set:

```bash
PUBLIC_KEYCLOAK_URL=https://sso.uds.dev/realms/uds
PUBLIC_KEYCLOAK_CLIENT_ID=your-keycloak-client-id
KEYCLOAK_CLIENT_SECRET=<secret>
```

##### With KeyCloak

1. Within Keycloak, under the UDS Realm, edit the client matching ```PUBLIC_KEYCLOAK_CLIENT_ID```.
2. Under "Valid redirect URIs" add:
   http://localhost:5173/auth/callback
   http://localhost:4173/auth/callback (for Playwright tests)

#### OpenAI

Set the following .env variables:

```bash
DEFAULT_MODEL=gpt-3.5-turbo
LEAPFROGAI_API_BASE_URL=https://api.openai.com
# If specified, app will use OpenAI instead of CowabungaAI
OPENAI_API_KEY=<your_openai_api_key>
```

## Notes and Troubleshooting

### Playwright End-to-End Tests

1. Install Playwright

   ```bash
   npm init playwright@latest
   ```

2. Run the E2E tests:

   ```bash
   npm run test:integration:ui
   ```

   Click the play button in the Playwright UI.
   Playwright will run its own production build and serve the app at ```http://localhost:4173```. If you make server side changes,
   restart playwright for them to take effect.

Notes:

1. Playwright tests are End-To-End tests and use the "real" full stack app. If you run these tests, they will use the configuration indicated by your
   .env file.
2. If you run the tests in headless mode (```npm run test:integration```) you do not need the app running, it will build the app and run on port 4173.
3. If using Keycloak, you cannot login twice within 30 seconds. If you global.setup.ts step fails, this is likely why. The setup file also tests logout, but
   this can take a long time because of the 30 second wait in between log ins. You can disable this test by setting the environment
   variable SKIP_LOGOUT_TEST=true

### Chat Data Flow

The logic for handling regular chat messages and assistant chat messages, along with persisting that data to the database is complex and deserves a detailed explanation.

Our chat page allows the user to send messages to /api/chat ("regular chat") and /api/chat/assistants ("chat with assistant"). The messages are streamed to the client so that text is
progressively displayed on the screen. We use the Vercel [AI SDK](https://sdk.vercel.ai/docs/getting-started/svelte) to handle streaming as well as response cancellation, regeneration, message editing, error handling, and more.

Messages streamed with regular chat, use the "useChat" function.
Assistants use the "useAssistants" function.
These functions do not provide the same features and handle data differently, resulting in several edge cases.

Here are a few of the big issues caused by these differences:

The useChat function does not save messages with the API to the database, we have to handle that on our own.
Messages sent with useAssistants, however, are saved to the database automatically.

Creation timestamps are handled differently depending on if they are streamed responses or if they have been saved to the database.
Streamed messages have timestamps on the "createdAt" field, saved messages have timestamps on the "created_at" field. Sometimes the dates are Date strings, unix seconds, or unix milliseconds.
Since dates can be returned in seconds, we lose some of the precision we would have for sorting the messages if they were returned in milliseconds. Due to this issue, there is logic in place to prevent the
user from sending messages too quickly, ensuring timestamps are unique.

Additionally, streamed messages have temporary ids that do not match the ids messages are assigned when they are saved to the database. This makes editing and deleting messages challenging, so we have to keep track of both streamed
messages and saved messages in client side state in the correct order. We use this state to look up the saved ids and make the appropriate API calls with the permanent ids.

While there are several automated tests for this logic, the edge cases and mocking scenarios are complex. Any modifications to this logic should be thoroughly manually tested.
