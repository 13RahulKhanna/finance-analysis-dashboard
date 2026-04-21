import { useEffect, useRef } from "react";

function AtomsBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    resize();
    window.addEventListener("resize", resize);

    const particles = [];

    // 🔥 create particles
    for (let i = 0; i < 40; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        size: Math.random() * 4 + 2,
      });
    }

    let rafId = 0;

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p) => {
        // move
        p.x += p.vx;
        p.y += p.vy;

        // bounce
        if (p.x <= 0 || p.x >= canvas.width) p.vx *= -1;
        if (p.y <= 0 || p.y >= canvas.height) p.vy *= -1;

        // draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = "#00eaff";
        ctx.shadowBlur = 15;
        ctx.shadowColor = "#00eaff";
        ctx.fill();
      });

      rafId = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(rafId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        opacity: 0.35,
      }}
    />
  );
}

export default AtomsBackground;
