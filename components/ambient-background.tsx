export function AmbientBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden="true">
      <div
        className="absolute -top-40 -left-32 h-[36rem] w-[36rem] rounded-full"
        style={{
          background: "radial-gradient(circle, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0) 70%)",
          filter: "blur(140px)",
          animation: "floatGlowA 18s ease-in-out infinite",
        }}
      />
      <div
        className="absolute top-1/3 -right-40 h-[40rem] w-[40rem] rounded-full"
        style={{
          background: "radial-gradient(circle, rgba(120,170,255,0.07) 0%, rgba(255,255,255,0) 70%)",
          filter: "blur(150px)",
          animation: "floatGlowB 22s ease-in-out infinite",
        }}
      />
      <div
        className="absolute bottom-0 left-1/4 h-[34rem] w-[34rem] rounded-full"
        style={{
          background: "radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 70%)",
          filter: "blur(130px)",
          animation: "floatGlowC 26s ease-in-out infinite",
        }}
      />
    </div>
  )
}
