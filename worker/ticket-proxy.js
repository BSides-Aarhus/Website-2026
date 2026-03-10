// Cloudflare Worker — Ticket Butler API Proxy
// Exposes a read-only endpoint for live ticket data without leaking the API token.
//
// Environment variables (set in Cloudflare dashboard):
//   TICKETBUTLER_API_TOKEN — Your API token
//   TICKETBUTLER_EVENT_UUID — The event UUID to fetch
//   ALLOWED_ORIGIN — Your site origin (e.g., https://bsidesaarhus.dk)

const CACHE_TTL = 30; // seconds — how long to cache responses

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowedOrigin = env.ALLOWED_ORIGIN || "https://bsidesaarhus.dk";

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders(allowedOrigin),
      });
    }

    // Only allow GET
    if (request.method !== "GET") {
      return jsonResponse({ error: "Method not allowed" }, 405, allowedOrigin);
    }

    // Only allow requests from our site
    if (origin && !origin.startsWith(allowedOrigin)) {
      return jsonResponse({ error: "Forbidden" }, 403, allowedOrigin);
    }

    const token = env.TICKETBUTLER_API_TOKEN;
    const eventUUID = env.TICKETBUTLER_EVENT_UUID;

    if (!token || !eventUUID) {
      return jsonResponse({ error: "Worker not configured" }, 500, allowedOrigin);
    }

    // Check cache
    const cacheKey = new Request(`https://cache.internal/tickets/${eventUUID}`);
    const cache = caches.default;
    let response = await cache.match(cacheKey);

    if (response) {
      // Add CORS headers to cached response
      const newHeaders = new Headers(response.headers);
      Object.entries(corsHeaders(allowedOrigin)).forEach(([k, v]) =>
        newHeaders.set(k, v)
      );
      return new Response(response.body, {
        status: response.status,
        headers: newHeaders,
      });
    }

    // Fetch from Ticket Butler API
    try {
      const apiResponse = await fetch(
        `https://bsidesaarhus.ticketbutler.io/api/v3/events/${eventUUID}/ticket-types/`,
        {
          headers: { Authorization: `Token ${token}` },
        }
      );

      if (!apiResponse.ok) {
        return jsonResponse(
          { error: "Upstream API error" },
          apiResponse.status,
          allowedOrigin
        );
      }

      const ticketTypes = await apiResponse.json();

      const totalSold = ticketTypes.reduce(
        (sum, t) => sum + (t.amount_sold || 0),
        0
      );
      const totalAvailable = ticketTypes.reduce(
        (sum, t) => sum + (t.amount_total || 0),
        0
      );

      const data = {
        total_sold: totalSold,
        total_available: totalAvailable,
        fetched_at: new Date().toISOString(),
        ticket_types: ticketTypes.map((t) => ({
          uuid: t.uuid,
          title: t.title,
          price: t.price,
          currency: t.currency || "DKK",
          amount_total: t.amount_total || 0,
          amount_sold: t.amount_sold || 0,
          amount_remaining: (t.amount_total || 0) - (t.amount_sold || 0),
          is_sold_out: (t.amount_sold || 0) >= (t.amount_total || 0),
        })),
      };

      // Cache the response
      response = jsonResponse(data, 200, allowedOrigin);
      response.headers.set("Cache-Control", `public, max-age=${CACHE_TTL}`);

      const cacheResponse = response.clone();
      await cache.put(cacheKey, cacheResponse);

      return response;
    } catch (err) {
      return jsonResponse(
        { error: "Failed to fetch ticket data" },
        502,
        allowedOrigin
      );
    }
  },
};

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin),
    },
  });
}
