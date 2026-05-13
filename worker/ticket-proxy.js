// Cloudflare Worker — Ticket Butler API Proxy
// Exposes a read-only endpoint for live ticket data without leaking the API token.
//
// Environment variables (set in Cloudflare dashboard):
//   TICKETBUTLER_API_TOKEN — Your API token
//   TICKETBUTLER_EVENT_UUID — The event UUID to fetch
//   ALLOWED_ORIGIN — Your site origin (e.g., https://bsidesaarhus.dk)
//   PUBLIC_TICKET_TYPE_UUIDS — Comma-separated UUIDs of public ticket types
//     (excludes internal types like Speaker/Crew/Goon from the counter)

const CACHE_TTL = 30; // seconds — how long to cache responses

const DEFAULT_PUBLIC_UUIDS = [
  "ad0158e893ec46a58b6d1266f71aed64", // Human
  "fe348f8948554497ad44637bb37103ee", // Community Friend
  "c100b3a716b54a9ab329f76cc123853b", // Student
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const configuredAllowedOrigin =
      env.ALLOWED_ORIGIN || "https://bsidesaarhus.dk";
    let allowedOrigin;
    try {
      allowedOrigin = new URL(configuredAllowedOrigin).origin;
    } catch {
      return jsonResponse({ error: "Worker not configured" }, 500, "null");
    }

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
    if (origin) {
      let requestOrigin;
      try {
        requestOrigin = new URL(origin).origin;
      } catch {
        return jsonResponse({ error: "Forbidden" }, 403, allowedOrigin);
      }

      if (requestOrigin !== allowedOrigin) {
        return jsonResponse({ error: "Forbidden" }, 403, allowedOrigin);
      }
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

      const allTicketTypes = await apiResponse.json();

      const allowlist = (env.PUBLIC_TICKET_TYPE_UUIDS || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
      const publicUUIDs = allowlist.length ? allowlist : DEFAULT_PUBLIC_UUIDS;
      const ticketTypes = allTicketTypes.filter(
        (t) => t.active !== false && publicUUIDs.includes(t.uuid)
      );

      const totalSold = ticketTypes.reduce(
        (sum, t) => sum + (t.amount_sold || 0),
        0
      );
      const totalAvailable = ticketTypes.reduce(
        (sum, t) => sum + (t.amount_total || 0),
        0
      );
      const totalInBasket = ticketTypes.reduce((sum, t) => {
        const total = t.amount_total || 0;
        const sold = t.amount_sold || 0;
        const left = t.amount_left == null ? total - sold : t.amount_left;
        return sum + Math.max(0, total - sold - left);
      }, 0);

      const data = {
        total_sold: totalSold,
        total_available: totalAvailable,
        total_in_basket: totalInBasket,
        fetched_at: new Date().toISOString(),
        ticket_types: ticketTypes.map((t) => {
          const total = t.amount_total || 0;
          const sold = t.amount_sold || 0;
          const left = t.amount_left == null ? total - sold : t.amount_left;
          const inBasket = Math.max(0, total - sold - left);
          return {
            uuid: t.uuid,
            title: t.title,
            price: t.price,
            currency: t.currency || "DKK",
            amount_total: total,
            amount_sold: sold,
            amount_remaining: left,
            amount_in_basket: inBasket,
            is_sold_out: sold >= total,
          };
        }),
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
