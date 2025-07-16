import React, { useState } from "react";
import useSound from "use-sound";
import { getBotMove } from "./api";
import DarkModeToggle from "./components/DarkModeToggle";

import rockSound from "/sounds/rock.wav";
import paperSound from "/sounds/paper.wav";
import scissorsSound from "/sounds/scissors.wav";
import shootSound from "/sounds/shoot.wav";
import winSound from "/sounds/win.wav";
import loseSound from "/sounds/lose.wav";
import drawSound from "/sounds/draw.wav";

const moves = ["rock", "paper", "scissors"];

function App() {
  const [userMove, setUserMove] = useState(null);
  const [botMove, setBotMove] = useState(null);
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [history, setHistory] = useState([]);
  const [isThrowing, setIsThrowing] = useState(false);
  const [stats, setStats] = useState({ win: 0, lose: 0, draw: 0 });

  const [playRock] = useSound(rockSound);
  const [playPaper] = useSound(paperSound);
  const [playScissors] = useSound(scissorsSound);
  const [playShoot] = useSound(shootSound);
  const [playWin] = useSound(winSound);
  const [playLose] = useSound(loseSound);
  const [playDraw] = useSound(drawSound);

  const handleUserMove = async (move) => {
    setUserMove(move);
    setBotMove(null);
    setResult("");
    setConfidence(null);
    setIsThrowing(true);

    playRock();
    setTimeout(() => playPaper(), 500);
    setTimeout(() => playScissors(), 1000);

    const response = await getBotMove(history);
    const predictedMove = response?.bot_move || moves[Math.floor(Math.random() * 3)];
    const confidenceScore = response?.confidence || 0;

    setTimeout(() => {
      playShoot();
      setBotMove(predictedMove);
      setConfidence(confidenceScore);
      setHistory((prev) => [...prev, move]);

      const result = getResult(move, predictedMove);
      setResult(result);
      updateStats(result);

      if (result === "win") playWin();
      else if (result === "lose") playLose();
      else playDraw();

      setIsThrowing(false);
    }, 1500);
  };

  const getResult = (user, bot) => {
    if (user === bot) return "draw";
    if (
      (user === "rock" && bot === "scissors") ||
      (user === "paper" && bot === "rock") ||
      (user === "scissors" && bot === "paper")
    )
      return "win";
    return "lose";
  };

  const updateStats = (result) => {
    setStats((prev) => ({
      ...prev,
      [result]: prev[result] + 1,
    }));
  };

  return (
    <div className="min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white transition-colors duration-500 flex flex-col items-center justify-center p-6 gap-6">
      <DarkModeToggle />

      <h1 className="text-4xl font-bold text-center">🤖 Rock Paper Scissors AI</h1>

      <div className="flex gap-4 flex-wrap justify-center">
        {moves.map((move) => (
          <button
            key={move}
            onClick={() => handleUserMove(move)}
            disabled={isThrowing}
            className={`${
              move === userMove ? "glow" : "bg-gray-700 dark:bg-gray-800"
            } px-6 py-3 rounded text-white hover:bg-gray-600 disabled:opacity-50`}
          >
            {move.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="mt-6 max-w-md w-full text-center border border-gray-600 rounded-lg p-4 shadow-md bg-gray-800/50 dark:bg-black/30 backdrop-blur-sm">
        {isThrowing ? (
          <p className="animate-pulse text-lg">Rock... Paper... Scissors... Shoot!</p>
        ) : userMove && botMove ? (
          <>
            <p className="text-xl mb-2">
              You: <strong>{userMove}</strong> | Bot: <strong>{botMove}</strong>
            </p>
            <p className="text-2xl font-bold mb-1">
              {result === "win" && "✅ You win!"}
              {result === "lose" && "❌ Bot wins!"}
              {result === "draw" && "🤝 It's a draw!"}
            </p>
            <p className="text-sm text-gray-400 mt-1">
              Bot confidence: {(confidence * 100).toFixed(1)}%
            </p>
          </>
        ) : (
          <p className="text-lg">Choose your move to begin!</p>
        )}
      </div>

      <div className="text-sm text-gray-400">
        📊 Wins: {stats.win} | Losses: {stats.lose} | Draws: {stats.draw}
      </div>
    </div>
  );
}

export default App;