import AtomsBackground from "./AtomsBackground.jsx";

/**
 * Full-viewport decorative layer: atoms canvas + dim overlay, behind dashboard (CSS z-index -1).
 */
export default function AnimatedBackground() {
  return (
    <div className="animated-background" aria-hidden="true">
      <div className="animated-background__canvas-wrap">
        <AtomsBackground />
      </div>
      <div className="animated-background__overlay" />
    </div>
  );
}
