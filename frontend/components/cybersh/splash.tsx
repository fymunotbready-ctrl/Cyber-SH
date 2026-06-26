"use client"

import { ACCENT_RGB, ACCENT_HEX } from "./lib"

export function Splash({ done }: { done: boolean }) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--page-bg)",
        transition: "opacity 0.7s cubic-bezier(0.4,0,0.2,1), transform 0.7s cubic-bezier(0.4,0,0.2,1), filter 0.7s ease",
        opacity: done ? 0 : 1,
        transform: done ? "scale(1.08)" : "scale(1)",
        filter: done ? "blur(8px)" : "blur(0px)",
        pointerEvents: done ? "none" : "auto",
        zIndex: 1000,
        overflow: "hidden",
      }}
    >
      {/* deep ambient wash */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.08) 0%, transparent 55%)",
          pointerEvents: "none",
        }}
      />

      {/* expanding glow rings behind the mark */}
      <div
        style={{
          position: "absolute",
          width: 320,
          height: 320,
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(255,255,255,0.20) 0%, rgba(255,255,255,0.08) 35%, transparent 70%)`,
          filter: "blur(50px)",
          animation: "cyberRing 3.2s ease-in-out infinite",
        }}
      />

      {/* sharp burst ring synced with the pop */}
      <div
        style={{
          position: "absolute",
          width: 240,
          height: 240,
          borderRadius: "50%",
          border: "1.5px solid rgba(var(--tint-rgb),0.5)",
          animation: "ringBurst 1.4s 0.15s cubic-bezier(0.22,1,0.36,1) both",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 240,
          height: 240,
          borderRadius: "50%",
          border: "1px solid rgba(var(--tint-rgb),0.3)",
          animation: "ringBurst 1.6s 0.32s cubic-bezier(0.22,1,0.36,1) both",
          pointerEvents: "none",
        }}
      />

      {/* logo mark */}
      <div
        style={{
          position: "relative",
          animation:
            "logoPop 1.25s cubic-bezier(0.34,1.56,0.64,1) both, cyberFloat 3.6s 1.4s ease-in-out infinite",
        }}
      >
        <img
          src="/cyber-sh-logo-trans.png"
          alt="Cyber-SH"
          width={220}
          height={196}
          style={{
            width: "min(58vw, 240px)",
            height: "auto",
            display: "block",
            filter: `drop-shadow(0 0 26px rgba(${ACCENT_RGB},0.55)) drop-shadow(0 14px 40px rgba(0,0,0,0.6))`,
          }}
        />
        {/* sheen sweep across the mark */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            overflow: "hidden",
            pointerEvents: "none",
            maskImage: "url(/cyber-sh-logo-trans.png)",
            WebkitMaskImage: "url(/cyber-sh-logo-trans.png)",
            maskSize: "contain",
            WebkitMaskSize: "contain",
            maskRepeat: "no-repeat",
            WebkitMaskRepeat: "no-repeat",
            maskPosition: "center",
            WebkitMaskPosition: "center",
          }}
        >
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "55%",
              height: "100%",
              background:
                "linear-gradient(105deg, transparent 20%, rgba(255,255,255,0.5) 50%, transparent 80%)",
              animation: "lgShimmer 2.6s 0.9s ease-in-out infinite",
            }}
          />
        </div>
      </div>

      <div
        style={{
          marginTop: 30,
          fontSize: 12,
          fontWeight: 600,
          letterSpacing: "0.32em",
          color: `rgba(${ACCENT_RGB},0.9)`,
          textTransform: "uppercase",
          animation: "cyberSlideUp 0.7s 0.7s both",
        }}
      >
        Cyber&nbsp;—&nbsp;SH
      </div>
      <div
        style={{
          marginTop: 10,
          fontSize: 11,
          color: "rgba(var(--tint-rgb),0.32)",
          letterSpacing: "0.1em",
          animation: "cyberSlideUp 0.7s 0.95s both",
        }}
      >
        Your personal AI assistant
      </div>

      {/* loading shimmer bar */}
      <div
        style={{
          marginTop: 26,
          width: 132,
          height: 3,
          borderRadius: 3,
          overflow: "hidden",
          background: "rgba(var(--tint-rgb),0.08)",
          animation: "cyberSlideUp 0.7s 1.1s both",
        }}
      >
        <div
          style={{
            width: "40%",
            height: "100%",
            borderRadius: 3,
            background: `linear-gradient(90deg, transparent, ${ACCENT_HEX}, transparent)`,
            animation: "loadSweep 1.3s ease-in-out infinite",
          }}
        />
      </div>
    </div>
  )
}
