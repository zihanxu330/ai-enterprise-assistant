# Dispatch Platform Product FAQ

## What is the dispatch platform?

The Dispatch Platform is an order management system that routes service orders to the optimal station and worker. It uses an LLM dispatch engine that balances distance, worker rating, and skill match.

## How does order dispatch work?

When a customer creates an order, the platform collects the order type, address, and time window. It then ranks candidate stations by distance and estimated time of arrival, and selects the best station and worker using the LLM engine. The dispatch decision includes a short rationale.

## Does it support multiple roles?

Yes. The system supports three roles: user (place orders and track progress), station (receive and fulfill orders), and enterprise (operations dashboard, dispatch center, and analytics).

## How are API keys secured?

API keys are injected through environment variables and are git-ignored. The .env file must never be committed to the repository.

## What storage does it use?

The current version stores data in memory for demonstration. For production, MySQL or MongoDB persistence is planned, together with Redis for caching.
