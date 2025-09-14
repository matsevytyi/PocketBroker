import express from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// serve static files (public/index.html)
app.use(express.static("public"));

// minimal config endpoint – sends PUBLIC key only
// (Optionally: generate a short-lived JWT here instead)
app.get("/config", (req, res) => {
  const { VAPI_PUBLIC_KEY, VAPI_API_KEY, ASSISTANT_ID } = process.env;
  
  // Use public key if available, otherwise fallback to API key
  const apiKey = VAPI_PUBLIC_KEY || VAPI_API_KEY;
  
  if (!apiKey) {
    return res.status(500).json({ error: "Server missing VAPI_PUBLIC_KEY or VAPI_API_KEY in .env file" });
  }
  
  res.json({
    apiKey: apiKey,
    assistant: ASSISTANT_ID || null
  });
});

app.listen(PORT, () =>
  console.log(`Server listening on http://localhost:${PORT}`)
);
