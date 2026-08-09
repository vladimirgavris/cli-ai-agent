# OpenAI Responses API

The API key is read locally from `.env` as OPENAI_API_KEY. Never paste or commit it.
The CLI uses the Responses API. A request can contain instructions, input, tools,
and a maximum output-token limit.

A model does not automatically remember an earlier API request. The application
stores visible user/assistant messages in a conversation JSON file and sends
the relevant transcript again on the next request.

An API call can fail because of authentication, connectivity, invalid requests,
or a service status error.