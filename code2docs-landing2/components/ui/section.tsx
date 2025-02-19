import * as React from "react";

import { cn } from "@/lib/utils";

const Section = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <section
    ref={ref}
    className={cn(
      "bg-background px-4 py-12 text-foreground sm:py-24 md:py-32",
      className,
    )}
    {...props}
  />
));
Section.displayName = "Section";

export { Section };
