import React from "react";

export default function PokemonSprite({
  src,
  alt,
  size = 200,
  flip = false,
  hit = false,
  fainted = false,
  style = {},
}) {
  return (
    <div
      style={{
        position: "relative",
        width: size,
        height: size,
        display: "grid",
        placeItems: "center",
        opacity: fainted ? 0.25 : 0.98,
        filter: fainted ? "grayscale(1)" : "none",
        overflow: "hidden",
        transition: "opacity 400ms ease, filter 400ms ease",
        animation: hit ? "sprite-shake 300ms ease" : "none",
        ...style,
      }}
    >
      {src ? (
        <img
          src={src}
          alt={alt}
          style={{
            width: "100%",
            height: "100%",
            minWidth: 0,
            minHeight: 0,
            objectFit: "contain",
            imageRendering: "pixelated",
            transform: flip ? "scaleX(-1)" : "none",
          }}
        />
      ) : (
        <div style={{ fontWeight: 900 }}>(Loading...)</div>
      )}

      {/* hit flash - brief red tint over the sprite, cleared by BattleArena's timeout */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "rgba(228,72,72,0.55)",
          mixBlendMode: "multiply",
          opacity: hit ? 1 : 0,
          transition: hit ? "opacity 40ms ease" : "opacity 250ms ease",
          pointerEvents: "none",
        }}
      />
    </div>
  );
}
