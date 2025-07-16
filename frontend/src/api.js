import axios from "axios";

// Base URL of your FastAPI backend
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Create Axios instance
const API = axios.create({
  baseURL: BASE_URL,
  timeout: 5000, // optional timeout
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * @typedef {Object} BotResponse
 * @property {"rock" | "paper" | "scissors"} bot_move
 * @property {number} confidence
 */

/**
 * Send user move history to the backend and receive the bot's predicted move.
 * @param {string[]} history - Last N user moves (e.g., ["rock", "paper"])
 * @returns {Promise<BotResponse|null>} - Bot's move and confidence, or null if failed
 */
export const getBotMove = async (history) => {
  try {
    const response = await API.post("/move", { history });

    if (!response?.data?.bot_move) {
      throw new Error("Malformed response from backend.");
    }

    return {
      bot_move: response.data.bot_move,
      confidence: response.data.confidence,
    };
  } catch (error) {
    console.error("[API ERROR] Failed to fetch bot move:", error.message);
    return null;
  }
};

/**
 * Ping the backend to verify it's alive.
 * @returns {Promise<boolean>} - True if server is alive, false otherwise.
 */
export const pingServer = async () => {
  try {
    const res = await API.get("/ping");
    return res.data?.message === "Bot is alive!";
  } catch (error) {
    console.warn("[API WARNING] Could not reach backend:", error.message);
    return false;
  }
};