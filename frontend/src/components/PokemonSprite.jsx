import React from "react";

export default function PokemonSprite({
  src,
  alt,
  size = 200,
  flip = false,
  style = {},
}) {
  return (
    <div
      style={{
        width: size,
        height: size,
        display: "grid",
        placeItems: "center",
        opacity: 0.98,
        overflow: "hidden",
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
    </div>
  );
}
